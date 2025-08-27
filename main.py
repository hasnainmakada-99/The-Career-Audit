# Import the functions we created in our other files
from parser import parse_resume
from analyzer import analyze_resume

# --- CONFIGURATION ---
# Specify the path to the resume file
RESUME_FILE_PATH = "sample_resume.pdf" # Make sure this file exists!

# Paste the full job description you want to analyze against
JOB_DESCRIPTION_TEXT = """
We are hiring a Senior Flutter Developer to join our innovative team.
The ideal candidate will have strong experience with Dart, Flutter, and Firebase.
Knowledge of DevOps practices, including Docker and Git, is a huge plus.
Experience with Python and NodeJS is also desirable for backend tasks.
Must be proficient in English.
"""
# --- END CONFIGURATION ---

def main():
    """
    The main function to run the full resume analysis process.
    """
    print("🚀 Starting Resume Analysis...")

    # Step 1: Parse the resume file to get its text content
    print(f"Parsing resume: '{RESUME_FILE_PATH}'")
    resume_text = parse_resume(RESUME_FILE_PATH)
    
    # Error handling: Check if the parser returned an error message
    if "Error:" in resume_text:
        print(resume_text) # Print the error and stop
        return

    print("Resume parsed successfully.")

    # Step 2: Analyze the extracted resume text against the job description
    print("Analyzing text against job description...")
    analysis_result = analyze_resume(resume_text, JOB_DESCRIPTION_TEXT)

    # Step 3: Display the final results in a clean format
    print("\n" + "="*40)
    print("         RESUME ANALYSIS COMPLETE")
    print("="*40 + "\n")

    print(f"✅ {len(analysis_result['found'])} Keywords Found in Your Resume:")
    # Print found keywords, 5 per line for readability
    for i in range(0, len(analysis_result['found']), 5):
        print("  - " + ", ".join(analysis_result['found'][i:i+5]))
        
    print("\n" + "-"*40 + "\n")

    print(f"❌ {len(analysis_result['missing'])} Keywords Missing From Your Resume:")
    # Print missing keywords, 5 per line for readability
    for i in range(0, len(analysis_result['missing']), 5):
        print("  - " + ", ".join(analysis_result['missing'][i:i+5]))

    print("\n" + "="*40)


if __name__ == '__main__':
    main()