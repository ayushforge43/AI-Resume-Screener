# 🤖 AI Resume Screener


### AI-Powered Resume Screening, Candidate Ranking & Interview Preparation


An intelligent web application that helps recruiters analyze resumes against a specific job description, calculate candidate match scores, identify skill gaps, rank candidates, and generate personalized interview questions.


🚀 **Live Demo:** https://ai-resume-screener-lzl3.onrender.com


---


## 📌 Overview


Recruiters often have to manually review a large number of resumes for a single job opening. This process can be time-consuming and inconsistent.


The **AI Resume Screener** automates important parts of the recruitment screening process.


Users can upload multiple resumes, provide a job description, and receive:


- Candidate matching scores
- Candidate ranking
- Matching and missing skills
- Experience and education analysis
- Hiring recommendations
- Candidate summaries
- Personalized interview questions


The system is designed as an AI-assisted recruitment tool where final hiring decisions remain with human recruiters.


---


## 🚀 Live Demo


👉 **Try the application:**  
https://ai-resume-screener-lzl3.onrender.com


---


## ✨ Features


### 📄 Resume Upload


- Upload PDF resumes
- Upload DOCX resumes
- Multiple resumes can be uploaded
- Secure filename handling


### 🎯 Resume & Job Matching


The system compares candidate resumes with the requirements of a job description.


It analyzes:


- Required skills
- Preferred skills
- Experience
- Education
- Relevant keywords


### 📊 Candidate Scoring


Each candidate receives an overall match score based on multiple factors.


The application provides a score breakdown for:


- Skills
- Experience
- Education
- Keywords
- Overall Match


🛠️ Technologies Used
Backend
Python
Flask
Resume Processing
PyPDF2
python-docx
Frontend
HTML
CSS
JavaScript
Deployment
GitHub
Render
Development Tools
Git
Visual Studio Code
📂 Project Structure
AI-Resume-Screener/
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
│
├── templates/
│   ├── index.html
│   ├── profile.html
│   └── ranking.html
│
├── app.py
├── info_extractor.py
├── interview_questions.py
├── matcher.py
├── project_extractor.py
├── recommendation.py
├── resume_parser.py
├── role_recommender.py
├── summary.py
├── requirements.txt
├── .gitignore
└── README.md
⚙️ Installation
1. Clone the repository
git clone https://github.com/ayushforge43/AI-Resume-Screener.git
2. Open the project
cd AI-Resume-Screener
3. Install dependencies
pip install -r requirements.txt
4. Run the application
python app.py
5. Open in your browser
http://127.0.0.1:5000
🎯 Example Use Case

A recruiter wants to hire a Python Backend Developer.

They enter:

Job Title:
Python Backend Developer

And provide requirements such as:

Python
Flask
SQL
REST APIs
Git

The recruiter then uploads multiple resumes.

The system analyzes each resume and produces:

Candidate A
Match Score: 87%


Candidate B
Match Score: 74%


Candidate C
Match Score: 61%

The recruiter can then open a candidate profile to understand:

Why the candidate received the score
Which skills match
Which skills are missing
Their experience and education
Recommended hiring decision
Personalized interview questions
📊 Key Components
resume_parser.py

Extracts text from PDF and DOCX resumes.

matcher.py

Compares candidate skills with job requirements and calculates matching information.

project_extractor.py

Extracts projects, experience, and education information.

recommendation.py

Generates candidate hiring recommendations.

summary.py

Creates candidate summaries and score explanations.

interview_questions.py

Generates candidate-specific interview questions.

role_recommender.py

Provides role recommendations based on candidate skills.

app.py

Main Flask application that connects the frontend and backend components.

🔐 Important Note

This application is designed as an AI-assisted recruitment screening tool.

It should support recruiters rather than replace human decision-making.

Candidate information and recommendations should always be reviewed by a human before making hiring decisions.

🚀 Future Improvements

Planned improvements include:

 Database integration using PostgreSQL
 Persistent candidate storage
 Advanced NLP-based skill extraction
 LLM-powered interview questions
 Authentication and recruiter accounts
 Resume comparison dashboard
 Export candidate reports as PDF
 Advanced analytics
 Job description automatic skill extraction
 Cloud-based resume storage
👨‍💻 Author

Ayush

B.Tech | Data Science & AI

Project

AI Resume Screener

GitHub:
https://github.com/ayushforge43/AI-Resume-Screener

Live Demo:
https://ai-resume-screener-lzl3.onrender.com

⭐ Support

If you find this project useful, consider giving the repository a ⭐ star!
