"""
Description: Task 2 - Text analysis with Regex and Zip archiving.
Lab Number: 1
Author: Filipp Filimonov
Date: 2026-04-16
"""
import re, zipfile, os

class TextAnalyzer:
    def __init__(self, path):
        self.path = path
        if not os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as f:
                f.write("Hello! This is a test pbbbc string. :---))) Uppercase letters: ABC.")
        with open(path, 'r', encoding='utf-8') as f: self.text = f.read()

    def analyze_general(self):
        sents = re.split(r'[.!?]+', self.text.strip())
        words = re.findall(r'\b\w+\b', self.text)
        smileys = re.findall(r'[:;]-*[\(\)\[\]]+', self.text)
        return {
            "Sentences": len([s for s in sents if s]),
            "Words": len(words),
            "Smileys": len(smileys)
        }

    def analyze_variant(self):
        modified = re.sub(r'p+b{2,}c+', 'ddd', self.text)
        words = re.findall(r'\b[A-Za-z]+\b', self.text)
        return {
            "Uppercase": re.findall(r'[A-Z]', self.text),
            "Modified": modified,
            "Sorted": sorted(words, key=len, reverse=True)
        }

def save_and_archive_results(data, txt, arc):
    with open(txt, 'w', encoding='utf-8') as f:
        for k, v in data.items(): f.write(f"{k}: {v}\n")
    with zipfile.ZipFile(arc, 'w') as zf: zf.write(txt)
    print(f"Results archived in {arc}")