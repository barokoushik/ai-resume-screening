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

SKILL_WEIGHTS = {
    "python": 3,
    "java": 3,
    "javascript": 3,
    "typescript": 3,
    "c": 3,
    "c++": 3,
    "c#": 3,

    "flask": 3,
    "django": 3,
    "fastapi": 3,
    "react": 3,
    "angular": 3,
    "vue": 3,
    "node.js": 3,
    "express": 3,

    "sql": 2,
    "mysql": 2,
    "postgresql": 2,
    "mongodb": 2,
    "sqlite": 2,

    "machine learning": 3,
    "deep learning": 3,
    "tensorflow": 3,
    "pytorch": 3,
    "scikit-learn": 3,

    "aws": 2,
    "azure": 2,
    "google cloud": 2,
    "docker": 2,
    "kubernetes": 2,

    "html": 1,
    "css": 1,
    "bootstrap": 1,
    "git": 1,
    "github": 1,
    "api": 2,
    "rest api": 2,
    "pandas": 2,
    "numpy": 2,
    "artificial intelligence": 3
}

@app.route("/", methods=["GET", "POST"])
def home():
    resume_text = None
    error = None

    match_score = None
    matched_skills = []
    missing_skills = []
    recommendation = None
    explanation = None
    strengths = []
    skill_gaps = []
    candidate_results = []

    if request.method == "POST":
        resumes = request.files.getlist("resumes")
        job_description = request.form.get("job_description", "").lower()

        if not resumes or all(resume.filename == "" for resume in resumes):
            error = "Please select at least one PDF resume."

        elif any(
            resume.filename and not resume.filename.lower().endswith(".pdf")
            for resume in resumes
        ):
            error = "Only PDF files are supported."

        elif not job_description.strip():
            error = "Please enter a job description."

        else:
            try:
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
                    required_skills.remove("api")

                for resume in resumes:
                    reader = PdfReader(resume)

                    extracted_pages = []

                    for page in reader.pages:
                        text = page.extract_text()

                        if text:
                            extracted_pages.append(text)

                    resume_text = "\n".join(extracted_pages)

                    if not resume_text.strip():
                        continue

                    resume_lower = resume_text.lower()

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
                        total_weight = sum(
                            SKILL_WEIGHTS.get(skill, 1)
                            for skill in required_skills
                        )

                        matched_weight = sum(
                            SKILL_WEIGHTS.get(skill, 1)
                            for skill in matched_skills
                        )

                        match_score = round(
                            (matched_weight / total_weight) * 100
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
                        explanation = (
                            "The candidate matches all detected required skills."
                        )
                    else:
                        explanation = (
                            "The candidate does not match the detected required skills."
                        )

                    strengths = matched_skills[:5]
                    skill_gaps = missing_skills[:5]

                    candidate_results.append({
                        "filename": resume.filename,
                        "match_score": match_score,
                        "recommendation": recommendation,
                        "matched_skills": matched_skills,
                        "missing_skills": missing_skills,
                        "strengths": strengths,
                        "skill_gaps": skill_gaps,
                        "explanation": explanation
                    })

                candidate_results.sort(
                    key=lambda candidate: candidate["match_score"],
                    reverse=True
                )

                if not candidate_results:
                    error = "No readable text was found in the uploaded PDFs."

            except Exception as e:
                print("Processing error:", e)
                error = "Could not process the uploaded resumes."

    return render_template(
        "index.html",
        resume_text=resume_text,
        error=error,
        match_score=match_score,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        recommendation=recommendation,
        explanation=explanation,
        strengths=strengths,
        skill_gaps=skill_gaps,
        candidate_results=candidate_results
    )


if __name__ == "__main__":
    app.run(debug=True)