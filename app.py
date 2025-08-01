import streamlit as st
import re
import nltk
import pdfplumber
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")

custom_stopwords = {
    "experience", "looking", "familiar", "ability", "knowledge", "skills", 
    "including", "etc", "using", "understanding", "proficient", "strong", 
    "with", "in", "working", "and", "or", "of", "an", "a", "the", "is", "are", 
    "has", "have", "will", "must", "be", "we", "our", "their", "you", "your",
    "computing"
}

def load_file(file):
    if file is None:
        return ""
    name = file.name.lower()
    if name.endswith(".pdf"):
        return extract_text_from_pdf(file)
    elif name.endswith(".txt"):
        return file.read().decode("utf-8")
    else:
        return ""

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words("english")).union(custom_stopwords)
    filtered = [t for t in tokens if t not in stop_words]
    return normalize_keywords(filtered)

def normalize_keywords(tokens):
    mapping = {
        "restful": "rest",
        "apis": "api",
        "api": "api",
        "developed": "develop",
        "developing": "develop",
        "developer": "develop",
        "js": "javascript",
        "engineering": "engineer"
    }
    return set(mapping.get(t, t) for t in tokens)

st.title("📄 Resume Keyword Scanner")

st.markdown("Upload your **resume** and a **job description** to see how well they match.")

resume_file = st.file_uploader("Upload your resume (.pdf or .txt)", type=["pdf", "txt"])
job_file = st.file_uploader("Upload job description (.pdf or .txt)", type=["pdf", "txt"])

if resume_file and job_file:
    resume_text = load_file(resume_file)
    job_text = load_file(job_file)

    resume_keywords = clean_text(resume_text)
    job_keywords = clean_text(job_text)

    matching = resume_keywords & job_keywords
    missing = job_keywords - resume_keywords

    score = len(matching) / len(job_keywords) * 100 if job_keywords else 0

    st.subheader(f"✅ Match Score: {score:.2f}%")

    st.markdown("### 🔍 Matching Keywords")
    if matching:
        st.write(", ".join(sorted(matching)))
    else:
        st.write("None found")

    st.markdown("### ⚠️ Missing Keywords")
    if missing:
        st.write(", ".join(sorted(missing)))
    else:
        st.write("None found")