import re


def extract_projects(text):

    projects = []

    lines = text.splitlines()

    in_projects = False

    stop_sections = [
        "experience",
        "internship",
        "education",
        "skills",
        "technical skills",
        "certifications",
        "soft skills",
        "languages",
        "achievements"
    ]

    for line in lines:

        line = line.strip()

        if not line:
            continue

        lower = line.lower()

        # Start Projects section
        if lower in [
            "projects",
            "project",
            "academic projects",
            "personal projects"
        ]:
            in_projects = True
            continue

        # Stop Projects section
        if in_projects and lower in stop_sections:
            break

        if in_projects:
            # Split projects separated by commas
            parts = line.split(",")

            for part in parts:
                part = part.strip()

                if len(part) > 2:
                    projects.append(part)

    return list(dict.fromkeys(projects))


def extract_education(text):

    education = []

    lines = text.splitlines()

    in_education = False

    stop_sections = [
        "experience",
        "skills",
        "technical skills",
        "projects",
        "certifications",
        "soft skills",
        "languages",
        "achievements",
        "internship",
        "internships"
    ]

    for line in lines:

        line = line.strip()

        if not line:
            continue

        lower = line.lower()

        # Start Education section
        if lower in ["education", "academic background", "qualifications"]:
            in_education = True
            continue

        # Stop Education section
        if in_education and lower in stop_sections:
            break

        if in_education:
            education.append(line)

    return list(dict.fromkeys(education))


def extract_experience(text):

    experience = []

    lines = text.splitlines()

    in_experience = False

    stop_sections = [
        "education",
        "skills",
        "technical skills",
        "projects",
        "certifications",
        "soft skills",
        "languages",
        "achievements"
    ]

    for line in lines:

        line = line.strip()

        if not line:
            continue

        lower = line.lower()

        # Start Experience section
        if lower in [
            "experience",
            "work experience",
            "professional experience",
            "internship",
            "internships"
        ]:
            in_experience = True
            continue

        # Stop Experience section
        if in_experience and lower in stop_sections:
            break

        if in_experience:
            experience.append(line)

    return list(dict.fromkeys(experience))