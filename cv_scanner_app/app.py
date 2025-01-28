from flask import Flask, request, render_template, redirect, url_for
import os
from werkzeug.utils import secure_filename
import spacy
import fitz  # PyMuPDF
import re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

nlp = spacy.load('en_core_web_sm')

# Danh sách các từ khóa kỹ năng phổ biến
skills_keywords = ["Python", "SQL", "Data Analysis", "Data Visualization", "Machine Learning", "Deep Learning",
                   "Natural Language Processing", "Time Management", "Teamwork", "Communication", "Problem Solving",
                   "Critical Thinking", "Microsoft Office", "Power BI", "Tableau"]

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def highlight_skills(text, skills):
    for skill in skills:
        text = re.sub(f"(?i)({re.escape(skill)})", r'<span class="highlight">\1</span>', text)
    return text

def extract_skills(text):
    extracted_skills = set()
    for keyword in skills_keywords:
        if keyword.lower() in text.lower():
            extracted_skills.add(keyword)
    return list(extracted_skills)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        text = extract_text_from_pdf(file_path)
        skills = extract_skills(text)
        highlighted_text = highlight_skills(text, skills)  # Văn bản đã được highlight
        
        return render_template('result.html', skills=skills, text=highlighted_text)  # Trả về văn bản đã highlight

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)