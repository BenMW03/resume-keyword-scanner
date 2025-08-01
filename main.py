import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stopwords.words('english', './nltk_data')

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    return set(t for t in tokens if t not in stop_words)

def load_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    resume_text = load_file('resume.txt')
    job_text = load_file('job_description.txt')

    resume_keywords = clean_text(resume_text)
    job_keywords = clean_text(job_text)

    matching_keywords = resume_keywords.intersection(job_keywords)
    missing_keywords = job_keywords.difference(resume_keywords)

    print("\n🔍 Matching Keywords:")
    print(", ".join(sorted(matching_keywords)))

    print("\n⚠️ Missing Keywords:")
    print(", ".join(sorted(missing_keywords)))

if __name__ == "__main__":
    main()

def normalize_keywords(tokens):
    mapping = {
        "restful": "rest",
        "apis": "api",
        "api": "api",
        "developed": "develop",
        "developing": "develop",
        "developer": "develop",
        "js": "javascript"
    }
    return set(mapping.get(t, t) for t in tokens)