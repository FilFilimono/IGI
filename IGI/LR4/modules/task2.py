import re
import zipfile
import os
from utils.mixins import InfoMixin

"""
Purpose: Text analysis using RegEx and Zip archiving
Lab: #X (Task 2)
Version: 1.0
Author: [Your Name]
Date: 2026-04-29
"""

class TextProcessor(InfoMixin):
    def __init__(self, content):
        self.content = content

class AdvancedAnalyzer(TextProcessor):
    def __init__(self, content):
        super().__init__(content)

    def get_sentences_count(self):
    
        declarative = len(re.findall(r'[^!?](\.|\.\.\.)(?=\s|[A-ZА-Я]|$)', self.content))
        interrogative = len(re.findall(r'\?', self.content))
        exclamatory = len(re.findall(r'!', self.content))
        return declarative, interrogative, exclamatory

    def get_average_lengths(self):
        words = re.findall(r'\b\w+\b', self.content)
        total_words = len(words)
        if total_words == 0: return 0, 0
        
        avg_word_len = sum(len(w) for w in words) / total_words
        
        sentences = re.split(r'[.!?]+', self.content)
        sentences = [s.strip() for s in sentences if s.strip()]
        total_sent = len(sentences)
        
        avg_sent_len = 0
        if total_sent > 0:
            total_chars_in_words = sum(len("".join(re.findall(r'\w+', s))) for s in sentences)
            avg_sent_len = total_chars_in_words / total_sent
            
        return avg_sent_len, avg_word_len

    def count_smileys(self):
        pattern = r'[;:][-]*(\(|\)|\[|\])\1*'
        matches = re.finditer(pattern, self.content)
        count = 0
        for match in matches:
            count += 1
        return count

    def individual_task_processing(self):
        cap_letters = "".join(re.findall(r'[A-Z]', self.content))
        modified_text = re.sub(r'p+b{2,}c+', 'ddd', self.content)
        
        words = re.findall(r'\b\w+\b', self.content)
        short_words_count = len([w for w in words if len(w) < 5])
        
        d_words = re.findall(r'\b\w*d\b', self.content, re.IGNORECASE)
        shortest_d = min(d_words, key=len) if d_words else "None"
        
        sorted_words = sorted(words, key=len, reverse=True)
        
        return {
            "capitals": cap_letters,
            "modified": modified_text,
            "short_count": short_words_count,
            "shortest_d": shortest_d,
            "sorted_words": sorted_words
        }

def run_task_2():
    print("\n--- Task 2: Text Analysis ---")
    
    input_file = os.path.join("data", "input.txt")
    if not os.path.exists(input_file):
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write("Hello world! This is a test. pbbbc. Is it working? Yes!! :) ;--]]")

    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    analyzer = AdvancedAnalyzer(text)
    
    dec, inter, excl = analyzer.get_sentences_count()
    avg_s, avg_w = analyzer.get_average_lengths()
    smiles = analyzer.count_smileys()
    indiv = analyzer.individual_task_processing()

    result_content = (
        f"Total sentences: {dec + inter + excl}\n"
        f"Types: Dec: {dec}, Int: {inter}, Excl: {excl}\n"
        f"Avg sentence len: {avg_s:.2f}, Avg word len: {avg_w:.2f}\n"
        f"Smileys: {smiles}\n"
        f"Capitals: {indiv['capitals']}\n"
        f"Words < 5: {indiv['short_count']}\n"
        f"Shortest ending in 'd': {indiv['shortest_d']}\n"
        f"Modified text: {indiv['modified']}\n"
    )
    
    print(result_content)
    
    res_file = os.path.join("data", "results.txt")
    with open(res_file, 'w', encoding='utf-8') as f:
        f.write(result_content)
        f.write("\nWords sorted by length:\n")
        f.write(", ".join(indiv['sorted_words']))

    zip_name = os.path.join("data", "results.zip")
    with zipfile.ZipFile(zip_name, 'w') as zip_f:
        zip_f.write(res_file, arcname="results.txt")
    
    print(f"\nArchived to {zip_name}")
    with zipfile.ZipFile(zip_name, 'r') as zip_f:
        for info in zip_f.infolist():
            print(f"File in archive: {info.filename}, Size: {info.file_size} bytes")