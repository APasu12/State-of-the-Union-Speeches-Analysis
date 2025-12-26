# US State of the Union Speeches: LSA Analysis (1950-2008)


# 1. Loads the full State of the Union speeches text from Project Gutenberg.
# 2. Cleans the text by removing HTML bold tags, hyperlinks, numbers, audience reactions (e.g., "(Applause)"), and Project Gutenberg meta-information.
# 3. Joins lines using a space (instead of newline) and normalizes whitespace.
# 4. Extracts the corpus from Harry S. Truman's speech until the phrase "business. God bless America."
# 5. Splits the corpus into individual speeches based on presidential names using a flexible regex.
# 6. For each speech, removes the leading header consisting of the president’s name and the month name.
# 7. Prints debugging info to verify the cleaned speeches.
# 8. Computes a TF-IDF word frequency matrix.
# 9. Applies SVD to perform Latent Semantic Analysis (LSA) and extracts latent topics.
# 10. Displays the top terms per topic and a 2D scatter plot of document projections.

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from text_cleaning import get_cleaned_corpus, extract_individual_speeches
from lsa_logic import remove_headers, perform_lsa

# Setup data
url = "https://www.gutenberg.org/cache/epub/5050/pg5050-images.html"
presidents = ["HARRY S TRUMAN", "DWIGHT D EISENHOWER", "JOHN F KENNEDY", "LYNDON B JOHNSON", 
              "RICHARD NIXON", "GERALD FORD", "JIMMY CARTER", "RONALD REAGAN", 
              "GEORGE H W BUSH", "BILL CLINTON", "GEORGE W BUSH"]

# Execute pipeline
filtered_text = get_cleaned_corpus(url)
raw_speeches = extract_individual_speeches(filtered_text, presidents)
speeches = remove_headers(raw_speeches, presidents)
vectorizer, U, S, VT, X = perform_lsa(speeches)

# Visualize LSA Space
plt.figure(figsize=(8, 6))
plt.scatter(U[:, 0], U[:, 1], marker='o', edgecolor='k')
for idx, coord in enumerate(U):
    plt.annotate(f"Doc {idx+1}", (coord[0], coord[1]))
plt.title("Speeches in LSA Space (First Two Components)")
plt.show()

# Mood Analysis Heatmap
moods = {
    "Hope": ["hope", "optimism", "promise", "future", "dream"],
    "Unity": ["together", "united", "union", "common", "team"],
    "Sorrow": ["sorrow", "grief", "sad", "mourning", "loss"],
    "Fear": ["fear", "danger", "threat", "risk", "crisis"]
}

counts = { m: [] for m in moods }
for speech in speeches:
    text = speech.lower()
    total_words = len(text.split())
    for mood, words in moods.items():
        c = sum(text.count(w) for w in words)
        counts[mood].append(c / total_words * 10000)

df = pd.DataFrame(counts, index=[f"Doc {i+1}" for i in range(len(speeches))])
plt.figure(figsize=(14,10))
sns.heatmap(df, cmap="coolwarm", annot=True, fmt=".1f")
plt.title("Mood‑Word Intensity per Speech (per 10k words)")
plt.show()
