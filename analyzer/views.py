from django.shortcuts import render, redirect, get_object_or_404
from .models import Resume, AnalysisResult
import PyPDF2

# ================= ROLES & SKILLS =================
ROLES = {
    "ML Engineer": [
        "python", "machine learning", "numpy", "pandas",
        "scikit-learn", "tensorflow", "pytorch"
    ],
    "AI Engineer": [
        "python", "deep learning", "nlp",
        "tensorflow", "pytorch", "opencv"
    ],
    "Full Stack Developer": [
        "html", "css", "javascript", "django",
        "react", "node", "sql"
    ]
}

EDUCATION_KEYWORDS = ["bca", "mca", "btech", "computer science", "information technology"]

EXPERIENCE_KEYWORDS = {
    "Fresher": ["intern", "training", "student"],
    "Mid-Level": ["experience", "2 years", "3 years"],
    "Senior": ["5 years", "lead", "manager"]
}

# ================= PDF TEXT =================
def extract_text(path):
    text = ""
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
    return text.lower()

# ================= SKILLS =================
def extract_skills(text):
    all_skills = set(skill for skills in ROLES.values() for skill in skills)
    return [skill for skill in all_skills if skill in text]

# ================= ROLE MATCH =================
def role_match(resume_skills):
    scores = {}
    for role, skills in ROLES.items():
        matched = set(resume_skills) & set(skills)
        scores[role] = round((len(matched) / len(skills)) * 100, 2)
    best_role = max(scores, key=scores.get)
    return best_role, scores[best_role]

# ================= EXPERIENCE =================
def detect_experience(text):
    for level, words in EXPERIENCE_KEYWORDS.items():
        for w in words:
            if w in text:
                return level
    return "Fresher"

# ================= EDUCATION =================
def detect_education(text):
    for edu in EDUCATION_KEYWORDS:
        if edu in text:
            return "Relevant"
    return "Not Mentioned"

# ================= RESUME QUALITY =================
def resume_quality_score(text):
    score = 0
    if "project" in text:
        score += 2
    if "skills" in text:
        score += 2
    if "experience" in text:
        score += 2
    if len(text.split()) > 400:
        score += 2
    return min(score, 10)

# ================= ATS SCORE =================
def ats_score(resume_skills, role):
    return round((len(resume_skills) / len(ROLES[role])) * 100, 2)

# ================= AI VERDICT =================
def ai_verdict(score):
    if score >= 70:
        return "Strong Match"
    elif score >= 40:
        return "Moderate Match"
    return "Weak Match"

# ================= AI SUGGESTIONS =================
def generate_ai_suggestions(ats, missing_skills, experience, quality):
    suggestions = []

    if ats < 60:
        suggestions.append(
            "Improve ATS score by adding more role-specific keywords."
        )

    if missing_skills:
        suggestions.append(
            "Consider adding or learning these skills: "
            + ", ".join(missing_skills[:3])
        )

    if experience == "Fresher":
        suggestions.append(
            "Highlight internships, academic projects, or certifications."
        )

    if quality < 6:
        suggestions.append(
            "Improve resume structure by clearly separating Skills, Projects, and Experience sections."
        )

    if not suggestions:
        suggestions.append(
            "Your resume is well-optimized for this role. Keep it updated."
        )

    return suggestions

# ================= UPLOAD =================
def upload_resume(request):
    if request.method == "POST":
        name = request.POST.get("name") or "Anonymous"
        resume_file = request.FILES.get("resume")

        resume = Resume.objects.create(name=name, resume_file=resume_file)

        text = extract_text(resume.resume_file.path)
        resume_skills = extract_skills(text)

        best_role, percentage = role_match(resume_skills)

        analysis = AnalysisResult.objects.create(
            resume=resume,
            match_percentage=percentage
        )

        return redirect("result", id=analysis.id)

    return render(request, "upload.html")

# ================= RESULT =================
def result(request, id):
    record = get_object_or_404(AnalysisResult, id=id)
    resume = record.resume

    text = extract_text(resume.resume_file.path)
    resume_skills = extract_skills(text)

    best_role, percentage = role_match(resume_skills)

    experience = detect_experience(text)
    education = detect_education(text)
    quality = resume_quality_score(text)
    ats = ats_score(resume_skills, best_role)

    matched_skills = list(set(resume_skills) & set(ROLES[best_role]))
    missing_skills = list(set(ROLES[best_role]) - set(matched_skills))
    verdict = ai_verdict(percentage)

    suggestions = generate_ai_suggestions(
        ats, missing_skills, experience, quality
    )

    context = {
        "name": resume.name,
        "best_role": best_role,
        "percentage": percentage,
        "experience": experience,
        "education": education,
        "quality": quality,
        "ats": ats,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "verdict": verdict,
        "suggestions": suggestions,
    }

    return render(request, "result.html", context)

# ================= HISTORY =================
def history(request):
    results = AnalysisResult.objects.select_related("resume").order_by("-id")
    return render(request, "history.html", {"results": results})

# ================= DELETE =================
def delete_history(request, id):
    record = get_object_or_404(AnalysisResult, id=id)
    if request.method == "POST":
        record.delete()
    return redirect("history")
