"""
Suggests which role(s) at the company a candidate's skill set fits best —
independent of whichever specific job description they were screened
against. Useful when a strong candidate isn't the right fit for the role
they applied to, but would be a great fit somewhere else on the team.
"""

# Each role's core skill profile, drawn from the same vocabulary matcher.py
# already detects. Keep keys as the *display* names extract_skills() returns
# (e.g. "SQL", "AWS") so matching is a direct set comparison.
ROLE_PROFILES = {
    "Backend Developer": [
        "Python", "Java", "Flask", "Django", "SQL", "MySQL", "Git", "Docker",
    ],
    "Frontend Developer": [
        "HTML", "CSS", "Javascript", "React", "Node.js", "Git",
    ],
    "Full Stack Developer": [
        "HTML", "CSS", "Javascript", "React", "Node.js", "Python", "Flask",
        "SQL", "Git",
    ],
    "Data Analyst": [
        "SQL", "Excel", "Power BI", "Pandas", "Numpy", "Data Science",
    ],
    "Data Scientist": [
        "Python", "Machine Learning", "Deep Learning", "Data Science",
        "Pandas", "Numpy", "Tensorflow",
    ],
    "Machine Learning Engineer": [
        "Python", "Machine Learning", "Deep Learning", "Tensorflow",
        "Numpy", "Pandas", "Docker", "AWS",
    ],
    "DevOps Engineer": [
        "Docker", "AWS", "Git", "Github", "Python",
    ],
    "Business Intelligence Analyst": [
        "Excel", "Power BI", "SQL", "Data Science",
    ],
    "QA / Software Engineer": [
        "Python", "Java", "C", "C++", "Git", "Github",
    ],
}


def recommend_positions(resume_skills, top_n=3):
    """
    Score a candidate's detected skills against every known role profile.

    Returns a list of dicts, sorted by fit % descending:
        {
            "role": "Data Scientist",
            "fit_score": 71,
            "matched_skills": [...],
            "missing_skills": [...],   # from that role's profile only
        }
    """
    resume_set = {s.lower() for s in resume_skills}
    ranked = []

    for role, required in ROLE_PROFILES.items():
        matched = [s for s in required if s.lower() in resume_set]
        missing = [s for s in required if s.lower() not in resume_set]
        fit_score = round((len(matched) / len(required)) * 100) if required else 0

        ranked.append({
            "role": role,
            "fit_score": fit_score,
            "matched_skills": matched,
            "missing_skills": missing,
        })

    ranked.sort(key=lambda r: r["fit_score"], reverse=True)
    return ranked[:top_n]


def best_position_reason(candidate_name, top_role):
    """One-line explainable reasoning for the #1 suggested role."""
    if top_role["fit_score"] == 0:
        return (
            f"{candidate_name}'s detected skills don't clearly align with any "
            f"defined role yet — worth a manual review."
        )

    skills_text = ", ".join(top_role["matched_skills"][:4]) or "their current skill set"
    return (
        f"Based on {skills_text}, {candidate_name} is the strongest fit for "
        f"{top_role['role']} ({top_role['fit_score']}% profile match)."
    )
