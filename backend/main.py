from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware

# Core Services
from services.extract_text import extract_text_from_resume
from services.analyze_keywords import analyze_keywords
from services.format_checks import check_formatting

# New LLM-first scoring engine
from services.score_engine_v3 import calculate_final_score_v3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):

    # 1. Extract resume text
    resume_text = extract_text_from_resume(file)

    # 2. Keyword analysis
    keyword_results = analyze_keywords(resume_text, job_description)

    # 3. Formatting checks
    formatting_results = check_formatting(resume_text)

    # 4. Final LLM-driven scoring
    breakdown = calculate_final_score_v3(
        resume_text,
        keyword_results,
        formatting_results,
        job_description
    )

    # Ensure formatting_score always exists for frontend
    formatting_results["format_score"] = breakdown.get("format_score", 0)

    # 5. Send results
    return {
        "final_score": breakdown["final_score"],
        "score_breakdown": breakdown,
        "keywords": keyword_results,
        "formatting": formatting_results,
    }
