from flask import Flask, request, render_template
import joblib
import os
from PyPDF2 import PdfReader
import spacy
import re

app = Flask(__name__)

# Load model, vectorizer, and NLP
model_path = os.path.join('models', 'resume screening model.pkl')
vectorizer_path = os.path.join('models', 'tfidf_vectorizer.pkl')
model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)
nlp = spacy.load('en_core_web_sm')

# Predefined key skills to search for
KEY_SKILLS = [
    "Data Analysis", "Machine Learning", "Data Science", "Python", "SQL", "R",
    "Deep Learning", "Statistics", "Data Visualization", "Big Data", "Tableau", "Power BI",
    "Cloud Computing", "AWS", "Azure", "Hadoop", "Spark", "Natural Language Processing"
]

def extract_text_from_pdf(file):
    """
    Extract text from a PDF file.
    """
    try:
        pdf_reader = PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise ValueError(f"Could not extract text from PDF: {e}")

def extract_contact_info(text):
    """
    Extracts email, phone, and LinkedIn from text.
    """
    email = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', text)
    phone = re.search(r'\+?\d[\d -]{8,}\d', text)
    linkedin = re.search(r'linkedin\.com/in/[A-Za-z0-9-]+', text)

    return {
        "email": email.group(0) if email else "Not found",
        "phone": phone.group(0) if phone else "Not found",
        "linkedin": f"https://{linkedin.group(0)}" if linkedin else "Not found"
    }
SKILL_CATEGORIES = {
    "Technical Skills": [
        "python", "java", "c++", "javascript", "html", "css", "sql", "r", "matlab", "linux", "docker", "aws", "azure", "hadoop"
    ],
    "Soft Skills": [
        "communication", "teamwork", "leadership", "problem-solving", "adaptability", "time management", "critical thinking", "collaboration"
    ],
    "Domain-Specific Skills": [
        "data science", "machine learning", "deep learning", "data analysis", "data visualization", "business analysis", "cloud computing", "artificial intelligence", "web development", "cybersecurity"
    ],
    "Design Skills": [
        "ui/ux", "photoshop", "illustrator", "figma", "adobe xd", "wireframing", "prototyping"
    ]
}

def extract_skills(text):
    """
    Extracts skills from text using predefined categories and NLP.
    """
    # Convert the text to lowercase for better matching
    text = text.lower()

    # List to hold found skills
    found_skills = {
        "Technical Skills": [],
        "Soft Skills": [],
        "Domain-Specific Skills": [],
        "Design Skills": []
    }

    # Iterate over each category
    for category, skills in SKILL_CATEGORIES.items():
        for skill in skills:
            if skill in text:
                found_skills[category].append(skill)

    # Remove duplicates and return the skills
    for category in found_skills:
        found_skills[category] = list(set(found_skills[category]))

    return found_skills

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        # Check for file upload
        if 'resumes' not in request.files:
            return "No files part in the request", 400

        files = request.files.getlist('resumes')

        if not files or all(file.filename == '' for file in files):
            return "No files selected", 400

        for file in files:
            try:
                # Extract text based on file type
                if file.filename.endswith('.pdf'):
                    content = extract_text_from_pdf(file)
                elif file.filename.endswith('.txt'):
                    content = file.read().decode('utf-8')
                else:
                    results.append({
                        "filename": file.filename,
                        "error": "Unsupported file type. Please upload PDF or text files."
                    })
                    continue

                # Extract features
                contact_info = extract_contact_info(content)
                skills = extract_skills(content)  # Returns skills categorized
                features = vectorizer.transform([content])  # Vectorize the input
                prediction = model.predict(features)  # Predict the output
                job_category = prediction[0]

                results.append({
                    "filename": file.filename,
                    "job_category": job_category,
                    "email": contact_info["email"],
                    "phone": contact_info["phone"],
                    "linkedin": contact_info["linkedin"],
                    "skills": skills  # Pass the categorized skills here
                })

            except Exception as e:
                results.append({
                    "filename": file.filename,
                    "error": str(e)
                })

        return render_template('resume.html', results=results)

    return render_template('resume.html', results=None)

if __name__ == '__main__':
    app.run(debug=True)
