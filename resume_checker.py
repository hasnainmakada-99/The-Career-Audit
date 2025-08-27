# in resume_checker.py
import re
from spellchecker import SpellChecker

# ... (ACTION_VERBS and BUZZWORDS lists are unchanged) ...
ACTION_VERBS = {'created', 'developed', 'led', 'managed', 'optimized', 'streamlined', 'implemented', 'architected', 'designed', 'engineered', 'built', 'launched', 'drove', 'increased', 'decreased', 'reduced', 'grew', 'improved', 'achieved', 'negotiated', 'mentored', 'authored', 'budgeted', 'consulted', 'directed', 'facilitated', 'founded', 'governed', 'headed', 'hired', 'hosted', 'initiated', 'inspired', 'instituted', 'instructed', 'interviewed', 'judged', 'lectured', 'lobbied', 'mediated', 'moderated', 'motivated', 'navigated', 'organized', 'oversaw', 'pioneered', 'presided', 'produced', 'programmed', 'promoted', 'publicized', 'recruited', 'regulated', 'retained', 'revamped', 'revitalized', 'saved', 'scheduled', 'secured', 'selected', 'supervised', 'taught', 'trained', 'unified', 'united', 'updated', 'upgraded', 'validated', 'verified', 'won', 'wrote'}
BUZZWORDS = {'synergy', 'go-getter', 'results-driven', 'team player', 'hard worker', 'proactive', 'self-starter', 'detail-oriented', 'think outside the box'}

# --- NEW V3 FEATURE: Spelling Check ---
def score_spelling(text):
    """Scores based on spelling errors, ignoring common tech words."""
    spell = SpellChecker()
    
    # Add common tech/resume words to a custom dictionary to avoid false positives
    known_words = [
        'python', 'javascript', 'java', 'react', 'nodejs', 'aws', 'gcp', 'azure',
        'docker', 'kubernetes', 'terraform', 'ansible', 'jenkins', 'git', 'github',
        'sql', 'nosql', 'mongodb', 'postgresql', 'api', 'apis', 'restful',
        'graphql', 'html', 'css', 'spacy', 'pytesseract', 'fastapi', 'uvicorn',
        'tech', 'devops', 'backend', 'frontend', 'agile', 'scrum', 'ceo', 'cto'
    ]
    spell.word_frequency.load_words(known_words)

    # Find all words in the resume
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Find unknown words
    misspelled = spell.unknown(words)
    
    error_count = len(misspelled)
    
    score = 0
    if error_count == 0:
        score = 15
        feedback = "Excellent! No spelling errors were found."
    elif error_count <= 2:
        score = 10
        feedback = f"Found {error_count} potential spelling error(s). Please review: {', '.join(list(misspelled)[:2])}."
    elif error_count <= 5:
        score = 5
        feedback = f"Found {error_count} potential spelling errors. Please proofread carefully."
    else:
        score = 0
        feedback = f"Found over 5 potential spelling errors. It's highly recommended to proofread your resume."
        
    return score, feedback

def score_quantification(text):
    # Re-balanced to 25 pts
    count = len(re.findall(r'(\d+|%|\$)', text))
    if count >= 8: return 25, f"Excellent! You've used {count} quantifiable metrics."
    elif count >= 4: return 15, f"Good job using {count} metrics. Aim for more."
    elif count >= 1: return 8, f"A good start with {count} metric(s). Add more numbers."
    return 0, "Try to add quantifiable results (e.g., 'Increased sales by 20%')."

def score_action_verbs(text):
    found_verbs = {word for word in text.lower().split() if word in ACTION_VERBS}
    count = len(found_verbs)
    score = 0
    if count >= 15: score = 20
    elif count >= 10: score = 15
    elif count >= 5: score = 10
    else: score = 0
    feedback = f"You used {count} strong action verbs. Keep it up!" if count > 0 else "Start bullet points with strong action verbs like 'Managed' or 'Developed'."
    return score, list(found_verbs), feedback

def score_readability(text):
    word_count = len(text.split())
    if 400 <= word_count <= 700: return 15, f"Word count of {word_count} is in the ideal range."
    elif 250 <= word_count < 400 or 700 < word_count <= 850: return 8, f"Word count of {word_count} is a bit short/long."
    return 0, f"Word count of {word_count} is outside the recommended range."

def score_sections(text):
    # Re-balanced to 10 pts
    score = 0; found_sections = []
    text_lower = text.lower()
    if re.search(r'(experience|employment|history)', text_lower): score += 4; found_sections.append("Experience")
    if re.search(r'(education|academic)', text_lower): score += 3; found_sections.append("Education")
    if re.search(r'(skills|abilities)', text_lower): score += 3; found_sections.append("Skills")
    feedback = f"Great! You have these essential sections: {', '.join(found_sections)}." if score > 0 else "Consider adding standard sections like 'Experience', 'Education', and 'Skills'."
    return score, feedback

def score_buzzwords(text):
    # Re-balanced to 5 pts
    found_buzzwords = {word for word in text.lower().split() if word in BUZZWORDS}
    score = max(5 - len(found_buzzwords), 0)
    feedback = "Excellent! No common buzzwords found." if len(found_buzzwords) == 0 else f"Consider replacing buzzwords like '{', '.join(found_buzzwords)}'."
    return score, feedback

def score_contact_info(text):
    score = 0
    feedback_items = []
    if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text): score += 5; feedback_items.append("Email found")
    else: feedback_items.append("Email not found")
    if re.search(r'(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}', text): score += 5; feedback_items.append("Phone number found")
    else: feedback_items.append("Phone number not found")
    feedback = " | ".join(feedback_items) + "."
    if score == 10: feedback = "Excellent! Contact information is present."
    return score, feedback

def check_resume_quality(resume_text):
    action_score, found_verbs, action_feedback = score_action_verbs(resume_text)
    
    scores = {
        "impact_and_quantification": score_quantification(resume_text),
        "action_verbs": (action_score, action_feedback),
        "readability": score_readability(resume_text),
        "essential_sections": score_sections(resume_text),
        "clarity_and_brevity": score_buzzwords(resume_text),
        "contact_information": score_contact_info(resume_text),
        "spelling": score_spelling(resume_text)
    }
    
    total_score = sum(score for score, feedback in scores.values())
    
    return {
        "total_score": total_score,
        "details": {key: value for key, (value, feedback) in scores.items()},
        "feedback": {key: feedback for key, (value, feedback) in scores.items()},
        "found_action_verbs": sorted(found_verbs)
    }