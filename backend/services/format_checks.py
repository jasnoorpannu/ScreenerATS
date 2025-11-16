import re

def check_formatting(resume_text: str) -> dict:
    if resume_text.startswith("[ERROR]"):
        return {
            "sections": 0,
            "bullets": 0,
            "avg_line_length": 0,
            "has_headings": False,
            "format_score": 0,
            "error": resume_text
        }

    lines = resume_text.split("\n")

    # Remove empty & tiny lines
    clean_lines = [l.strip() for l in lines if len(l.strip()) > 1]

    # Count bullet points
    bullet_count = sum(1 for l in clean_lines if l.strip().startswith(("-", "*", "•", "‣", "➔")))

    # Detect headings
    headings = [
        "summary", "experience", "education", "projects",
        "skills", "certifications", "achievements",
        "work experience", "internships", "technical skills"
    ]

    found_headings = [h for h in headings if h in resume_text.lower()]

    # Section count = number of headings found
    section_count = len(found_headings)

    # Average line length
    if clean_lines:
        avg_line_length = sum(len(l) for l in clean_lines) / len(clean_lines)
    else:
        avg_line_length = 0

    # Format score
    format_score = 0
    if section_count >= 3:
        format_score += 40
    if bullet_count >= 5:
        format_score += 30
    if 40 < avg_line_length < 120:
        format_score += 30

    return {
        "sections": section_count,
        "bullets": bullet_count,
        "avg_line_length": round(avg_line_length, 2),
        "has_headings": section_count > 0,
        "format_score": format_score
    }
