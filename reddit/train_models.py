import pandas as pd
import json
from gensim.models import Word2Vec
from geotext import GeoText

posts_file = "./data/travel_posts_20241117_181532.csv"
comments_file = "./data/travel_comments_20241117_181532.csv"
post_reddit_dataset = "./data/reddit_dot_scores_quality.csv"
mapping_file = "./post_to_countries.json"
output_dir = "./models/"

posts_df = pd.read_csv(posts_file)
comments_df = pd.read_csv(comments_file)
reddit_df = pd.read_csv(post_reddit_dataset)

country_posts = {}
country_comments = {}
post_to_country = {}

with open(mapping_file, "r") as f: 
    post_to_country = json.load(f)

for _, row in posts_df.iterrows(): 
    post_id = row["Post ID"]
    post_title = row["Title"]
    body = row["Body Text"]

    if post_id in post_to_country: 
        combined_text = f"{post_title} {body}"

        for country in post_to_country[post_id]:
            if country not in country_posts: 
                country_posts[country] = []
            country_posts[country].append(combined_text)


for _, row in comments_df.iterrows(): 
    post_id = row["Post ID"]
    body = row["Body"]

    if post_id in post_to_country: 
        
        for country in post_to_country[post_id]:
            if country not in country_posts:
                country_posts[country] = []
            country_posts[country].append(combined_text)


for _, row in reddit_df.iterrows():
    
    title = row["title"]
    body = row["body"]

    combined_text = f"{title} {body}"

    geo = GeoText(combined_text)
    countries = [country.lower() for country in set(geo.countries)]

    for country in countries: 
        if country not in country_posts:
                country_posts[country] = []
        country_posts[country].append(combined_text)

for country, posts in country_posts.items():
    print(f"training model {country}")

    tokenized_posts = [post.split() for post in posts]

    model = Word2Vec(
        sentences=tokenized_posts,
        vector_size=100,
        window=5,
        min_count=2,
        workers=4,
    )

    model.save(f"{output_dir}{country}.model")
    print(f"saving model {country}")