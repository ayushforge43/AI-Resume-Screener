"""
Personalized interview question generator.

Every candidate gets a different set of questions because the questions are
built out of THEIR OWN detected skills, projects, experience lines and the
gap between their resume and the job description - never a fixed list.
"""

# ---------------------------------------------------------------------------
# Per-skill technical questions. Kept as short lists (not single strings) so
# candidates who share a skill don't always get the exact same wording.
# ---------------------------------------------------------------------------
SKILL_QUESTION_BANK = {
    "python": [
        "Explain how Python's memory management (reference counting + garbage collection) works.",
        "What are Python decorators and where have you used them in your own code?",
        "How would you optimize a slow Python script that processes a large dataset?",
    ],
    "java": [
        "Explain the difference between an abstract class and an interface in Java.",
        "How does Java's garbage collector decide when to free an object?",
        "What is the difference between checked and unchecked exceptions in Java?",
    ],
    "c": [
        "Explain the difference between stack and heap memory allocation in C.",
        "How do you avoid memory leaks in C when working with malloc/free?",
    ],
    "c++": [
        "Explain the difference between a pointer and a reference in C++.",
        "What is RAII and why is it important in C++?",
    ],
    "sql": [
        "Write a SQL query to find the second highest salary from an Employee table.",
        "Explain the difference between INNER JOIN and LEFT JOIN with an example.",
        "How would you optimize a slow-running SQL query?",
    ],
    "mysql": [
        "How do indexes improve query performance in MySQL, and what's the trade-off?",
    ],
    "flask": [
        "Explain how routing and request handling work in Flask.",
        "How would you structure a Flask application as it grows beyond a single file?",
        "How would you deploy a Flask application to production?",
    ],
    "django": [
        "Explain Django's MVT (Model-View-Template) architecture.",
        "How does Django's ORM help avoid raw SQL, and when would you still write raw SQL?",
    ],
    "machine learning": [
        "Explain the difference between supervised and unsupervised learning.",
        "How do you decide which evaluation metric to use for a classification model?",
        "What steps do you take to prevent overfitting in a machine learning model?",
    ],
    "deep learning": [
        "Explain the vanishing gradient problem and how it's typically addressed.",
        "What is the difference between a CNN and an RNN, and when would you use each?",
    ],
    "data science": [
        "Walk through your typical end-to-end workflow for a data science project.",
    ],
    "html": [
        "What's the difference between semantic and non-semantic HTML elements?",
    ],
    "css": [
        "Explain the CSS box model and how box-sizing changes it.",
    ],
    "javascript": [
        "Explain the difference between var, let and const in JavaScript.",
        "What is the event loop and how does it relate to asynchronous JavaScript?",
    ],
    "react": [
        "Explain the difference between state and props in React.",
        "What problem do React hooks like useEffect solve?",
    ],
    "nodejs": [
        "Explain how Node.js handles asynchronous I/O with a single thread.",
    ],
    "git": [
        "Explain the difference between git merge and git rebase.",
        "How do you resolve a merge conflict in Git?",
    ],
    "github": [
        "Walk through the pull-request workflow you typically follow on GitHub.",
    ],
    "docker": [
        "Explain the difference between a Docker image and a Docker container.",
    ],
    "aws": [
        "Which AWS services have you used, and what did you use each one for?",
    ],
    "excel": [
        "Which Excel functions do you rely on most for data analysis, and why?",
    ],
    "power bi": [
        "How do you design a Power BI dashboard so it's easy for non-technical stakeholders to read?",
    ],
    "tensorflow": [
        "What is TensorFlow used for, and what's a project where you applied it?",
    ],
    "pandas": [
        "How do you handle missing values in a Pandas DataFrame?",
        "Explain the difference between .loc and .iloc in Pandas.",
    ],
    "numpy": [
        "What is the difference between a NumPy array and a plain Python list?",
    ],
}

GENERIC_TECHNICAL = [
    "Tell us about a technical problem you found genuinely difficult to solve, and how you solved it.",
    "How do you usually approach learning a new technology or tool?",
]

BEHAVIORAL_BANK = [
    "Describe a time you disagreed with a teammate about a technical decision. How did you resolve it?",
    "Tell us about a time you had to learn something quickly under a deadline.",
    "Describe a situation where you had to prioritize between several competing tasks.",
    "Tell us about a mistake you made in a project and what you did after realizing it.",
]


def _difficulty_for(index, total):
    if total <= 1:
        return "Medium"
    ratio = index / max(total - 1, 1)
    if ratio < 0.34:
        return "Easy"
    if ratio < 0.75:
        return "Medium"
    return "Hard"


def _clean_lines(lines, limit=6):
    seen = []
    for line in lines:
        line = line.strip(" -\u2022\t")
        if len(line) < 8:
            continue
        if line.lower() in [s.lower() for s in seen]:
            continue
        seen.append(line)
        if len(seen) >= limit:
            break
    return seen


def _technical_questions(resume_skills, count=5):
    questions = []
    for skill in resume_skills:
        bank = SKILL_QUESTION_BANK.get(skill.lower())
        if not bank:
            continue
        questions.append(bank[0])
        if len(questions) >= count:
            break

    for skill in resume_skills:
        if len(questions) >= count:
            break
        bank = SKILL_QUESTION_BANK.get(skill.lower())
        if bank and len(bank) > 1 and bank[1] not in questions:
            questions.append(bank[1])

    if not questions:
        questions = list(GENERIC_TECHNICAL)

    return questions[:count]


def _resume_based_questions(projects, experience, resume_skills, count=3):
    questions = []

    for project in _clean_lines(projects, limit=3):
        short = project if len(project) < 90 else project[:87] + "..."
        questions.append(
            f'You listed "{short}" as a project \u2014 walk us through how you built it and '
            f"what the trickiest part was."
        )

    for exp in _clean_lines(experience, limit=2):
        short = exp if len(exp) < 90 else exp[:87] + "..."
        questions.append(
            f'Your resume mentions "{short}" \u2014 what was your specific contribution there?'
        )

    if not questions:
        if resume_skills:
            questions.append(
                f"Your resume lists {', '.join(resume_skills[:3])} \u2014 which of these have you "
                f"actually applied in a real project, and how?"
            )
        else:
            questions.append(
                "Walk us through the project or experience on your resume you're most proud of."
            )

    return questions[:count]


def _job_specific_questions(job_skills, matched_skills, count=3):
    questions = []
    for skill in job_skills:
        if skill in matched_skills:
            bank = SKILL_QUESTION_BANK.get(skill.lower())
            if bank:
                extra = bank[2] if len(bank) > 2 else bank[-1]
                questions.append(f"For this role we need strong {skill}. {extra}")
        if len(questions) >= count:
            break

    if not questions:
        questions.append(
            "This role requires skills that aren't clearly reflected on your resume \u2014 "
            "how would you get up to speed quickly?"
        )

    return questions[:count]


def _skill_gap_questions(missing_skills, count=2):
    questions = []
    for skill in missing_skills[:count]:
        questions.append(
            f"We didn't see {skill} on your resume, but it's required for this role \u2014 "
            f"do you have any exposure to it, and how would you approach learning it?"
        )
    if not questions:
        questions.append(
            "Your skill set already covers everything required \u2014 which of these skills "
            "would you say is your strongest, and why?"
        )
    return questions


def _behavioral_questions(score, count=2):
    pool = list(BEHAVIORAL_BANK)
    if score < 50:
        pool.insert(0, "This role needs skills you're still building \u2014 tell us about a time "
                        "you successfully picked up a skill you didn't have going in.")
    return pool[:count]


def generate_questions(matched_skills, resume_skills=None, job_skills=None,
                        missing_skills=None, projects=None, experience=None,
                        score=None, job_title=None):
    """
    Build a personalized, categorized interview question set.

    Backward compatible: if called the old way, with only `matched_skills`,
    it still works and returns a personalized set based on those skills.
    """
    resume_skills = resume_skills if resume_skills is not None else matched_skills
    job_skills = job_skills or []
    missing_skills = missing_skills or []
    projects = projects or []
    experience = experience or []
    score = score if score is not None else 0

    technical = _technical_questions(resume_skills, count=5)
    resume_based = _resume_based_questions(projects, experience, resume_skills, count=3)
    job_specific = _job_specific_questions(job_skills, matched_skills, count=3)
    behavioral = _behavioral_questions(score, count=2)
    skill_gap = _skill_gap_questions(missing_skills, count=2)

    categories = [
        ("Technical", technical),
        ("Resume-Based", resume_based),
        ("Job-Specific", job_specific),
        ("Behavioral", behavioral),
        ("Skill Gap", skill_gap),
    ]

    structured = []
    counter = 1
    for category, qs in categories:
        for i, q in enumerate(qs):
            structured.append({
                "id": counter,
                "category": category,
                "question": q,
                "difficulty": _difficulty_for(i, len(qs)),
            })
            counter += 1

    return structured


def generate_flat_questions(*args, **kwargs):
    """Convenience helper returning just the question strings (legacy shape)."""
    return [item["question"] for item in generate_questions(*args, **kwargs)]
