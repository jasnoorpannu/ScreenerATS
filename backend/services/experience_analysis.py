import re
from collections import Counter

SENIORITY_LEVELS = {
    "intern": 0,
    "internship": 0,
    "junior": 1,
    "jr": 1,
    "associate": 1,
    "mid": 2,
    "mid-level": 2,
    "senior": 3,
    "sr": 3,
    "lead": 4,
    "principal": 5,
    "manager": 5,
    "head": 5
}

LEADERSHIP_VERBS = [
    "led","managed","supervised","mentored","directed","owned",
    "headed","coordinated","orchestrated","oversaw","spearheaded"
]

STOPWORDS = {
    "and","the","for","with","you","are","your","this","that","from","have","has",
    "was","were","will","would","should","can","may","a","an","in","on","of","to",
    "by","as","at","is","it","be","or"
}

def _normalize(t):
    return re.sub(r"\s+", " ", re.sub(r"[^a-zA-Z0-9\-\–\—\+ ]", " ", t.lower())).strip()

def _extract_year_ranges(t):
    r = re.findall(r"(\b20\d{2})\s*[-–—]\s*(\b20\d{2})", t)
    out = []
    for a,b in r:
        try:
            a,b = int(a), int(b)
            if b >= a:
                out.append((a,b))
        except:
            pass
    return out

def _extract_year_counts(t):
    r = re.findall(r"(\d+)\s*\+?\s*(?:years|yrs|year|y)", t)
    return [int(x) for x in r if x.isdigit()]

def estimate_years_experience(t):
    x = _normalize(t)
    ranges = _extract_year_ranges(x)
    total = 0
    if ranges:
        merged = []
        ranges.sort()
        s,e = ranges[0]
        for a,b in ranges[1:]:
            if a <= e+1:
                e = max(e,b)
            else:
                merged.append((s,e))
                s,e = a,b
        merged.append((s,e))
        total = sum(e-s+1 for s,e in merged)
    explicit = _extract_year_counts(x)
    return max(total, max(explicit) if explicit else 0)

def _infer_seniority_level(t):
    x = _normalize(t)
    lvl = 2
    for token,val in SENIORITY_LEVELS.items():
        if re.search(r"\b"+re.escape(token)+r"\b", x):
            if val > lvl:
                lvl = val
    return lvl

def _count_leadership(t):
    x = _normalize(t)
    c = 0
    for v in LEADERSHIP_VERBS:
        c += len(re.findall(r"\b"+re.escape(v)+r"\b", x))
    return c

def _extract_keyword_set(t, n=40):
    x = _normalize(t)
    words = [w for w in re.findall(r"\b[a-z0-9+\-\.]{2,}\b", x) if w not in STOPWORDS]
    ctr = Counter(words)
    return set([w for w,_ in ctr.most_common(n)])

def _domain_overlap(resume, jd):
    a = _extract_keyword_set(resume,80)
    b = _extract_keyword_set(jd,80)
    if not b:
        return 0.0
    return round((len(a.intersection(b))/len(b))*100,2)

def analyze_experience(resume_text, job_description):
    years = estimate_years_experience(resume_text)
    rl = _infer_seniority_level(resume_text)
    jl = _infer_seniority_level(job_description)
    match = rl >= jl
    lead = _count_leadership(resume_text)
    dom = _domain_overlap(resume_text, job_description)
    yscore = min(years/10*40,40)
    lscore = min(lead,5)/5*15
    dscore = dom/100*15
    sscore = 30 if match else max(0, 30 - (jl-rl)*10)
    total = round(min(max(yscore + lscore + dscore + sscore, 0), 100), 2)
    return {
        "years_experience": years,
        "resume_seniority_level": rl,
        "jd_seniority_level": jl,
        "seniority_match": match,
        "leadership_count": lead,
        "domain_overlap_percent": dom,
        "experience_score": total
    }
