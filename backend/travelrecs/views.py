from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import pycountry
import re
from typing import List, Dict
import nltk
from nltk.data import find
from nltk import download
import os
from rank_bm25 import BM25Okapi
import pickle
import json

try:
    find('corpora/wordnet.zip')
except LookupError:
    download('wordnet')

#load data and alpha_3 code for each country
index_dir = "./travelrecs/bm25_index/"
corpus_file = os.path.join(index_dir, "bm25_corpus.pkl")
metadata_file = os.path.join(index_dir, "metadata.json")
country_info_file = os.path.join(index_dir, "country_info.json")

bm25 = None
country_to_index = {}
country_metadata = {}
country_info = {}

def expand_query(query: str, max_synonyms: int = 1) -> List[str]:
    query_tokens = query.split()
    expanded_query = set(query_tokens)  

    for token in query_tokens:
        synonyms = []
        for synset in nltk.corpus.wordnet.synsets(token):
            for lemma in synset.lemmas():
                synonym = lemma.name().replace("_", " ").lower()
                if synonym != token and synonym not in synonyms:
                    synonyms.append(synonym)
                    if len(synonyms) >= max_synonyms:
                        break
            if len(synonyms) >= max_synonyms:
                break

        expanded_query.update(synonyms)

    return list(expanded_query)

def clean_text(text: str) -> str:
    text = re.sub(r"[^a-zA-Z\s]", "", text.lower())
    return re.sub(r"\s+", " ", text).strip()

def get_country_alpha3(country_name: str) -> str:
    try:
        country = pycountry.countries.lookup(country_name)
        return country.alpha_3
    except LookupError:
        return None
    
def load_bm25_index():
    global bm25, country_to_index, country_metadata, country_info

    with open(corpus_file, "rb") as f:
        tokenized_corpus = pickle.load(f)

    with open(metadata_file, "r") as f:
        country_metadata = json.load(f)

    with open(country_info_file, "r") as f:
        country_info = json.load(f)

    # Rebuild the BM25 index
    corpus = []
    for idx, country in enumerate(country_metadata["countries"]):
        for document in tokenized_corpus[country]:
            corpus.append(document)
            country_to_index[len(corpus) - 1] = country

    bm25 = BM25Okapi(corpus, k1=1.2, b=.9)

load_bm25_index()

def home(request):
    return HttpResponse("Hello, world!")

def query(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
    query = request.GET.get("query", "").strip()
    if not query:
        return JsonResponse({"error": "missing request arg 'query'"}, status=400)
    
    #perform bm_25 on each country doc, return list of countries, their score and alpha_3 codes in order
    # Expand the user query
    expanded_query = expand_query(query)
    print(expanded_query)
    tokenized_query = clean_text(" ".join(expanded_query)).split()

    # Perform BM25 scoring
    scores = bm25.get_scores(tokenized_query)

    ranked_results = {}
    for idx, score in enumerate(scores):
        country = country_to_index[idx]
        ranked_results[country] = ranked_results.get(country, 0) + score

    sorted_results = sorted(ranked_results.items(), key=lambda x: x[1], reverse=True)

    results = []
    for country, score in sorted_results:
        alpha_3 = get_country_alpha3(country)
        results.append({"name": country, "score": score, "code": alpha_3, "info": country_info[country]})

    return JsonResponse({"results": results}, safe=False)