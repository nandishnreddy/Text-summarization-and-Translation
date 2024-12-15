from flask import Flask, render_template, request
from main import summerizer, translate_summary
import os
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
import docx

app = Flask(__name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

# File upload folder
app.config['UPLOAD_FOLDER'] = 'uploads/'


# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


# Function to extract text from DOCX
def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text


@app.route("/", methods=["GET", "POST"])
def home():
    summary = None
    original_len = None
    summarized_len = None

    if request.method == "POST":
        raw_text = request.form.get("text")
        file = request.files.get("file")

        if raw_text:
            summary, keywords, _, original_len, summarized_len = summerizer(raw_text)
            return render_template("result.html", summary=summary, keywords=keywords, original_len=original_len,
                                       summarized_len=summarized_len)

        if file and allowed_file(file.filename):
            # Secure the filename and save the file
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Extract text based on file type
            if file.filename.endswith('.txt'):
                with open(file_path, 'r') as f:
                    raw_text = f.read()
            elif file.filename.endswith('.pdf'):
                raw_text = extract_text_from_pdf(file_path)
            elif file.filename.endswith('.docx'):
                raw_text = extract_text_from_docx(file_path)

            if raw_text:
                summary, keywords, _, original_len, summarized_len = summerizer(raw_text)
                return render_template("result.html", summary=summary, keywords=keywords, original_len=original_len,
                                       summarized_len=summarized_len)

    return render_template(
        "index.html",
        summary=summary,
        original_len=original_len,
        summarized_len=summarized_len
    )


@app.route('/translate', methods=['POST'])
def translate():
    summary = request.form.get("summary")
    target_language = request.form.get("language")

    if summary and target_language:
        try:
            translated = translate_summary(summary, target_language)
            return render_template(
                "result.html",
                summary=summary,
                translation=translated,
                language=target_language
            )
        except Exception as e:
            return f"Error during translation: {e}", 500

    return "Error: Missing text or language input", 400


if __name__ == "__main__":
    app.run(debug=True)
