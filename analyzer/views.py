from django.shortcuts import render
from .models import Resume, AnalysisResult
import PyPDF2

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ---------------- SKILLS LIST ----------------
SKILLS = [
    "python", "django", "machine learning",
    "sql", "html", "css", "javascript",
    "numpy", "pandas", "excel", "power bi"
]


# ---------------- PDF TEXT EXTRACTION ----------------
def extract_text(path):
    text = ""
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
    return text.lower()


# ---------------- SKILL EXTRACTION ----------------
def extract_skills(text):
    return [skill for skill in SKILLS if skill in text.lower()]


# ---------------- RESUME ↔ JD MATCH ----------------
def match_resume_with_jd(resume_text, jd_text):
    documents = [resume_text, jd_text]

    tfidf = TfidfVectorizer(stop_words="english")
    matrix = tfidf.fit_transform(documents)

    score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
    return round(score * 100, 2)


# ---------------- MAIN VIEW ----------------
def upload_resume(request):
    percentage = None
    matched_skills = []
    missing_skills = []
    error = None

    if request.method == "POST":
        name = request.POST.get("name")
        resume_file = request.FILES.get("resume")
        jd_text = request.POST.get("jd")

        if not resume_file or not jd_text:
            error = "Resume and Job Description are required."
        else:
            resume = Resume.objects.create(
                name=name,
                resume_file=resume_file
            )

            resume_text = extract_text(resume.resume_file.path)

            percentage = match_resume_with_jd(resume_text, jd_text)

            resume_skills = extract_skills(resume_text)
            jd_skills = extract_skills(jd_text)

            matched_skills = list(set(resume_skills) & set(jd_skills))
            missing_skills = list(set(jd_skills) - set(resume_skills))

            # ✅ HISTORY IS SAVED HERE (THIS WAS YOUR ISSUE)
            AnalysisResult.objects.create(
                resume=resume,
                match_percentage=percentage
            )

    return render(
        request,
        "upload.html",
        {
            "percentage": percentage,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "error": error
        }
    )


# ---------------- HISTORY VIEW ----------------
def history(request):
    results = AnalysisResult.objects.all().order_by("-created_at")
    return render(request, "history.html", {"results": results})
