import csv
import string
import gensim
import os
from gensim.models import Word2Vec
from collections import defaultdict

translator = str.maketrans("", "", string.punctuation)

data_files = ["./data-exploration/reddit_dot_scores_quality.csv"]
country_file = "./data-exploration/countries.csv"
model_output_dir = "./country_models"

os.makedirs(model_output_dir, exist_ok=True)

valid_countries = set()
with open(country_file, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        valid_countries.add(row['Country'].lower().strip())  # Convert to lowercase

country_posts = defaultdict(list)

for file in data_files: 
    with open(file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames

        has_title = 'title' in headers

        for row in reader:
            # Process body text
            post_text = row['body'].lower().translate(translator).split()  # Tokenize and remove punctuation
            mentioned_countries = {c for c in valid_countries if c in post_text}

            # Add title text to post_text if available
            if has_title:
                title_text = row['title'].lower().translate(translator).split()
                mentioned_countries.update({c for c in valid_countries if c in title_text})
                post_text.extend(title_text)

            # Add the post's words (unigrams) to each mentioned country's list
            for country in mentioned_countries:
                country_posts[country].append(post_text)

# Train and save a Word2Vec model for each country
for country, sentences in country_posts.items():
    # Train Word2Vec model on the sentences associated with each country
    model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, sg=1)
    
    # Save the model in a format compatible with other applications
    model_path = os.path.join(model_output_dir, f"{country}.model")
    model.save(model_path)
    print(f"Model saved for {country} at {model_path}")