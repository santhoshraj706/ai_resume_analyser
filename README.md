# AI Resume Analyzer & Skill Gap Recommender

A machine learning web application that analyzes a student's resume or skill set, predicts the most suitable tech career role, and generates a personalized skill gap report with a learning roadmap.

Built using **Python Flask** and **scikit-learn** as a college placement preparation project.

---

## What It Does

- **Upload your CV** (PDF, DOCX, or TXT) or paste your skills directly
- **Predicts your best-fit role** from: Full Stack Developer, Backend Developer, Data Analyst, AI ML Engineer, Cybersecurity Analyst
- **Shows your Skill Match Score** — how close you are to the ideal candidate profile
- **Lists missing skills** you still need to learn for that role
- **Gives a step-by-step learning roadmap** to bridge the gap
- **Suggests a portfolio project** idea tailored to the predicted role

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Machine Learning | scikit-learn (TF-IDF + Logistic Regression) |
| CV Parsing | pypdf, python-docx |
| Frontend | HTML, CSS (Vanilla) |
| Dataset | Custom CSV — 500 labeled skill samples |
| Model Storage | Pickle (model.pkl) |

---

## Project Structure

```
ai-resume-skill-gap-analyzer/
├── app.py                  # Flask routes, CV parsing, skill extraction, prediction
├── train_model.py          # Trains and saves the ML model
├── skills_dataset.csv      # Training data (skills → role)
├── model.pkl               # Saved trained pipeline (auto-generated)
├── requirements.txt        # Python dependencies
├── test_cv.txt             # Sample resume for testing
├── templates/
│   └── index.html          # Main UI page
├── static/
│   └── style.css           # Styling
└── README.md
```

---

## How to Run

**1. Clone the repo and install dependencies:**
```bash
git clone https://github.com/your-username/ai-resume-skill-gap-analyzer.git
cd ai-resume-skill-gap-analyzer
pip install -r requirements.txt
```

**2. Train the ML model:**
```bash
python train_model.py
```

**3. Start the app:**
```bash
python app.py
```

**4. Open in browser:**
```
http://127.0.0.1:5000
```

---

## How the ML Works

The core task is **text classification**:

- **Input:** skill keywords extracted from your resume (e.g. `python flask sql git`)
- **Output:** predicted career role (e.g. `Backend Developer`)

### Training pipeline (`train_model.py`):
1. Load `skills_dataset.csv` — 500 rows of skill strings labeled with roles
2. Split into train/test sets
3. Use `TfidfVectorizer` to convert skill text into numeric feature vectors
4. Train `LogisticRegression` to learn which skill patterns map to which roles
5. Package both into a single `Pipeline` and save as `model.pkl`

### Why TF-IDF?
Skills like `python` appear in almost every role, so they get a lower weight. Skills like `wireshark` appear almost exclusively in Cybersecurity rows, making them strong signals. TF-IDF captures this automatically without any manual feature engineering.

### Why Logistic Regression?
Fast, interpretable, and performs very well on small text classification datasets. Easy to explain in interviews and viva. No deep learning needed for a 5-class problem with clean features.

---

## Skill Gap Logic (Non-ML)

After predicting the role, the skill gap is calculated using plain Python:

1. Each role has a predefined list of core required skills in `app.py`
2. The skills extracted from your CV are compared against that list
3. Missing skills = required skills not found in your resume
4. Match Score = `(matched / total required) × 100`

This part is intentionally non-ML — it's transparent, predictable, and easy to explain.

---

## CV Parsing

| File Type | Library Used |
|---|---|
| `.pdf` | `pypdf` — extracts text page by page |
| `.docx` | `python-docx` — reads paragraph text |
| `.txt` | Built-in Python file reading |

Skill extraction uses regex word-boundary matching to correctly identify both single-word skills (`python`, `docker`) and multi-word phrases (`machine learning`, `deep learning`).

---

## Future Improvements

- Add more roles (DevOps, Cloud Engineer, Mobile Developer, etc.)
- Use a larger, real-world resume dataset for training
- Compare models — Random Forest, SVM vs Logistic Regression
- Add per-skill resource links (courses, docs, YouTube)
- Store user history in a database for progress tracking
- Add user login so students can save and revisit reports

---

## Interview Explanation

> "This project takes a student's resume as input, extracts skill keywords using regex, converts them into TF-IDF vectors, and passes them through a Logistic Regression classifier trained on 500 labeled samples to predict the closest matching career role. The skill gap is then calculated by comparing the extracted skills against a predefined required skill list for that role using set operations. The full ML pipeline is saved as a pickle file so Flask can load it and predict instantly without retraining."
