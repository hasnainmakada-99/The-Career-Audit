# in api.py

import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# Import our custom functions
from parser import parse_resume
from analyzer import analyze_resume
from resume_checker import check_resume_quality  # <-- NEW IMPORT

# Initialize the FastAPI app
app = FastAPI()

# ... (CORS middleware and TEMP_DIR setup remain the same) ...
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
TEMP_DIR = "temp_resumes"
os.makedirs(TEMP_DIR, exist_ok=True)


# --- Endpoint for Job Description Matching (No changes here) ---
@app.post("/analyze/")
async def analyze_resume_endpoint(
    job_description: str = Form(...), 
    resume_file: UploadFile = File(...)
):
    # ... (this function's code remains the same) ...
    file_path = os.path.join(TEMP_DIR, resume_file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(resume_file.file, buffer)
    resume_text = parse_resume(file_path)
    if "Error:" in resume_text:
        return {"error": resume_text}
    analysis = analyze_resume(resume_text, job_description)
    os.remove(file_path)
    return analysis


# --- NEW ENDPOINT for General Resume Quality Check ---
@app.post("/check-resume/")
async def check_resume_endpoint(resume_file: UploadFile = File(...)):
    """
    This endpoint receives only a resume file, scores its overall
    quality, and returns a detailed breakdown.
    """
    # Save and parse the file (same as before)
    file_path = os.path.join(TEMP_DIR, resume_file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(resume_file.file, buffer)

    resume_text = parse_resume(file_path)
    if "Error:" in resume_text:
        return {"error": resume_text}

    # Call our new quality checker function
    quality_report = check_resume_quality(resume_text)

    # Clean up the temporary file
    os.remove(file_path)

    # Return the final report
    return quality_report


# --- Serve the Frontend (No changes here) ---
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/")
async def read_index():
    return FileResponse('static/index.html')


# --- ADD THIS NEW ENDPOINT ---
@app.get("/health-check")
async def read_health_check():
    """Serves the health check HTML page."""
    return FileResponse('static/health_check.html')