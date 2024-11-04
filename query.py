import os
import gensim
from collections import Counter
from gensim.models import Word2Vec
import numpy as np
import string
import argparse

# Path to directory where country models are stored
model_dir = 'country_models'

# Function to calculate unigram similarity between query and model vocabulary
def calculate_unigram_similarity(query_unigrams, model_vocab):
    # Count matches between query unigrams and model vocabulary words
    match_count = sum(query_unigrams[word] for word in query_unigrams if word in model_vocab)
    # Normalize similarity by the length of the query
    return match_count / len(query_unigrams) if query_unigrams else 0

# Load all model filenames
model_files = [f for f in os.listdir(model_dir) if f.endswith('.model')]

def get_top_5_models(query):
    # Preprocess the query to extract unigrams and remove punctuation
    query_words = query.lower().translate(str.maketrans("", "", string.punctuation)).split()
    query_unigrams = Counter(query_words)  # Unigram counts of words in the query

    model_scores = []
    
    for model_file in model_files:
        # Load each model
        model_path = os.path.join(model_dir, model_file)
        model = Word2Vec.load(model_path)
        
        # Calculate similarity based on unigram overlap with model's vocabulary
        similarity_score = calculate_unigram_similarity(query_unigrams, model.wv.key_to_index)
        
        # Append the score and model filename
        model_scores.append((model_file, similarity_score))

    # Sort by similarity scores in descending order and retrieve the top 5 models
    top_5_models = sorted(model_scores, key=lambda x: x[1], reverse=True)[:5]
    
    # Extract just the filenames of the top 5 models
    top_5_filenames = [model[0] for model in top_5_models]
    return top_5_filenames

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find top 5 country models based on query similarity")
    parser.add_argument("query", type=str, help="Query for finding similar country models")
    
    args = parser.parse_args()
    query = args.query
    
    top_models = get_top_5_models(query)
    print("Top 5 matching models:", top_models)
