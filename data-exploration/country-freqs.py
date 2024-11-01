import csv
import json
from collections import defaultdict
import string

# File paths
city_file = './countries.csv'
data_files = ['./travel.csv', './reddit_dot_scores_quality.csv']
output_file = './country_frequencies.json'

# Step 1: Get valid city names from worldcities.csv in lowercase for case-insensitive comparison
valid_countries = set()
with open(city_file, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        valid_countries.add(row['Country'].lower().strip())  # Convert to lowercase

# Step 2: Build dictionaries to hold city frequencies based on post counts
body_freqs = defaultdict(int)
title_freqs = defaultdict(int)

# Step 3: Count city occurrences by checking each post in the data files
translator = str.maketrans("", "", string.punctuation)

count = 0
for file in data_files:
    with open(file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        headers = reader.fieldnames

        # Check if 'title' column exists in the current dataset
        has_title = 'title' in headers

        for row in reader:
            print(count)
            count += 1

            # Process the body text: lowercase, remove punctuation and spaces
            post_text = row['body'].lower().translate(translator).replace(" ", "")
            c_in_body = {c for c in valid_countries if c in post_text}
            for c in c_in_body:
                body_freqs[c] += 1
            
            # Process the title text similarly, if it exists
            if has_title:
                title_text = row['title'].lower().translate(translator).replace(" ", "")
                cities_in_title = {city for city in valid_countries if city in title_text}
                for city in cities_in_title:
                    title_freqs[city] += 1

# Step 4: Save body frequencies as a JSON file
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump({'body_frequencies': body_freqs, 'title_frequencies': title_freqs}, f, ensure_ascii=False, indent=4)

print(f"Countries frequencies have been saved to {output_file}")
