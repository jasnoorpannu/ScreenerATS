from sentence_transformers import SentenceTransformer, util
import torch

model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_match_score(resume_text: str, job_description: str) -> float:
    # Convert both texts to embeddings
    emb_resume = model.encode(resume_text, convert_to_tensor=True)
    emb_jd = model.encode(job_description, convert_to_tensor=True)

    # Compute cosine similarity
    cos_sim = util.cos_sim(emb_resume, emb_jd)

    score = float(cos_sim[0][0])  # Convert tensor → float
    return round(score * 100, 2)  # Scale to 0–100
