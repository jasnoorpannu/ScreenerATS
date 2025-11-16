import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-2.5-flash"   # stable, available, supports generateContent

def _extract_number(text: str) -> float:
    if not text:
        return 0.0
    cleaned = "".join(c for c in text if c.isdigit() or c == ".")
    try:
        return float(cleaned)
    except:
        return 0.0


def _ask_gemini(prompt: str) -> float:
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)

        if not response or not hasattr(response, "text"):
            print("Gemini empty response")
            return 0.0

        val = _extract_number(response.text)
        return max(0, min(val, 100))  # clamp 0–100

    except Exception as e:
        print("Gemini Error:", e)
        return 0.0


def llm_relevancy_score(resume_text: str, job_description: str) -> float:
    prompt = f"""
Rate the resume's overall RELEVANCY for the job description.

Consider:
- skill alignment
- experience match
- backend relevance
- domain fit

Return ONLY a number (0–100).

Resume:
{resume_text}

Job Description:
{job_description}
"""
    return _ask_gemini(prompt)


def llm_skill_strength(resume_text: str, job_description: str) -> float:
    prompt = f"""
Evaluate the resume's SKILL MATCH against the job description.

Consider:
- programming languages
- backend skills
- APIs, DBs, system knowledge
- required vs demonstrated skills

Return ONLY a number (0–100).
Resume:
{resume_text}

Job Description:
{job_description}
"""
    return _ask_gemini(prompt)


def llm_experience_strength(resume_text: str, job_description: str) -> float:
    prompt = f"""
Evaluate the EXPERIENCE strength relative to the job description.

Consider:
- project depth
- internships
- impact & responsibility
- backend-related experience

Return ONLY a number (0–100).
Resume:
{resume_text}

Job Description:
{job_description}
"""
    return _ask_gemini(prompt)
