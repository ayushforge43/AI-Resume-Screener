# Resume Intelligence — Smart Resume Screening & Candidate Ranking

An AI-assisted recruitment dashboard: upload resumes, describe a role, get
scored/ranked candidates and a personalized interview question set for each
one — built on your original Flask pipeline.

## Run it

```bash
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000

## What changed vs. your original project

**Kept intact:** the overall pipeline (extract → match → score → rank →
recommend → interview questions), Flask routing style, and the general shape
of `matcher.py` / `project_extractor.py` / `info_extractor.py`.

**Frontend** (`templates/`, `static/`) — completely new, since none was
uploaded:
- `index.html` — dashboard with animated stat cards, drag-and-drop resume
  upload, job description form, and a simulated AI-pipeline processing
  overlay (upload → extract → analyze → compare → score → questions).
- `ranking.html` — sortable, searchable, filterable candidate ranking table
  with match-score badges.
- `profile.html` — full candidate profile: animated score ring, score
  breakdown bars, skills analysis (matching / missing / additional),
  explainable AI analysis, hiring recommendation, education/experience/
  projects, and the personalized interview question board (filter by
  category, regenerate, copy, export as .txt).
- `static/css/style.css` — dark navy/indigo glass UI with a violet + teal
  accent pair, `Space Grotesk` / `Inter` / `JetBrains Mono` type system.
- `static/js/main.js` — dropzone, processing-pipeline animation, animated
  counters/bars, question filtering, copy-to-clipboard, export.

**Backend logic — real fixes, not just cosmetic:**
- `matcher.py`: skill matching now uses whole-word matching instead of
  substring matching. Previously a single-letter skill like `"c"` matched
  inside *any* word containing the letter c (e.g. "science",
  "certification"), which silently inflated everyone's skill list. Also
  added correct display casing (`SQL`, `AWS`, `HTML`, not `Sql`/`Aws`/`Html`).
- `interview_questions.py`: this was the main ask. Questions are now built
  per-candidate from **their own** detected skills, projects, work
  experience, and the specific gap between their resume and the job
  description — grouped into Technical / Resume-Based / Job-Specific /
  Behavioral / Skill-Gap categories with difficulty labels, instead of one
  shared fixed list for every candidate.
- `resume_parser.py`: now supports `.docx` in addition to `.pdf`, and raises
  friendly, catchable errors instead of crashing the request.
- `summary.py` / `recommendation.py`: reasoning is now grounded in the
  candidate's actual matched/missing skills (e.g. "lacks AWS, TensorFlow")
  instead of a generic templated sentence, and a `score_breakdown()` helper
  produces the Skills/Experience/Education/Keywords/Overall split shown on
  the profile page.
- `project_extractor.py`: added `extract_education()` using the same
  section-scanning approach as the existing projects/experience extractors.
- `app.py`: added a dashboard route with real stats, a candidate profile
  route (`/candidate/<id>`), a "regenerate questions" endpoint, DOCX support
  wiring, flash-based friendly error handling (oversized upload, missing JD,
  unreadable file, unsupported format), and secured filenames on save.

## Notes / next steps if you keep building this

- Candidate data is stored in-memory (`all_candidates` in `app.py`) — it
  resets on server restart. Fine for a demo; swap for SQLite/Postgres if you
  need it to persist.
- The skill list in `matcher.py` is still a fixed vocabulary. For the JD
  "paste & auto-extract required/preferred skills" feature to fully live up
  to the brief, that list would need to grow or be swapped for an actual
  NLP/keyword-extraction step.
- No `.env`/API key is required anywhere in this version — all "AI" here is
  rule-based (skill matching + templated reasoning), not an LLM call. If you
  want LLM-generated summaries/questions instead, that's a clean drop-in
  behind `summary.py` / `interview_questions.py`.
