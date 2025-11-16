from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from services.extract_text import extract_text_from_resume
from services.analyze_keywords import analyze_keywords
from services.format_checks import check_formatting
from services.score_engine import calculate_final_score
from services.semantic_similarity import semantic_match_score

app = FastAPI()

# Allow frontend requests
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
    # Extract text
    resume_text = extract_text_from_resume(file)

    # Keyword analysis
    keyword_results = analyze_keywords(resume_text, job_description)

    # Formatting checks
    formatting_results = check_formatting(resume_text)
    
    #Semantic Similarity
    semantic_score = semantic_match_score(resume_text, job_description)


    # Final score
    score = calculate_final_score(
        keyword_results,
        formatting_results,
        semantic_score
    )

    return {
        "score": score,
        "keywords": keyword_results,
        "formatting": formatting_results,
        "semantic_score": semantic_score
    }
