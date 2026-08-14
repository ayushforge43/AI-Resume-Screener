from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from resume_parser import extract_text, ResumeParseError
from info_extractor import extract_name, extract_email, extract_phone
from matcher import extract_skills, compare_skills
from recommendation import get_recommendation
from summary import generate_summary, score_breakdown
from project_extractor import extract_projects, extract_experience, extract_education
from interview_questions import generate_questions
from role_recommender import recommend_positions, best_position_reason
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

# Upload folder
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Allow large batches of resumes
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------------------------------------------------------------------
# In-memory "database" for this demo app. Good enough for a single-session
# screening run / classroom-style demo; swap for a real DB for production use.
# ---------------------------------------------------------------------------
all_candidates = []
current_job = {"title": "", "description": ""}
history = {
    "jobs_created": 0,
    "resumes_screened": 0,
    "interviews_generated": 0,
}


def _allowed_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS


def _status_for_score(score):
    if score >= 85:
        return "Excellent Match"
    if score >= 70:
        return "Strong Match"
    if score >= 50:
        return "Potential Match"
    return "Low Match"


def _dashboard_stats(candidates):
    total = len(candidates)
    shortlisted = len([c for c in candidates if c["score"] >= 70])
    rejected = len([c for c in candidates if c["score"] < 50])
    avg_score = round(sum(c["score"] for c in candidates) / total) if total else 0

    return {
        "total_resumes": history["resumes_screened"],
        "shortlisted": shortlisted,
        "rejected": rejected,
        "avg_score": avg_score,
        "jobs_created": history["jobs_created"],
        "interviews_generated": history["interviews_generated"],
    }


@app.route("/")
def home():
    stats = _dashboard_stats(all_candidates)
    top_candidates = sorted(all_candidates, key=lambda c: c["score"], reverse=True)[:5]
    return render_template(
        "index.html",
        stats=stats,
        top_candidates=top_candidates,
        job_title=current_job["title"],
    )


@app.route("/upload", methods=["POST"])
def upload():

    global all_candidates, current_job

    resumes = request.files.getlist("resume")

    job_title = request.form.get("job_title", "").strip() or "Untitled Role"
    job_description = request.form.get("job_description", "").strip()
    preferred_skills_raw = request.form.get("preferred_skills", "").strip()

    if not job_description:
        flash("Please provide a job description before starting the analysis.", "error")
        return redirect(url_for("home"))

    valid_resumes = [r for r in resumes if r and r.filename]

    if not valid_resumes:
        flash("Please upload at least one PDF or DOCX resume.", "error")
        return redirect(url_for("home"))

    # Extract job skills once
    job_skills = extract_skills(job_description)
    if preferred_skills_raw:
        job_skills = list(dict.fromkeys(job_skills + extract_skills(preferred_skills_raw)))

    current_job = {"title": job_title, "description": job_description}
    history["jobs_created"] += 1

    candidates = []

    for resume in valid_resumes:

        if not _allowed_file(resume.filename):
            flash(
                f'"{resume.filename}" was skipped — please upload a PDF or DOCX resume.',
                "error",
            )
            continue

        try:
            safe_name = secure_filename(resume.filename)
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], safe_name)
            resume.save(save_path)

            # Extract text
            resume_text = extract_text(save_path)

            # Candidate information
            candidate_name = extract_name(resume_text) or "Not Found"
            candidate_email = extract_email(resume_text) or "Not Found"
            candidate_phone = extract_phone(resume_text) or "Not Found"

            # Skills
            resume_skills = extract_skills(resume_text)

            # Match skills
            score, matched_skills, missing_skills = compare_skills(
                resume_skills, job_skills
            )

            # Recommendation (grounded in matched/missing skills, not generic)
            recommendation, reason = get_recommendation(
                score, matched_skills, missing_skills
            )

            # AI Summary + explainable breakdown
            summary = generate_summary(
                candidate_name, matched_skills, score, missing_skills
            )

            # Projects / experience / education
            projects = extract_projects(resume_text)
            experience = extract_experience(resume_text)
            education = extract_education(resume_text)

            breakdown = score_breakdown(
                score, matched_skills, job_skills, experience, bool(education)
            )

            # Best-fit position(s) across the company, based on this
            # candidate's own skill set (independent of the JD applied to)
            best_fit_roles = recommend_positions(resume_skills, top_n=3)
            best_fit_reason = best_position_reason(candidate_name, best_fit_roles[0]) if best_fit_roles else ""

            # Personalized, categorized interview questions
            questions = generate_questions(
                matched_skills,
                resume_skills=resume_skills,
                job_skills=job_skills,
                missing_skills=missing_skills,
                projects=projects,
                experience=experience,
                score=score,
                job_title=job_title,
            )
            history["interviews_generated"] += 1

            candidate = {
                "id": len(candidates),
                "name": candidate_name,
                "email": candidate_email,
                "phone": candidate_phone,
                "score": score,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "additional_skills": [s for s in resume_skills if s not in matched_skills],
                "recommendation": recommendation,
                "reason": reason,
                "summary": summary,
                "breakdown": breakdown,
                "projects": projects,
                "experience": experience,
                "education": education,
                "questions": questions,
                "status": _status_for_score(score),
                "best_fit_roles": best_fit_roles,
                "best_fit_reason": best_fit_reason,
            }

            candidates.append(candidate)
            history["resumes_screened"] += 1

        except ResumeParseError as e:
            flash(f'"{resume.filename}": {e}', "error")
        except Exception as e:
            flash(f'Something went wrong processing "{resume.filename}". Please try again.', "error")
            app.logger.exception("Error processing %s: %s", resume.filename, e)

    if not candidates:
        flash("No resumes could be analyzed. Please check the files and try again.", "error")
        return redirect(url_for("home"))

    # Highest score first, re-assign ids to match sorted order
    candidates.sort(key=lambda x: x["score"], reverse=True)
    for i, c in enumerate(candidates):
        c["id"] = i

    all_candidates = candidates

    return render_template(
        "ranking.html",
        candidates=candidates[:20],
        total_candidates=len(candidates),
        current_page=1,
        total_pages=max(1, (len(candidates) + 19) // 20),
        search="",
        job_title=current_job["title"],
    )


@app.route("/results")
def results():

    global all_candidates

    search = request.args.get("search", "").strip().lower()
    status_filter = request.args.get("status", "").strip()

    try:
        page = int(request.args.get("page", 1))
    except ValueError:
        page = 1

    filtered = all_candidates

    if search:
        filtered = [
            c for c in filtered
            if search in c["name"].lower() or search in c["email"].lower()
        ]

    if status_filter:
        filtered = [c for c in filtered if c["status"] == status_filter]

    per_page = 20
    total_candidates = len(filtered)
    total_pages = max(1, (total_candidates + per_page - 1) // per_page)

    page = max(1, min(page, total_pages))

    start = (page - 1) * per_page
    end = start + per_page
    page_candidates = filtered[start:end]

    return render_template(
        "ranking.html",
        candidates=page_candidates,
        total_candidates=total_candidates,
        current_page=page,
        total_pages=total_pages,
        search=search,
        status_filter=status_filter,
        job_title=current_job["title"],
    )


@app.route("/candidate/<int:candidate_id>")
def profile(candidate_id):
    candidate = next((c for c in all_candidates if c["id"] == candidate_id), None)
    if candidate is None:
        flash("That candidate profile is no longer available. Please re-run the analysis.", "error")
        return redirect(url_for("home"))

    return render_template(
        "profile.html",
        candidate=candidate,
        job_title=current_job["title"],
    )


@app.route("/candidate/<int:candidate_id>/regenerate-questions", methods=["POST"])
def regenerate_questions(candidate_id):
    candidate = next((c for c in all_candidates if c["id"] == candidate_id), None)
    if candidate is None:
        flash("That candidate profile is no longer available.", "error")
        return redirect(url_for("home"))

    job_skills = extract_skills(current_job.get("description", ""))
    candidate["questions"] = generate_questions(
        candidate["matched_skills"],
        resume_skills=candidate["matched_skills"] + candidate["additional_skills"],
        job_skills=job_skills,
        missing_skills=candidate["missing_skills"],
        projects=candidate["projects"],
        experience=candidate["experience"],
        score=candidate["score"],
        job_title=current_job["title"],
    )
    history["interviews_generated"] += 1
    flash("Interview questions regenerated.", "success")
    return redirect(url_for("profile", candidate_id=candidate_id))


@app.errorhandler(413)
def too_large(e):
    flash("That upload is too large. Please upload smaller files.", "error")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
