import re

SKILL_LIST = [
    "python",
    "java",
    "c",
    "c++",
    "sql",
    "mysql",
    "flask",
    "django",
    "machine learning",
    "deep learning",
    "data science",
    "html",
    "css",
    "javascript",
    "react",
    "nodejs",
    "git",
    "github",
    "docker",
    "aws",
    "excel",
    "power bi",
    "tensorflow",
    "pandas",
    "numpy",
]


# Skills whose conventional display casing isn't simple Title Case
# (acronyms, stylized product names).
DISPLAY_OVERRIDES = {
    "sql": "SQL",
    "mysql": "MySQL",
    "html": "HTML",
    "css": "CSS",
    "aws": "AWS",
    "c": "C",
    "c++": "C++",
    "nodejs": "Node.js",
    "power bi": "Power BI",
}


def _display_name(skill):
    return DISPLAY_OVERRIDES.get(skill, skill.title())


def extract_skills(text):
    """
    Detect known skills in free text using whole-word matching, so short
    skill names like "C" or "R" don't false-positive inside unrelated words
    (e.g. "science", "certification").
    """
    text = text.lower()
    found_skills = []

    for skill in SKILL_LIST:
        # Escape regex special chars (e.g. "c++") and match on word
        # boundaries. "+" isn't a \w character so \b won't sit next to it
        # cleanly — handle that case with a lookaround instead.
        escaped = re.escape(skill)
        pattern = r'(?<![a-z0-9])' + escaped + r'(?![a-z0-9])'
        if re.search(pattern, text):
            found_skills.append(_display_name(skill))

    return found_skills


def compare_skills(resume_skills, job_skills):
    matched = []
    missing = []

    for skill in job_skills:
        if skill in resume_skills:
            matched.append(skill)
        else:
            missing.append(skill)

    if len(job_skills) == 0:
        score = 0
    else:
        score = round((len(matched) / len(job_skills)) * 100)

    return score, matched, missing