import os
import tempfile
import fitz  # PyMuPDF
from flask import Flask, render_template, request, send_file, jsonify
from docx import Document
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure maximum file size (1GB)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # 1GB

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.lower().endswith('.pdf'):
        try:
            # Create a temporary file to save the uploaded PDF
            fd, temp_pdf_path = tempfile.mkstemp(suffix='.pdf')
            os.close(fd)
            
            # Save uploaded file to temp path
            file.save(temp_pdf_path)
            
            # Create a new Word document
            doc = Document()
            
            # Open the PDF
            pdf_document = fitz.open(temp_pdf_path)
            
            # Extract text from each page
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                text = page.get_text()
                doc.add_paragraph(text)
                # Add a page break after each page (optional, but good for structure)
                if page_num < len(pdf_document) - 1:
                    doc.add_page_break()
            
            pdf_document.close()
            
            # Save the Word document to a temporary file
            fd_out, temp_docx_path = tempfile.mkstemp(suffix='.docx')
            os.close(fd_out)
            doc.save(temp_docx_path)
            
            # Clean up the input PDF
            os.remove(temp_pdf_path)
            
            # Send the file and suggest a filename
            output_filename = os.path.splitext(secure_filename(file.filename))[0] + '.docx'
            
            # Use a generator to delete the file after sending
            def generate():
                with open(temp_docx_path, 'rb') as f:
                    yield from f
                os.remove(temp_docx_path)

            # Note: Flask's send_file doesn't easily support delete-after-send with generator directly in all versions 
            # without correct headers. A safer approach for local app is to just send it and let OS/periodic cleanup handle it, 
            # or try-finally block if synchronous.
            # Simplified approach: Send file, then user OS will clean temp eventually or we can risk a small leak in a focused local app.
            # BETTER: Read into memory if size allows? No, 1GB file.
            # BEST: Use `after_this_request` callback.
            
            @flask.after_this_request
            def remove_file(response):
                try:
                    os.remove(temp_docx_path)
                except Exception as e:
                    app.logger.error(f"Error removing temp file: {e}")
                return response
                
            return send_file(temp_docx_path, as_attachment=True, download_name=output_filename)

        except Exception as e:
            return jsonify({'error': str(e)}), 500
            
    return jsonify({'error': 'Invalid file type. Please upload a PDF.'}), 400

# Fix for name 'flask' is not defined in the inner function
import flask 

if __name__ == '__main__':
    app.run(debug=False, port=5000)
