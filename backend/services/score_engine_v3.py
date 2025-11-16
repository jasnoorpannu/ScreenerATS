from services.llm_scoring import (
    llm_relevancy_score,
    llm_skill_strength,
    llm_experience_strength
)

def calculate_final_score_v3(resume_text, keyword_results, formatting_results, job_description):

    # --- LLM SCORES ---
    relevancy = llm_relevancy_score(resume_text, job_description)
    skill_strength = llm_skill_strength(resume_text, job_description)
    experience_strength = llm_experience_strength(resume_text, job_description)

    # --- RULE SCORES ---
    keyword_score = float(keyword_results.get("keyword_score", 0))
    format_score = float(formatting_results.get("format_score", 0))

    # --- HARSHER WEIGHTS ---
    weights = {
        "relevancy": 0.35,    # down from 0.45
        "skill": 0.22,        # down from 0.25
        "experience": 0.18,   # down from 0.20
        "keyword": 0.18,      # UP from 0.07 (penalize missing keywords)
        "format": 0.07        # slightly more weight
    }

    final = (
        relevancy * weights["relevancy"] +
        skill_strength * weights["skill"] +
        experience_strength * weights["experience"] +
        keyword_score * weights["keyword"] +
        format_score * weights["format"]
    )

    # --- PENALTY: Missing keywords ---
    missing_keywords = len(keyword_results.get("missing", []))
    final -= min(missing_keywords * 0.8, 10)   # up to -10 penalty

    # --- Prevent unrealistic perfection ---
    if relevancy > 85 and skill_strength > 90 and experience_strength > 90:
        final -= 5

    # --- Bounds ---
    final_score = round(max(25, min(final, 92)), 2)

    return {
        "relevancy_score": relevancy,
        "skill_strength": skill_strength,
        "experience_strength": experience_strength,
        "keyword_score": keyword_score,
        "format_score": format_score,
        "final_score": final_score
    }
