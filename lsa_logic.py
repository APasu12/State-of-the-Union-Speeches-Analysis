import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from text_cleaning import flexible_name_pattern

# File contains Word Frequency Matrix and Singular Valu Decomposition (SVD) processing

def remove_headers(speeches, presidents):
    # Step 4: Remove Header (President Name and Month) from Each Speech
    month_pattern = r'(January|February|March|April|May|June|July|August|September|October|November|December)'
    header_pattern = r'^(?:' + "|".join(flexible_name_pattern(p) for p in presidents) + r')\s+' + month_pattern + r'\s+'
    
    cleaned_speeches = []
    for speech in speeches:
        new_speech = re.sub(header_pattern, '', speech, flags=re.IGNORECASE)
        cleaned_speeches.append(new_speech)
    return cleaned_speeches

def perform_lsa(speeches, n_components=7):
    # Step 5: Compute the Word Frequency Matrix
    vectorizer = TfidfVectorizer(stop_words='english', token_pattern=r'\b[a-zA-Z]+\b')
    X = vectorizer.fit_transform(speeches)
    
    # Step 6: Compute SVD and Perform Latent Semantic Analysis (LSA)
    svd_model = TruncatedSVD(n_components=n_components, random_state=42)
    U = svd_model.fit_transform(X)
    S = svd_model.singular_values_
    VT = svd_model.components_
    
    return vectorizer, U, S, VT, X
