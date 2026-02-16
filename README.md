# PDF to Word Converter

A lightweight, private (locally hosted), and fast application to convert PDF files into editable Word documents (`.docx`). No need for any more online third-party services. 

I solved my own problem as I needed to convert a large pdf files for a project into text files and found it hard to do so with the available online tools. Some were free but crashed on large files, others were paid and I didn't want to pay for a service I would use only once. 

## Features
- **Drag & Drop Interface**: Simple and intuitive modern UI.
- **Large File Support**: Optimized to handle PDF files up to 1GB.
- **Local Processing**: detailed privacy - your files never leave your machine.
- **One-Click Launch**: Includes a convenient desktop shortcut.

## Quick Start
**Use the Desktop Shortcut:**
Double-click the "PDF Converter" icon on your Desktop.

**Or run manually:**
Double-click `run_app.bat` in this folder.

## Manual Installation (for developers)
1.  **Clone/Download** this repository.
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the App**:
    ```bash
    python app.py
    ```
4.  Open `http://localhost:5000` in your browser.

## Technologies
- **Backend**: Python, Flask, PyMuPDF (fitz), python-docx
- **Frontend**: HTML5, CSS3, JavaScript

## Troubleshooting
- If the app doesn't start, ensure you have Python installed and added to your PATH.
- If a conversion fails for a very specific PDF, please check if the PDF is password protected or corrupted.
