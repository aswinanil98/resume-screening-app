NLP-Based Resume Screening Application
An AI-powered web application for automating resume screening and classification using Natural Language Processing (NLP) techniques. The tool extracts key information from resumes and categorizes them based on job roles, helping recruiters streamline their hiring process.

🚀 Features
Upload multiple resumes in PDF or text format.
Extracts key details like:
Contact Information (Email, Phone, LinkedIn).
Key Skills (including predefined skill categories).
Predicts job categories for resumes using a trained machine learning model.
Displays results in a user-friendly web interface.
Powered by Flask, Scikit-learn, SpaCy, and PyPDF2.
🔧 Technology Stack
Backend: Flask (Python-based web framework).
NLP: SpaCy for text processing and entity extraction.
Machine Learning: Scikit-learn for model training and predictions.
Data Parsing: PyPDF2 for extracting text from PDF files.
Frontend: HTML, CSS, Bootstrap for a responsive user interface.

📊 Workflow
Upload Resumes: Upload single or multiple resume files.
Data Extraction:
Extracts text, skills, and contact information.
Prediction: Uses a machine learning model to classify resumes into job categories.
Result Display: Presents structured results, including the job category and extracted details, on a web page.

📁 Directory Structure
graphql
resume-screening-app/
│
├── models/                     # Contains trained ML model and vectorizer
│   ├── resume_screening_model.pkl
│   └── tfidf_vectorizer.pkl
│
├── templates/                  # HTML templates for Flask
│   └── resume.html
│
├── static/                     # CSS and JS files
│   └── style.css
│
├── app.py                      # Main Flask application
├── requirements.txt            # Dependencies for the project
└── README.md                   # Project documentation

🛡️ Security Considerations
Ensure the input files are sanitized to avoid malicious file uploads.
Use HTTPS in deployment for secure data transfer.
Store models and sensitive configurations securely.

🌟 Future Enhancements
Integrate more advanced NLP models for improved accuracy.
Add support for additional resume formats (e.g., DOCX).
Provide downloadable reports for recruiters.
Extend predictions to rank resumes based on predefined criteria.

🤝 Contributing
Contributions are welcome! Feel free to fork the repository, create a branch, and submit a pull request. For major changes, open an issue to discuss your ideas first.

📧 Contact
For any queries or feedback, please reach out to: aswin.anil1998@gmail.com
https://www.linkedin.com/in/aswin-anil-00b85419b/
