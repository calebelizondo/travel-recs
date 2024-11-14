from comcrawl import IndexClient
import pycountry
import os
import re
import pandas as pd

urls = ['https://www.reddit.com/r/travel/', 'https://www.tripadvisor.com/', 'https://www.foodandwine.com/travel/', 'https://www.fodors.com/', 'https://www.roughguides.com/', 'https://www.tasteatlas.com/']
country_names = [country.name.lower() for country in pycountry.countries]

client = IndexClient()

def save_document(country, content):
    folder_path = os.path.join("output", country)
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f"document_{hash(content)}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

i = 0
for url in urls: 
    i += 1
    client.search(url + '*')
    client.results = (pd.DataFrame(client.results)
                  .sort_values(by="timestamp")
                  .drop_duplicates("urlkey", keep="last")
                  .to_dict("records"))

    client.download()

    pd.DataFrame(client.results).to_csv(f"{i}results.csv")
