# AI-Based Resume Screening, Job Description Matching & Candidate Ranking System

## Overview
This project is a **Django-based AI application** that analyzes resumes against a given **Job Description (JD)** using **Natural Language Processing (NLP)**.  
It calculates a **match percentage**, provides an **AI verdict**, identifies **skill gaps**, generates **resume improvement suggestions**, ranks candidates, and maintains an **analysis history** with delete functionality.

The system simulates the core features of an **Applicant Tracking System (ATS)**.

---

## Features
- Upload resumes in **PDF format**
- Paste **custom Job Description**
- **AI-based matching** using TF-IDF & Cosine Similarity
- **Match Percentage**
- **AI Verdict**: Strong / Moderate / Weak Match
- **Skill Gap Analysis** (matched & missing skills)
- **AI Resume Improvement Suggestions**
- **Candidate Ranking** (multiple resumes vs one JD)
- **Analysis History** with secure delete option
- Clean, responsive UI using **Bootstrap**

---

## AI Techniques Used
- **Natural Language Processing (NLP)**
- **TF-IDF (Term Frequency–Inverse Document Frequency)**
- **Cosine Similarity**
- **Rule-Based AI** for verdict and recommendations (Explainable AI)

> This project uses applied NLP and statistical machine learning (not deep learning), making it reliable and explainable.

---

## Technologies
- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, Bootstrap
- **AI/ML:** Scikit-learn
- **PDF Processing:** PyPDF2
- **Database:** SQLite
- **Version Control:** Git, GitHub

---

## Project Structure
