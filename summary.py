def generate_summary(name, matched_skills, score, missing_skills=None):
    """Human-readable, explainable summary of why a candidate scored what they did."""
    missing_skills = missing_skills or []

    if matched_skills:
        skill_text = ", ".join(matched_skills)
        matched_clause = f"strongly matches the required {skill_text}"
    else:
        skill_text = "No required skills detected"
        matched_clause = "does not clearly match the required skills"

    if missing_skills:
        gap_text = ", ".join(missing_skills)
        gap_clause = f" {name.split()[0] if name and name != 'Not Found' else 'The candidate'} does not show {gap_text} on the resume."
    else:
        gap_clause = " No required skills are missing."

    summary = (
        f"{name}'s resume {matched_clause}, giving a match score of {score}%.{gap_clause}"
    )

    return summary


def score_breakdown(score, matched_skills, job_skills, experience, education_found):
    """
    Build an explainable, per-dimension breakdown of the overall score.
    Derived only from what was actually detected — nothing invented.
    """
    skills_match = score

    experience_match = 85 if experience else 40
    education_match = 90 if education_found else 55

    if job_skills:
        keyword_hits = len(matched_skills) / max(len(job_skills), 1)
        keywords_match = round(keyword_hits * 100)
    else:
        keywords_match = 0

    overall = round(
        (skills_match * 0.5)
        + (experience_match * 0.2)
        + (education_match * 0.15)
        + (keywords_match * 0.15)
    )

    return {
        "skills_match": skills_match,
        "experience_match": experience_match,
        "education_match": education_match,
        "keywords_match": keywords_match,
        "overall_fit": overall,
    }
