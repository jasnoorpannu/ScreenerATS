from services.llm_scoring import (
    llm_relevancy_score,
    llm_skill_strength,
    llm_experience_strength
)

def calculate_final_score_v3(
    resume_text,
    keyword_results,
    formatting_results,
    job_description,
    api_key
):
    # --- LLM SCORES ---
    relevancy = llm_relevancy_score(resume_text, job_description, api_key)
    skill_strength = llm_skill_strength(resume_text, job_description, api_key)
    experience_strength = llm_experience_strength(resume_text, job_description, api_key)

    # --- RULE SCORES ---
    keyword_score = float(keyword_results.get("keyword_score", 0))
    format_score = float(formatting_results.get("format_score", 0))

    # --- WEIGHTS ---
    weights = {
        "relevancy": 0.35,
        "skill": 0.22,
        "experience": 0.18,
        "keyword": 0.18,
        "format": 0.07,
    }

    final = (
        relevancy * weights["relevancy"] +
        skill_strength * weights["skill"] +
        experience_strength * weights["experience"] +
        keyword_score * weights["keyword"] +
        format_score * weights["format"]
    )

    # --- PENALTY FOR MISSING KEYWORDS ---
    missing_keywords = len(keyword_results.get("missing", []))
    final -= min(missing_keywords * 0.8, 10)

    # --- NO UNREALISTIC PERFECTION ---
    if relevancy > 85 and skill_strength > 90 and experience_strength > 90:
        final -= 5

    # --- BOUNDS ---
    final_score = round(max(25, min(final, 92)), 2)

    return {
        "relevancy_score": round(relevancy, 2),
        "skill_strength": round(skill_strength, 2),
        "experience_strength": round(experience_strength, 2),
        "keyword_score": round(keyword_score, 2),
        "format_score": round(format_score, 2),
        "final_score": final_score
    }
