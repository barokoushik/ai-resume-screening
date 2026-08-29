from flask import Flask, render_template, request
from pypdf import PdfReader
import re

app = Flask(__name__)

SKILLS = [
    # Programming languages
    "python",
    "java",
    "javascript",
    "typescript",
    "c",
    "c++",
    "c#",

    # Frontend
    "html",
    "css",
    "react",
    "angular",
    "vue",
    "bootstrap",

    # Backend
    "flask",
    "django",
    "fastapi",
    "node.js",
    "express",

    # Databases
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "sqlite",

    # Development tools
    "git",
    "github",
    "docker",
    "kubernetes",

    # Cloud
    "aws",
    "azure",
    "google cloud",

    # AI / Data
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",

    # APIs
    "rest api",
    "api"
]

@app.route("/", methods=["GET", "POST"])
def home():
    resume_text = None
    error = None

    match_score = None
    matched_skills = []
    missing_skills = []
    recommendation = None
    explanation = None

    if request.method == "POST":
        resume = request.files.get("resume")
        job_description = request.form.get("job_description", "").lower()

        if not resume or resume.filename == "":
            error = "Please select a PDF resume."

        elif not resume.filename.lower().endswith(".pdf"):
            error = "Only PDF files are supported."

        elif not job_description.strip():
            error = "Please enter a job description."

        else:
            try:
                reader = PdfReader(resume)

                extracted_pages = []

                for page in reader.pages:
                    text = page.extract_text()

                    if text:
                        extracted_pages.append(text)

                resume_text = "\n".join(extracted_pages)

                if not resume_text.strip():
                    error = "No readable text was found in this PDF."

                else:
                    resume_lower = resume_text.lower()

                    def contains_skill(text, skill):
                        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"
                        return re.search(pattern, text, re.IGNORECASE) is not None
                    required_skills = [
                        skill
                        for skill in SKILLS
                        if contains_skill(job_description, skill)
                    ]    
                    
                    # Avoid counting generic API separately when REST API is present
                    if "rest api" in required_skills and "api" in required_skills:
                        required_skills.remover("api")

                    matched_skills = [
                        skill
                        for skill in required_skills
                        if contains_skill(resume_lower, skill)
                    ]

                    missing_skills = [
                        skill
                        for skill in required_skills
                        if not contains_skill(resume_lower, skill)
                    ]

                    if required_skills:
                        match_score = round(
                            (len(matched_skills) / len(required_skills)) * 100
                        )
                    else:
                        match_score = 0
                    if match_score >= 80:
                        recommendation = "Strong Match"
                    elif match_score >= 60:
                        recommendation = "Good Match"
                    elif match_score >= 40:
                        recommendation = "Moderate Match"
                    else:
                        recommendation = "Low Match"

                    if matched_skills and missing_skills:
                        explanation = (
                            f"The candidate matches {len(matched_skills)} required skills "
                            f"but is missing {len(missing_skills)} required skills."
                        )
                    elif matched_skills:
                        explanation = "The candidate matches all detected required skills."
                    else:
                        explanation = "The candidate does not match the detected required skills."
            except Exception as e:
                print("Processing error:", e)
                error = "Could not read this PDF. Please try another file."

    return render_template(
    "index.html",
    resume_text=resume_text,
    error=error,
    match_score=match_score,
    matched_skills=matched_skills,
    missing_skills=missing_skills,
    recommendation=recommendation,
    explanation=explanation
)


if __name__ == "__main__":
    app.run(debug=True)