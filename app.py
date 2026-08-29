from flask import Flask, render_template, request
from pypdf import PdfReader

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    resume_text = None
    error = None

    if request.method == "POST":
        resume = request.files.get("resume")

        if not resume or resume.filename == "":
            error = "Please select a PDF resume."
        elif not resume.filename.lower().endswith(".pdf"):
            error = "Only PDF files are supported."
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

            except Exception:
                error = "Could not read this PDF. Please try another file."

    return render_template(
        "index.html",
        resume_text=resume_text,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)