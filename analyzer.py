# in analyzer.py
import spacy
from resume_checker import score_action_verbs

nlp = spacy.load("en_core_web_sm")

MANDATORY_TRIGGERS = {"required", "must have", "essential", "core requirement"}
BONUS_TRIGGERS = {"nice to have", "plus", "bonus", "preferred", "desirable"}
WEIGHTS = {"mandatory": 3, "normal": 2, "bonus": 1}
SKILL_DB = {
    'react.js': 'React', 'reactjs': 'React', 'node.js': 'Node.js', 'nodejs': 'Node.js',
    'aws': 'Amazon Web Services', 'gcp': 'Google Cloud Platform', 'html5': 'HTML',
    'css3': 'CSS', 'js': 'JavaScript', 'mongo': 'MongoDB', 'postgress': 'PostgreSQL',
    'sql': 'SQL', 'docker': 'Docker', 'k8s': 'Kubernetes', 'ci/cd': 'CI/CD',
    'ci / cd': 'CI/CD', 'dev ops': 'DevOps', 'quality assurance': 'QA', 'qa': 'QA',
    'machine learning': 'Machine Learning', 'ml': 'Machine Learning', 'software engineering': 'Software Engineering'
}
STOP_WORDS = {
    "a", "an", "the", "in", "on", "for", "of", "with", "to", "and", "or", "but",
    "experience", "team", "candidate", "knowledge", "skills", "skill", "plus",
    "ideal", "strong", "tasks", "duties", "responsibilities", "requirements",
    "proficient", "join", "work", "innovative", "senior", "developer", "our",
    "role", "you", "we"
}

def normalize_skills(keywords):
    normalized = set()
    for keyword in keywords:
        cleaned_keyword = keyword.lower().strip()
        if cleaned_keyword in SKILL_DB:
            normalized.add(SKILL_DB[cleaned_keyword])
        else:
            normalized.add(keyword)
    return list(normalized)

def extract_keywords_from_jd(job_description_text):
    doc = nlp(job_description_text.lower())
    categorized_keywords = {"mandatory": set(), "bonus": set(), "normal": set()}
    for sentence in doc.sents:
        sentence_text = sentence.text
        category = "normal"
        if any(trigger in sentence_text for trigger in MANDATORY_TRIGGERS):
            category = "mandatory"
        elif any(trigger in sentence_text for trigger in BONUS_TRIGGERS):
            category = "bonus"
        raw_keywords = set()
        for token in sentence:
            if token.pos_ in ["PROPN", "NOUN"]:
                raw_keywords.add(token.text)
        for chunk in sentence.noun_chunks:
            cleaned_chunk = " ".join(token.text for token in chunk if token.text not in STOP_WORDS)
            if cleaned_chunk:
                raw_keywords.add(cleaned_chunk)
        for keyword in raw_keywords:
            categorized_keywords[category].add(keyword)
    final_categorized = {}
    for category, keywords in categorized_keywords.items():
        filtered_keywords = {kw for kw in keywords if kw not in STOP_WORDS and len(kw) > 1}
        final_categorized[category] = normalize_skills(filtered_keywords)
    return final_categorized

def analyze_resume(resume_text, job_description_text):
    jd_keywords_categorized = extract_keywords_from_jd(job_description_text)
    resume_text_lower = resume_text.lower()
    found_keywords, missing_keywords = [], []
    user_score, total_possible_score = 0, 0
    
    for category, keywords in jd_keywords_categorized.items():
        weight = WEIGHTS.get(category, 1)
        total_possible_score += len(keywords) * weight
        for keyword in keywords:
            if keyword.lower() in resume_text_lower:
                found_keywords.append(keyword)
                user_score += weight
            else:
                missing_keywords.append(keyword)

    final_score = round((user_score / total_possible_score) * 100) if total_possible_score > 0 else 0
    
    _, found_verbs_list = score_action_verbs(resume_text)
            
    return {
        "found": found_keywords,
        "missing": missing_keywords,
        "score": final_score,
        "found_action_verbs": sorted(found_verbs_list)
    }