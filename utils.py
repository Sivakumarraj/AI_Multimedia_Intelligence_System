# utils.py
import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    return text.strip()

def format_result(summary, caption, similarity):
    return {
        "Text Summary": summary,
        "Image Caption": caption,
        "Image-Text Similarity": round(similarity, 2)
    }
