import os
import re
import io
import pickle
from flask import Flask, render_template, request
from pypdf import PdfReader
from docx import Document

app = Flask(__name__)

# Load trained classification model — use absolute path so it works on Vercel too
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "model.pkl"), "rb") as f:
    model = pickle.load(f)

# Core skills mapping for each job role
required_skills = {
    "Full Stack Developer": ["html", "css", "javascript", "react", "node", "express", "mongodb", "sql", "git"],
    "Backend Developer": ["python", "flask", "django", "sql", "api", "authentication", "git"],
    "Data Analyst": ["python", "pandas", "numpy", "sql", "excel", "statistics", "visualization"],
    "AI ML Engineer": ["python", "numpy", "pandas", "sklearn", "machine learning", "deep learning", "data preprocessing"],
    "Cybersecurity Analyst": ["networking", "linux", "security", "python", "wireshark", "cryptography"]
}

# Dynamic roadmaps for skills development
learning_path = {
    "Full Stack Developer": [
        "Learn HTML, CSS, and JavaScript fundamentals thoroughly",
        "Build small static websites to practice layout and styling",
        "Learn a frontend framework like React",
        "Learn Node.js and Express for backend development",
        "Learn how to connect a database like MongoDB or MySQL",
        "Practice by building full projects that connect frontend and backend"
    ],
    "Backend Developer": [
        "Get strong in Python basics and OOP concepts",
        "Learn Flask or Django framework fundamentals",
        "Understand REST APIs and how to design endpoints",
        "Learn SQL and how to connect a database to your app",
        "Learn authentication concepts like JWT and sessions",
        "Practice deploying a backend project on a free hosting service"
    ],
    "Data Analyst": [
        "Strengthen Python basics, especially with pandas and numpy",
        "Learn SQL for querying and joining tables",
        "Get comfortable with Excel for quick data analysis",
        "Learn basic statistics concepts (mean, median, correlation, etc.)",
        "Learn data visualization using matplotlib or seaborn",
        "Practice by analyzing real datasets and creating dashboards"
    ],
    "AI ML Engineer": [
        "Build a strong foundation in Python, numpy, and pandas",
        "Learn data preprocessing techniques (cleaning, scaling, encoding)",
        "Learn core machine learning algorithms using scikit-learn",
        "Understand model evaluation metrics like accuracy, precision, recall",
        "Get introduced to deep learning basics (neural networks)",
        "Practice by building small ML projects end-to-end"
    ],
    "Cybersecurity Analyst": [
        "Learn networking basics (IP, DNS, ports, protocols)",
        "Get comfortable with Linux command line",
        "Learn about common security threats and how to prevent them",
        "Practice using tools like Wireshark for network analysis",
        "Learn the basics of cryptography and encryption",
        "Try beginner-friendly ethical hacking labs (legal practice platforms)"
    ]
}

project_suggestions = {
    "Full Stack Developer": "Build a personal portfolio website with a working contact form, connected to a Node.js backend and MongoDB database.",
    "Backend Developer": "Build a REST API for a simple Library Management System using Flask, with login authentication and CRUD operations on a SQL database.",
    "Data Analyst": "Take a public dataset (like sales or student performance data) and build a complete analysis with charts and a short report on the insights found.",
    "AI ML Engineer": "Build a spam email classifier using scikit-learn, with proper data preprocessing, model training, and accuracy evaluation.",
    "Cybersecurity Analyst": "Set up a small home lab and write a report on scanning a test network with Wireshark and Nmap, documenting vulnerabilities found."
}

def extract_text_from_pdf(file_stream):
    try:
        reader = PdfReader(file_stream)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return ""

def extract_text_from_docx(file_stream):
    try:
        doc = Document(file_stream)
        text = []
        for p in doc.paragraphs:
            text.append(p.text)
        return "\n".join(text)
    except Exception as e:
        print(f"Error parsing DOCX: {e}")
        return ""

def extract_skills_from_text(text):
    text_lower = text.lower()
    # clean punctuation but preserve tags like ++, #, -
    text_clean = re.sub(r'[^\w\s\+\#\-]', ' ', text_lower)
    text_clean = ' ' + text_clean + ' '
    
    extracted = set()
    
    # Match phrases first
    multi_word_skills = [
        ("machine learning", "machine learning"),
        ("deep learning", "deep learning"),
        ("data preprocessing", "data preprocessing"),
        ("incident response", "incident response"),
        ("model deployment", "model deployment"),
        ("model evaluation", "model evaluation"),
        ("computer vision", "computer vision"),
        ("threat analysis", "threat analysis"),
        ("access control", "access control"),
        ("ethical hacking", "ethical hacking"),
        ("rest framework", "rest framework"),
        ("risk assessment", "risk assessment"),
        ("feature engineering", "feature engineering"),
        ("gradient descent", "gradient descent"),
        ("intrusion detection", "intrusion detection"),
        ("malware analysis", "malware analysis"),
        ("network security", "network security"),
        ("vulnerability assessment", "vulnerability"),
        ("penetration testing", "pentesting"),
        ("rest api", "api"),
        ("rest apis", "api"),
        ("restful api", "api"),
        ("restful apis", "api"),
        ("data analysis", "data analysis"),
        ("data cleaning", "data cleaning"),
        ("ci/cd", "ci/cd"),
        ("continuous integration", "ci/cd")
    ]
    
    for phrase, skill_key in multi_word_skills:
        if phrase in text_clean:
            extracted.add(skill_key)
            text_clean = text_clean.replace(phrase, ' ')
            
    # Match single-word tokens
    single_word_skills = {
        "python": "python",
        "javascript": "javascript",
        "js": "javascript",
        "typescript": "typescript",
        "ts": "typescript",
        "html": "html",
        "css": "css",
        "sql": "sql",
        "mysql": "mysql",
        "postgresql": "postgresql",
        "postgres": "postgresql",
        "mongodb": "mongodb",
        "c++": "cpp",
        "cpp": "cpp",
        "c#": "csharp",
        "csharp": "csharp",
        "java": "java",
        "php": "php",
        "ruby": "ruby",
        "react": "react",
        "node": "node",
        "node.js": "node",
        "express": "express",
        "express.js": "express",
        "flask": "flask",
        "django": "django",
        "fastapi": "fastapi",
        "angular": "angular",
        "vue": "vue",
        "jquery": "jquery",
        "bootstrap": "bootstrap",
        "tailwind": "tailwind",
        "redux": "redux",
        "vite": "vite",
        "ejs": "ejs",
        "mongoose": "mongoose",
        "webpack": "webpack",
        "sqlalchemy": "sqlalchemy",
        "pandas": "pandas",
        "numpy": "numpy",
        "sklearn": "sklearn",
        "scikit-learn": "sklearn",
        "tensorflow": "tensorflow",
        "keras": "keras",
        "pytorch": "pytorch",
        "statistics": "statistics",
        "visualization": "visualization",
        "tableau": "tableau",
        "powerbi": "powerbi",
        "excel": "excel",
        "nlp": "nlp",
        "regression": "regression",
        "clustering": "clustering",
        "matplotlib": "matplotlib",
        "seaborn": "seaborn",
        "algorithms": "algorithms",
        "classification": "classification",
        "git": "git",
        "github": "git",
        "docker": "docker",
        "nginx": "nginx",
        "aws": "aws",
        "heroku": "heroku",
        "redis": "redis",
        "celery": "celery",
        "postman": "postman",
        "swagger": "swagger",
        "networking": "networking",
        "linux": "linux",
        "security": "security",
        "cybersecurity": "security",
        "wireshark": "wireshark",
        "cryptography": "cryptography",
        "vulnerability": "vulnerability",
        "scanning": "scanning",
        "vpn": "vpn",
        "compliance": "compliance",
        "pentesting": "pentesting",
        "firewall": "firewall",
        "soc": "soc",
        "forensics": "forensics",
        "encryption": "encryption",
        "nmap": "nmap",
        "siem": "siem",
        "api": "api",
        "apis": "api",
        "authentication": "authentication",
        "auth": "authentication",
        "microservices": "microservices",
        "jwt": "jwt",
        "oauth": "oauth"
    }
    
    for word, skill_key in single_word_skills.items():
        if '+' in word or '#' in word or '-' in word:
            if f" {word} " in text_clean:
                extracted.add(skill_key)
        else:
            pattern = r'\b' + re.escape(word) + r'\b'
            if re.search(pattern, text_clean):
                extracted.add(skill_key)
                
    return sorted(list(extracted))

@app.route("/", methods=["GET", "POST"])
def home():
    predicted_role = None
    missing_skills = None
    matched_skills = None
    path = None
    project = None
    user_input = ""
    extracted_skills = []
    match_score = 0
    error_message = None

    if request.method == "POST":
        text = ""
        # Check for uploaded file
        if "cv_file" in request.files:
            file = request.files["cv_file"]
            if file and file.filename != "":
                filename = file.filename.lower()
                if filename.endswith(".pdf") or filename.endswith(".docx") or filename.endswith(".txt"):
                    file_bytes = file.read()
                    if filename.endswith(".pdf"):
                        text = extract_text_from_pdf(io.BytesIO(file_bytes))
                    elif filename.endswith(".docx"):
                        text = extract_text_from_docx(io.BytesIO(file_bytes))
                    elif filename.endswith(".txt"):
                        text = file_bytes.decode("utf-8", errors="ignore")
                else:
                    error_message = "Invalid file type. Supported: PDF, DOCX, TXT."
        
        # Fallback to pasted text
        if not text and not error_message:
            text = request.form.get("skills", "").strip()
            user_input = text

        if text and not error_message:
            extracted_skills = extract_skills_from_text(text)
            
            if extracted_skills:
                prediction_input = " ".join(extracted_skills)
                predicted_role = model.predict([prediction_input])[0]
                
                needed = required_skills.get(predicted_role, [])
                matched_skills = [s for s in needed if s in extracted_skills]
                missing_skills = [s for s in needed if s not in extracted_skills]
                
                if needed:
                    match_score = int((len(matched_skills) / len(needed)) * 100)
                
                path = learning_path.get(predicted_role, [])
                project = project_suggestions.get(predicted_role, "")
            else:
                error_message = "Could not extract any skills from the input. Make sure technology names are typed clearly."

    return render_template(
        "index.html",
        predicted_role=predicted_role,
        missing_skills=missing_skills,
        matched_skills=matched_skills,
        extracted_skills=extracted_skills,
        match_score=match_score,
        path=path,
        project=project,
        user_input=user_input,
        error_message=error_message
    )

if __name__ == "__main__":
    app.run(debug=True)
