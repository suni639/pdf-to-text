# PDF to Word Converter

A lightweight, private (locally hosted), and fast application to convert PDF files into editable Word documents (`.docx`). No need for any more online third-party services. 

I solved my own problem as I needed to convert large PDF files for a project into text files and found it tricky with the available online tools. Some were free but crashed on large files (plus you don't know who to trust!), others were paid and I didn't want to pay for that kind of service. 

## Features
- **Drag & Drop Interface**: Simple and intuitive modern UI.
- **Large File Support**: Optimised to handle PDF files up to 1GB.
- **Local Processing**: Complete privacy - your files never leave your machine.
- **One-Click Launch**: Includes a convenient desktop shortcut script. No faff.

## Installation & Setup

**Important:** For the desktop shortcut script to work out-of-the-box, place this project folder exactly at: `C:\Projects\dev\pdf-to-text`. Otherwise be aware of where the different filepaths are pointing to in the codebase.

1. **Clone or Download** this repository to your machine.
2. **Open a command prompt** in the project folder.
3. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
4.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
5. **Create the Desktop Shortcut (Optional):**
   Right-click `create_shortcut.ps1` and select **Run with PowerShell**. This will place a "PDF Converter" icon on your Desktop.

## Quick Start
Once installed, you can launch the app in two ways:
- **Desktop Shortcut:** Double-click the "PDF Converter" icon on your Desktop.
- **Manual Launch:** Double-click `run_app.bat` inside the project folder.

A command window will open to start the local server, and your default web browser will automatically open the application at `http://localhost:5000`.

## Technologies
- **Backend**: Python, Flask, PyMuPDF (fitz), python-docx
- **Frontend**: HTML5, CSS3, JavaScript

## Troubleshooting
- If the app doesn't start, ensure you have Python installed and added to your system PATH.
- If the `.bat` file briefly flashes and closes, ensure you have created the `venv` folder as described in the installation steps.
- If a conversion fails for a specific PDF, check if the PDF is password-protected or corrupted.