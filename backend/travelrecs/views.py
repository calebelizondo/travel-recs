from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from gensim.models import Word2Vec
import os
import re
import pycountry


print("loading model")
model_file = './travelrecs/models/google_pca_reduced.model'
model = Word2Vec.load(model_file)
countries = [
    {"name": country.name, "code": country.alpha_3}
    for country in pycountry.countries
    if "island" not in country.name.lower() and "islands" not in country.name.lower()
]
print("done loading model")


# Create your views here.
def home(request):
    return HttpResponse("Hello, world!")


def tokenize(query):
    return [re.sub(r'[^a-zA-Z]', '', word).lower() for word in query.split() if re.sub(r'[^a-zA-Z]', '', word)]


def query(request): 
    if request.method == "GET": 
        query = request.GET.get("query", "").lower()
        if not query: 
            return JsonResponse({"error": "missing request arg 'query'"}, status=400)
        
        tokens = tokenize(query)

        if not tokens:
            return JsonResponse({"error": "query cannot be empty"}, status=400)

    scores = {}
    for country in countries: 
        country_name = country["name"]
        country_code = country["code"]
        country_tokens = tokenize(country_name)
        combined_tokens = country_tokens + tokens
        print(combined_tokens)
        score = 0
        count = 0
        for word1 in country_tokens:
            for word2 in tokens:
                if word1 in model.wv and word2 in model.wv:
                    similarity = model.wv.similarity(word1, word2)
                    score += similarity  # Add similarity instead of multiplying
                    count += 1

        # Normalize the score by the number of comparisons
        # To avoid division by zero, we ensure a minimum of 1 for the count
        scores[country_name] = {"code": country_code, "score": score / max(count, 1)}

    # Sort countries by score in descending order
    sorted_countries = sorted(scores.items(), key=lambda x: x[1]["score"], reverse=True)
    result = [
        {"name": country, "code": details["code"], "score": details["score"]}
        for country, details in sorted_countries
        if details["score"] > 0
    ]

    return JsonResponse({"results": result})
