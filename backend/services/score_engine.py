def calculate_final_score(keyword_results: dict, formatting_results: dict, semantic_score: float) -> int:
    if "error" in keyword_results or "error" in formatting_results:
        return 0

    keyword_score = keyword_results.get("keyword_score", 0)
    format_score = formatting_results.get("format_score", 0)

    final = (
        semantic_score * 0.55 +   # most important
        keyword_score * 0.25 +    # still helps
        format_score * 0.20       # still matters
    )

    return round(min(max(final, 0), 100))
