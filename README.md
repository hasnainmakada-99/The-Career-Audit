# The Career Audit 🩺

> An AI-powered, dual-engine web application designed to help job seekers optimize their resumes, pass through Applicant Tracking Systems (ATS), and land their dream job.

This tool provides a comprehensive analysis of a resume's quality and its alignment with a specific job description, offering actionable feedback to give applicants a competitive edge.



---
## Key Features 🎯

"The Career Audit" is built with two distinct analysis engines:

### 1. ATS Match Scorer
Analyzes a resume against a specific job description to predict its performance in a real-world Applicant Tracking System.
* **Weighted Scoring:** Intelligently gives more importance to skills listed as "required" or "must-have" in the job description.
* **Skill Normalization:** Understands that variations like "React.js," "ReactJS," and "React framework" all refer to the same core skill ("React").
* **Language Quality Analysis:** Provides feedback on the use of strong, achievement-oriented action verbs within the resume.

### 2. Resume Health Check
Provides an overall quality score out of 100 based on universal best practices, without needing a job description. The score is broken down into seven key categories:
* **Impact & Quantification:** Checks for the use of numbers, percentages, and metrics to showcase achievements.
* **Action Verbs:** Rewards the use of strong, active language.
* **Spelling & Grammar:** Identifies potential spelling errors, with a built-in dictionary for common tech terms to avoid false positives.
* **Readability:** Analyzes the word count to ensure the resume is concise and effective.
* **Essential Sections:** Verifies the presence of critical sections like "Experience," "Education," and "Skills."
* **Contact Information:** Checks for a valid email and phone number.
* **Clarity & Brevity:** Penalizes the use of vague clichés and buzzwords.

### Robust Parsing Engine
* **Multi-Format Support:** Accepts `.pdf`, `.docx`, and image files (`.png`, `.jpg`).
* **OCR Integration:** Utilizes the Tesseract OCR engine to read and analyze text from scanned PDFs and image-based resumes.

---
## Tech Stack 🛠️

* **Backend:** Python, FastAPI, Uvicorn
* **NLP & Analysis:** spaCy, Pytesseract, `pyspellchecker`
* **Frontend:** HTML5, CSS3, Vanilla JavaScript (with Fetch API)

---
## Local Setup & Installation

To run this project locally, follow these steps:

1.  **Prerequisites:**
    * Python 3.10+
    * pip package manager
    * **Tesseract-OCR Engine:** You must install Tesseract on your system. Follow the official installation guide for your OS ([Windows](https://github.com/UB-Mannheim/tesseract/wiki), [macOS/Linux](https://tesseract-ocr.github.io/tessdoc/Installation.html)).

2.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd the-career-audit
    ```

3.  **Create a Virtual Environment:**
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  **Install Dependencies:**
    First, create the `requirements.txt` file if you haven't already: `pip freeze > requirements.txt`. Then, install the packages:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Download spaCy Model:**
    ```bash
    python -m spacy download en_core_web_sm
    ```

6.  **Configure Tesseract Path:**
    * Open the `parser.py` file.
    * Find the line `pytesseract.pytesseract.tesseract_cmd = r'...'`.
    * Uncomment it and ensure the path points to your Tesseract installation location.

7.  **Run the Application:**
    Use the custom run script to start the server:
    ```bash
    python run.py
    ```
    The application will be available at `http://1227.0.0.1:8000`.

---
## Future Improvements (Roadmap) 🗺️

This project is a strong foundation with exciting potential for future upgrades, including:

* **V4 - Section-Specific Analysis:** Re-architecting the Health Check to provide feedback on a section-by-section basis.
* **Semantic Matching:** Upgrading the ATS Match Scorer with a `sentence-transformers` model to understand the conceptual meaning of sentences, not just keywords.
* **Deployment:** Launching the application on a cloud platform like Render or Heroku.

---
## License

This project is licensed under the MIT License.