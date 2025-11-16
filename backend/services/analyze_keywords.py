import re

# Hard filter: Only allow real technical or job-relevant terms.
ALLOWED_KEYWORDS = {
    "python","java","c","c++","javascript","typescript","node","react","nextjs","angular",
    "mongodb","mysql","postgres","sql","docker","kubernetes","aws","azure","gcp",
    "rest","api","apis","microservices","devops","ci","cd","ml","ai","tensorflow",
    "pytorch","nlp","redis","rabbitmq","linux","cloud","git","github","fastapi",
    "flask","django","fullstack","backend","frontend","data","database","algorithms",
    "system","architecture","scalability","performance","security","analytics",
    "testing","automation","debugging","infrastructure","pipelines","etl"
}

# Allow custom extraction
def tokenize(text: str):
    text = text.lower()
    return re.findall(r"[a-zA-Z0-9+.#]+", text)

def analyze_keywords(resume_text: str, job_description: str):
    resume_tokens = tokenize(resume_text)
    jd_tokens = tokenize(job_description)

    # filter tokens to keep only relevant technical ones
    resume_keywords = {t for t in resume_tokens if t in ALLOWED_KEYWORDS}
    jd_keywords = {t for t in jd_tokens if t in ALLOWED_KEYWORDS}

    matched = sorted(resume_keywords.intersection(jd_keywords))
    missing = sorted(jd_keywords - resume_keywords)

    # Limit list sizes (no keyword dump)
    matched = matched[:30]
    missing = missing[:30]

    # scoring
    if len(jd_keywords) == 0:
        score = 0
    else:
        score = round((len(matched) / len(jd_keywords)) * 100, 2)

    return {
        "matched": matched,
        "missing": missing,
        "keyword_score": score,
        "total_relevant_keywords": len(jd_keywords),
    }
