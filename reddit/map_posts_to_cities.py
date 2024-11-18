import pandas as pd
import json
from geotext import GeoText

csv_file = "./data/travel_posts_20241117_181532.csv"
df = pd.read_csv(csv_file)

post_to_countries = {}

for _, row in df.iterrows():
    post_id = row["Post ID"]
    post_title = row["Title"]
    body = row["Body Text"]
    

    combined_text = f"{post_title} {body}"
    geo = GeoText(combined_text)
    countries = [country.lower() for country in set(geo.countries)]

    if countries: 
        post_to_countries[post_id] = countries

output_file = "./post_to_countries.json"

with open(output_file, "w") as f:
    json.dump(post_to_countries, f, indent=4)

print(f"Saved mapping to {output_file}")