import re

SKILL_GROUPS = {
    "python_dev": [
        "python","numpy","pandas","fastapi","flask","django","scripting",
        "pydantic","rest api","backend","oop","asyncio"
    ],
    "machine_learning": [
        "machine learning","ml","deep learning","pytorch","tensorflow","sklearn",
        "model training","regression","nlp","embeddings","feature engineering"
    ],
    "data_engineering": [
        "sql","postgres","mongodb","etl","data pipeline","spark","hadoop",
        "big data","airflow"
    ],
    "cloud_devops": [
        "docker","kubernetes","k8s","aws","azure","gcp","terraform","ci/cd",
        "jenkins","containers","deployment"
    ],
    "frontend": [
        "react","nextjs","typescript","javascript","ui","components"
    ],
    "soft_skills": [
        "leadership","communication","teamwork","mentorship","collaboration",
        "problem solving"
    ]
}

def normalize(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9+.\- ]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def analyze_skill_groups(resume_text: str):
    resume = normalize(resume_text)
    group_scores = {}
    matched_skills = {}
    missing_skills = {}
    total_group_score = 0
    num_groups = len(SKILL_GROUPS)

    for group, skills in SKILL_GROUPS.items():
        matched = []
        missing = []
        for skill in skills:
            s = normalize(skill)
            if s in resume:
                matched.append(skill)
            else:
                missing.append(skill)
        score = round((len(matched) / len(skills)) * 100, 2)
        group_scores[group] = score
        matched_skills[group] = matched
        missing_skills[group] = missing
        total_group_score += score

    overall = round(total_group_score / num_groups, 2)

    return {
        "group_scores": group_scores,
        "overall_skill_score": overall,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }
