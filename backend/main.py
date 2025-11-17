from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from services.extract_text import extract_text_from_resume
from services.analyze_keywords import analyze_keywords
from services.format_checks import check_formatting
from services.score_engine_v3 import calculate_final_score_v3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://screenerats.vercel.app",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "message": "ScreenerATS API is live",
        "endpoints": {
            "analyze": "/analyze (POST)",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Simple health check for uptime monitoring"""
    return {"status": "healthy"}

@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    api_key: str = Form(...),
):
    """
    Expects:
      - file: resume (pdf/docx)
      - job_description: text
      - api_key: user's Gemini API key (passed through; not stored)
    """
    # 1) extract resume text
    resume_text = extract_text_from_resume(file)
    
    # 2) keyword & formatting checks
    keyword_results = analyze_keywords(resume_text, job_description)
    formatting_results = check_formatting(resume_text)
    
    # 3) final LLM-driven scoring (uses user's key)
    breakdown = calculate_final_score_v3(
        resume_text,
        keyword_results,
        formatting_results,
        job_description,
        api_key,
    )
    
    # ensure format_score exists for frontend
    formatting_results["format_score"] = breakdown.get("format_score", 0)
    
    return {
        "final_score": breakdown["final_score"],
        "score_breakdown": breakdown,
        "keywords": keyword_results,
        "formatting": formatting_results,
    }