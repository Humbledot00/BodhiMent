import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from collections import Counter

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    # Process the text with spaCy
    doc = nlp(text)
    
    # Filter out stopwords and punctuation
    keywords = [token.text for token in doc if not token.is_stop and not token.is_punct]
    
    # Find the most common keywords
    keyword_freq = Counter(keywords)
    
    # Get the top N keywords
    top_keywords = keyword_freq.most_common(10)
    
    # Return only the keywords, not their frequencies
    return [keyword for keyword, freq in top_keywords]

# Sample input paragraph
text = """
Chhatrapati Shivaji Maharaj was a revered Indian warrior king and the founder of the Maratha Empire in western India in the 17th century. Born in 1630 at Shivneri Fort, he was a master tactician and an accomplished military leader who established a competent and progressive civil rule with well-structured administrative organizations. Shivaji is renowned for his innovative military tactics, which leveraged strategic geography, guerrilla warfare, and his navy to defend his kingdom against the Mughal Empire and other adversaries.
"""

# Extract keywords
keywords = extract_keywords(text)
print("Extracted Keywords:", keywords)

