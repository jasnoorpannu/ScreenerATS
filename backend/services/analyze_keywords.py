import re
from collections import Counter

# Common action verbs & tech skills to auto-detect
ACTION_VERBS = [
    "developed", "designed", "built", "implemented", "led", "optimized",
    "created", "managed", "debugged", "configured", "analyzed"
]

TECH_WORDS = [
    "python", "c++", "java", "fastapi", "react", "machine learning",
    "tensorflow", "pytorch", "sql", "docker", "rest", "api", 
    "aws", "azure", "git", "linux", "postgres"
]

def clean_text(t: str) -> str:
    t = t.lower()
    t = re.sub(r"[^a-z0-9+.# ]", " ", t)
    return re.sub(r"\s+", " ", t).strip()

def extract_keywords(job_description: str) -> list:
    text = clean_text(job_description)

    # Extract words that look meaningful (2+ chars)
    raw_words = [w for w in text.split() if len(w) > 2]

    # Remove stopwords
    stopwords = {"and", "the", "with", "for", "you", "are", "your", "this"}
    filtered = [w for w in raw_words if w not in stopwords]

    return list(set(filtered + ACTION_VERBS + TECH_WORDS))

def analyze_keywords(resume_text: str, job_description: str) -> dict:
    if resume_text.startswith("[ERROR]"):
        return {
            "matched": [],
            "missing": [],
            "score": 0,
            "error": resume_text
        }

    resume = clean_text(resume_text)
    jd_keywords = extract_keywords(job_description)

    matched = []
    missing = []

    for kw in jd_keywords:
        if kw.lower() in resume:
            matched.append(kw)
        else:
            missing.append(kw)

    # Simple frequency scoring
    resume_words = resume.split()
    counts = Counter(resume_words)

    keyword_frequency = {kw: counts.get(kw.lower(), 0) for kw in matched}

    keyword_score = round((len(matched) / len(jd_keywords)) * 100, 2) if jd_keywords else 0

    return {
        "matched": matched,
        "missing": missing,
        "frequency": keyword_frequency,
        "keyword_score": keyword_score
    }
