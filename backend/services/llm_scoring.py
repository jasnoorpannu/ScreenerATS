import google.generativeai as genai

MODEL_NAME = "gemini-2.5-flash"


def _extract_number(text: str) -> float:
    if not text:
        return 0.0
    cleaned = "".join(c for c in text if c.isdigit() or c == ".")
    try:
        return float(cleaned)
    except:
        return 0.0


def _ask_gemini(prompt: str, api_key: str) -> float:
    try:
        if not api_key or not api_key.strip():
            print("Gemini: missing api_key")
            return 0.0

        # configure with provided key (per-request)
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)

        if not response or not hasattr(response, "text"):
            print("Gemini returned empty response")
            return 0.0

        val = _extract_number(response.text)
        return max(0.0, min(val, 100.0))
    except Exception as e:
        print("Gemini Error:", e)
        return 0.0


def llm_relevancy_score(resume_text: str, job_description: str, api_key: str) -> float:
    prompt = f"""
Rate the resume's overall RELEVANCY for the job description.

Consider:
- skill alignment
- experience match
- backend relevance
- domain fit

Return ONLY a single numeric score between 0 and 100 (no commentary).
Resume:
{resume_text}

Job Description:
{job_description}
"""
    return _ask_gemini(prompt, api_key)


def llm_skill_strength(resume_text: str, job_description: str, api_key: str) -> float:
    prompt = f"""
Evaluate how strongly the resume demonstrates the REQUIRED SKILLS from the job description.

Consider:
- programming languages
- backend frameworks
- databases/APIs/system design exposure
- measurable outcomes

Return ONLY a single numeric score between 0 and 100 (no commentary).
Resume:
{resume_text}

Job Description:
{job_description}
"""
    return _ask_gemini(prompt, api_key)


def llm_experience_strength(resume_text: str, job_description: str, api_key: str) -> float:
    prompt = f"""
Evaluate the strength and relevance of the candidate's EXPERIENCE relative to the job.

Consider:
- seniority fit (intern / junior / mid / senior)
- project depth & complexity
- leadership / ownership
- measurable impact

Return ONLY a single numeric score between 0 and 100 (no commentary).
Resume:
{resume_text}

Job Description:
{job_description}
"""
    return _ask_gemini(prompt, api_key)
