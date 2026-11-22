import io
import os
import tempfile

import pymupdf  # PyMuPDF
from docx import Document
from flask import Flask, jsonify, render_template, request, send_file
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

    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Invalid file type. Please upload a PDF.'}), 400

    # The uploaded PDF goes to a temporary file so PyMuPDF can read large files from disk.
    # It is always deleted in `finally`, whether or not the conversion succeeds.
    fd, temp_pdf_path = tempfile.mkstemp(suffix='.pdf')
    os.close(fd)
    try:
        file.save(temp_pdf_path)

        doc = Document()
        words_found = 0
        with pymupdf.open(temp_pdf_path) as pdf_document:
            page_count = len(pdf_document)
            for page_num in range(page_count):
                text = pdf_document.load_page(page_num).get_text()
                words_found += len(text.split())
                doc.add_paragraph(text)
                # Page break after each page, to keep the PDF's structure
                if page_num < page_count - 1:
                    doc.add_page_break()

        if words_found == 0:
            return jsonify({'error': 'No text found in this PDF. It may be a scanned document '
                                     '(text stored as images), which needs OCR to convert.'}), 422

        # Build the Word document in memory, so no converted copy is left on disk.
        output = io.BytesIO()
        doc.save(output)
        output.seek(0)

        output_filename = os.path.splitext(secure_filename(file.filename))[0] + '.docx'
        return send_file(
            output,
            as_attachment=True,
            download_name=output_filename,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        try:
            os.remove(temp_pdf_path)
        except OSError as e:
            app.logger.error(f"Error removing temp file: {e}")


if __name__ == '__main__':
    app.run(debug=False, port=5000)
