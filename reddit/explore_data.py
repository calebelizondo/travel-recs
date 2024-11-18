import os
from gensim.models import Word2Vec

models_dir = "./models/"
model_files = [f for f in os.listdir(models_dir) if f.endswith('.model')]

for model_file in model_files: 
    model_path = os.path.join(models_dir, model_file)
    print("Loading model: {model_file}")
    model = Word2Vec.load(model_path)
    
    vocab_size = len(model.wv)
    
    country = model_file.replace("_word2vec.model", "")
    print(f"Country: {country}, Vocabulary size: {vocab_size}")