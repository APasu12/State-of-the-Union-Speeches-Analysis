# State-of-the-Union-Speeches-Analysis

Source: https://www.gutenberg.org/cache/epub/5050/pg5050-images.html

Each Speech begins with the words "State of the Union Address" followed by the President's name and the date. This text is ignored in the analysis to ensure that the results are not skewed. Numbers, bolded text, hyperlinks, audience reactions, and information about Project Gutenberg are ignored in the analysis.

# Project Overview
Transforming raw text from Project Gutenberg into a structured semantic model:
* **Data Extraction**: Scrapes the full text and uses custom regex patterns to isolate individual speeches based on presidential names (from Harry S. Truman to George W. Bush).
* **Text Cleaning**: Removes HTML tags, numbers, audience reactions (such as "(Applause)"), and Project Gutenberg metadata to ensure a clean word frequency matrix.
* **Mathematical Modeling**: 
    * Computes a Term Frequency-Inverse Document Frequency (TF-IDF) matrix to weight important terms.
    * Performs Singular Value Decomposition (SVD) to reduce the high-dimensional term-document matrix into latent semantic topics.
* **Visual Analysis**: Speeches are mapped into a 2D LSA space, and heatmaps are generated to track "Mood-Word Intensity" using Hope, Unity, Sorrow, and Fear labeled categories.

# Analysis
One of the highlighting features of the Mood-Word Intensity per Speech Heatmap is that Document 53 (State of the Union Speech of 2002) included an abnormally large amount of words that created a sense of "unity." This was President Bush's address to Congress following the 9/11 attacks (the "unity" tone makes sense), and overall, this heatmap allowed me to identify patterns in the mood of these speeches. The dictionary of words that defined these tones can be expanded upon in future analyses to create an enhanced heatmap.

Additionally, there is a very strong, positive correlation between Speeches 1-10 (1950-1960) and Speeches 35-45 (1984-1994), meaning that these speeches had very similar tones.

Single letters like "t", "f", and "s" were included in the Top Term graphs. This is likely due to high usage of contractions, such as in "wouldn't" or "China's" where the program causes "t" and "s" to be processed as separate words. This is very interesting to see that the program isn't able to differentiate between conjunctions (without explicitly writing the code for it). I purposely left the program as it is now since I wanted to see if this would impact the "Top Terms" results, which it ultimately did.

# How to Use
1. Install dependencies: `pip install -r requirements.txt`
2. Run the analysis: `python main.py`
