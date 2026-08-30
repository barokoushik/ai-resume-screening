# HireLens AI

HireLens AI is an explainable resume-screening web application that helps compare multiple candidates against job requirements and rank them based on relevant skills.

## 🎯 Problem

Manually reviewing multiple resumes can be repetitive and time-consuming. Recruiters need a simple way to identify candidates whose skills align with the requirements of a job.

HireLens AI helps organize this process by extracting information from PDF resumes, comparing detected skills with the job description, and presenting clear candidate rankings.

## ✨ Features

- Upload multiple PDF resumes
- Enter job requirements
- Detect relevant technical skills
- Weighted skill-based match scoring
- Automatic candidate ranking
- Shortlisted, Review, and Not Shortlisted status
- Candidate strengths and skill gaps
- Matched and missing skill explanations
- Experience overview extraction
- Explainable screening results
- Candidate status filters
- Glass, Light, and Dark result themes
- Responsive navigation
- Dedicated How It Works and About pages

## ⚙️ How It Works

1. Enter the job description.
2. Upload one or multiple PDF resumes.
3. HireLens detects supported skills from the job description.
4. Each resume is checked for those required skills.
5. Weighted skill matching is used to calculate a match score.
6. Candidates are ranked from highest to lowest score.
7. Results display strengths, skill gaps, experience information, and shortlist status.

## 🧠 Screening Approach

HireLens AI uses explainable weighted skill matching.

Skills detected in the job description become the requirements used during screening. Different supported skills can have different weights, and each candidate's score is calculated according to the required skills found in their resume.

This approach keeps the screening result transparent because users can see which skills matched and which skills are missing.

## 🛠️ Tech Stack

- Python
- Flask
- HTML
- CSS
- JavaScript
- PyPDF
- Regular Expressions (Regex)

## 📁 Project Structure

```text
ai-resume-screening/
├── static/
│   └── style.css
├── templates/
│   ├── index.html
│   ├── how_it_works.html
│   └── about.html
├── app.py
├── requirements.txt
├── .gitignore
└── README.md