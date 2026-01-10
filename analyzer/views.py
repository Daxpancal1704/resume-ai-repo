from django.shortcuts import render, redirect, get_object_or_404
from .models import Resume, AnalysisResult
import PyPDF2


# ---------------- ROLE SKILL MAP (AI KNOWLEDGE BASE) ----------------
ROLES = {
    "ML Engineer": [
        "python", "machine learning", "numpy", "pandas",
        "scikit-learn", "tensorflow", "pytorch"
    ],
    "AI Engineer": [
        "python", "machine learning", "deep learning",
        "nlp", "tensorflow", "pytorch", "opencv"
    ],
    "Full Stack Developer": [
        "html", "css", "javascript", "django",
        "react", "node", "sql"
    ]
}


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
    all_skills = set(skill for skills in ROLES.values() for skill in skills)
    return [skill for skill in all_skills if skill in text]


# ---------------- ROLE MATCHING LOGIC ----------------
def match_resume_to_roles(resume_skills):
    scores = {}
    for role, skills in ROLES.items():
        matched = set(resume_skills) & set(skills)
        score = (len(matched) / len(skills)) * 100
        scores[role] = round(score, 2)

    best_role = max(scores, key=scores.get)
    return best_role, scores


# ---------------- AI VERDICT ----------------
def ai_verdict(percentage):
    if percentage >= 70:
        return "Strong Match"
    elif percentage >= 40:
        return "Moderate Match"
    return "Weak Match"


# ---------------- AI SUGGESTIONS ----------------
def ai_resume_suggestions(missing_skills):
    if not missing_skills:
        return ["Your resume strongly matches this role."]
    return [f"Consider adding {skill} to improve your profile." for skill in missing_skills]


# ==================================================
# PAGE 1 : UPLOAD FORM
# ==================================================
def upload_resume(request):
    if request.method == "POST":
        resume = Resume.objects.create(
            name=request.POST.get("name"),
            resume_file=request.FILES.get("resume")
        )
        # 🔁 Redirect to result page
        return redirect("result", resume.id)

    return render(request, "upload.html")


# ==================================================
# PAGE 2 : RESULT PAGE (ALL AI DETAILS)
# ==================================================
def result(request, id):
    resume = get_object_or_404(Resume, id=id)

    resume_text = extract_text(resume.resume_file.path)
    resume_skills = extract_skills(resume_text)

    best_role, scores = match_resume_to_roles(resume_skills)
    percentage = scores[best_role]

    matched_skills = list(set(resume_skills) & set(ROLES[best_role]))
    missing_skills = list(set(ROLES[best_role]) - set(matched_skills))

    verdict = ai_verdict(percentage)
    suggestions = ai_resume_suggestions(missing_skills)

    AnalysisResult.objects.create(
        resume=resume,
        match_percentage=percentage
    )

    return render(
        request,
        "result.html",
        {
            "name": resume.name,
            "best_role": best_role,
            "percentage": percentage,
            "verdict": verdict,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "suggestions": suggestions
        }
    )


# ---------------- HISTORY VIEW ----------------
def history(request):
    results = AnalysisResult.objects.all().order_by("-created_at")
    return render(request, "history.html", {"results": results})


# ---------------- DELETE HISTORY ----------------
def delete_history(request, id):
    if request.method == "POST":
        record = get_object_or_404(AnalysisResult, id=id)
        record.delete()
    return redirect("history")
