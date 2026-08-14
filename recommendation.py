def get_recommendation(score, matched_skills=None, missing_skills=None):
    matched_skills = matched_skills or []
    missing_skills = missing_skills or []

    matched_text = ", ".join(matched_skills[:3]) if matched_skills else "few relevant skills"
    missing_text = ", ".join(missing_skills[:2]) if missing_skills else None

    if score >= 85:
        label = "Strongly Recommended"
        reason = f"Excellent match for the role. Demonstrates strong {matched_text}."
        if missing_text:
            reason += f" Consider asking about {missing_text} during the interview."

    elif score >= 70:
        label = "Recommended"
        reason = f"Good candidate with most required skills, including {matched_text}. Suitable for interview."
        if missing_text:
            reason += f" Worth probing on {missing_text}."

    elif score >= 50:
        label = "Consider"
        reason = f"Has some required skills ({matched_text}) but needs improvement."
        if missing_text:
            reason += f" Notably lacks {missing_text}."

    else:
        label = "Not Recommended"
        reason = "Resume lacks most of the important skills required for this role."
        if missing_text:
            reason += f" Missing: {missing_text}."

    return label, reason
