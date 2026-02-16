document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const browseBtn = document.getElementById('browse-btn');
    const loadingOverlay = document.getElementById('loading-overlay');
    const statusMessage = document.getElementById('status-message');
    const progressBar = document.getElementById('progress-bar');

    // Trigger file input click when browse button is clicked
    browseBtn.addEventListener('click', (e) => {
        e.stopPropagation(); // Prevent bubbling up to dropZone click
        fileInput.click();
    });

    // Make the entire drop zone clickable to browse files
    dropZone.addEventListener('click', () => {
        fileInput.click();
    });

    // Handle file selection via input
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    // Drag and Drop Events
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('drag-over');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');

        if (e.dataTransfer.files.length > 0) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    function handleFile(file) {
        if (file.type !== 'application/pdf' && !file.name.toLowerCase().endsWith('.pdf')) {
            showStatus('Please upload a valid PDF file.', 'error');
            return;
        }

        uploadFile(file);
    }

    function uploadFile(file) {
        // Reset UI
        showStatus('', ''); // clear status
        loadingOverlay.classList.remove('hidden');
        progressBar.style.width = '0%';

        const formData = new FormData();
        formData.append('file', file);

        const xhr = new XMLHttpRequest();

        xhr.open('POST', '/convert', true);

        // Progress event
        xhr.upload.onprogress = (e) => {
            if (e.lengthComputable) {
                const percentComplete = (e.loaded / e.total) * 100;
                // Cap upload progress visually at 50% to leave room for processing
                progressBar.style.width = (percentComplete * 0.5) + '%';
            }
        };

        xhr.onload = () => {
            if (xhr.status === 200) {
                // Success: File download is triggered
                progressBar.style.width = '100%';

                // Trigger download manually if needed, but normally browser handles attachment
                // However, binary response via AJAX needs handling to blob
                const blob = xhr.response;
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;

                // Get filename from header or default
                let filename = 'converted.docx';
                const disposition = xhr.getResponseHeader('Content-Disposition');
                if (disposition && disposition.indexOf('attachment') !== -1) {
                    const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                    const matches = filenameRegex.exec(disposition);
                    if (matches != null && matches[1]) {
                        filename = matches[1].replace(/['"]/g, '');
                    }
                }

                a.download = filename;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);

                setTimeout(() => {
                    loadingOverlay.classList.add('hidden');
                    showStatus('Conversion successful! Download started.', 'success');
                }, 500);
            } else {
                loadingOverlay.classList.add('hidden');
                // Read the blob as text to get the error message
                const reader = new FileReader();
                reader.onload = function () {
                    try {
                        const response = JSON.parse(reader.result);
                        showStatus(response.error || 'An error occurred during conversion.', 'error');
                    } catch (e) {
                        showStatus('An error occurred during conversion.', 'error');
                    }
                };
                reader.onerror = function () {
                    showStatus('An error occurred during conversion.', 'error');
                };
                reader.readAsText(xhr.response);
            }

        };

        xhr.onerror = () => {
            loadingOverlay.classList.add('hidden');
            showStatus('Network error occurred.', 'error');
        };

        xhr.responseType = 'blob'; // Important for file download
        xhr.send(formData);

        // Mock progress for the processing phase (after upload)
        let processingProgress = 50;
        const interval = setInterval(() => {
            if (xhr.readyState === 4) {
                clearInterval(interval);
            } else if (processingProgress < 95) {
                processingProgress += 1;
                progressBar.style.width = processingProgress + '%';
            }
        }, 500); // Slow increment
    }

    function showStatus(message, type) {
        statusMessage.textContent = message;
        statusMessage.className = 'status-message ' + type;
        if (message) {
            statusMessage.classList.remove('hidden');
        } else {
            statusMessage.classList.add('hidden');
        }
    }
});
