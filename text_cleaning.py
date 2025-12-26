import requests
from bs4 import BeautifulSoup
import re

def get_cleaned_corpus(url):
    # Step 1: Load and Clean the Corpus
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    # Remove bold (<b>) and hyperlink (<a>) tags
    for tag in soup.find_all(['b', 'a']):
        tag.decompose()

    full_text = soup.get_text()
    text_no_numbers = re.sub(r'\d+', '', full_text)

    lines = text_no_numbers.splitlines()
    filtered_lines = [line for line in lines if "Project Gutenberg" not in line]

    filtered_text = " ".join(filtered_lines)
    filtered_text = re.sub(r'\s+', ' ', filtered_text).strip()

    # Remove audience reactions
    filtered_text = re.sub(
        r'\([^)]*\b(applause|laughter|cheer|reaction)\b[^)]*\)',
        '', filtered_text, flags=re.IGNORECASE
    )
    return filtered_text

def flexible_name_pattern(name):
    # Function to build a flexible regex pattern for a president's name
    parts = name.split()
    flexible_parts = []
    for part in parts:
        if len(part) == 1: 
            flexible_parts.append(part + r'\.?')
        else:
            flexible_parts.append(re.escape(part))
    return r'\s+'.join(flexible_parts)

def extract_individual_speeches(filtered_text, presidents):
    # Step 2: Extract the Relevant Corpus Text
    start_marker = "HARRY S. TRUMAN"
    end_marker = "business. God bless America."
    
    start_match = re.search(re.escape(start_marker), filtered_text, flags=re.IGNORECASE)
    end_match = re.search(re.escape(end_marker), filtered_text, flags=re.IGNORECASE)
    
    start_index = start_match.start()
    end_index = end_match.end()
    corpus_text = filtered_text[start_index:end_index]

    # Step 3: Split the Corpus into Individual Speeches
    pattern = "(" + "|".join(flexible_name_pattern(p) for p in presidents) + ")"
    parts = re.split(pattern, corpus_text, flags=re.IGNORECASE)

    speeches = []
    i = 1
    while i < len(parts):
        president = parts[i].strip()
        if i+1 < len(parts):
            speech_text = president + " " + parts[i+1].strip()
            speeches.append(speech_text)
        i += 2
    return speeches
