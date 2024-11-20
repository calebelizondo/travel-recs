from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import torch
from transformers import AutoTokenizer, AutoModel
import pycountry
import re
from typing import List, Dict
import numpy as np
from nltk.corpus import wordnet

class SimilarityService:
    def __init__(self):
        # Load BERT model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
        self.model = AutoModel.from_pretrained('bert-base-uncased')
        
        # Filter and prepare countries list
        self.countries = [
            {"name": country.name, "code": country.alpha_3}
            for country in pycountry.countries
            if "island" not in country.name.lower() and "islands" not in country.name.lower()
        ]

    def expand_query(query_tokens):
        expanded = set()

        for word in query_tokens:
            synonyms = wordnet.synsets(word)
            for syn in synonyms:
                for lemma in syn.lemmas():
                    expanded.add(lemma.name())  
        
        return list(expanded)


    def _get_bert_embedding(self, text: str) -> torch.Tensor:
        # Add special tokens and convert to tensor
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        
        # Get BERT embeddings
        with torch.no_grad():
            outputs = self.model(**inputs)
            
        # Use the [CLS] token embedding as the sentence embedding
        return outputs.last_hidden_state[:, 0, :].squeeze()

    def calculate_similarity(self, text1: str, text2: str) -> float:
        emb1 = self._get_bert_embedding(text1)
        emb2 = self._get_bert_embedding(text2)
        
        similarity = torch.nn.functional.cosine_similarity(emb1.unsqueeze(0), emb2.unsqueeze(0))
        return float(similarity)

    def get_country_scores(self, query: str) -> List[Dict]:
        if not query.strip():
            return []

        scores = []
        for country in self.countries:
            country_name = country["name"]
            score = self.calculate_similarity(country_name, query)
            
            scores.append({
                "name": country_name,
                "code": country["code"],
                "score": score
            })

        return sorted(scores, key=lambda x: x["score"], reverse=True)

# Initialize the service
similarity_service = SimilarityService()

def home(request):
    return HttpResponse("Hello, world!")

def query(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
    query = request.GET.get("query", "").strip()
    if not query:
        return JsonResponse({"error": "missing request arg 'query'"}, status=400)

    try:
        results = similarity_service.get_country_scores(query)
        return JsonResponse({
            "results": [r for r in results if r["score"] > 0]
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)