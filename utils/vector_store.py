import os
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# Download NLTK data if not already present
try:
    nltk.data.find('corpora/stopwords')
except nltk.downloader.DownloadError:
    nltk.download('stopwords')
try:
    nltk.data.find('tokenizers/punkt')
except nltk.downloader.DownloadError:
    nltk.download('punkt')


class VectorStore:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.vectorizers: dict[str, TfidfVectorizer] = {}
        self.corpus: dict[str, list[str]] = {}
        self.vectors: dict[str, Any] = {} # Storing numpy arrays
        self.url_map: dict[str, dict[str, str]] = {} # agent_key -> url -> content
        self.load_all_data()

    def _preprocess_text(self, text):
        # Convert to lowercase
        text = text.lower()
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Tokenize and remove stopwords
        words = word_tokenize(text)
        words = [word for word in words if word not in stopwords.words('english')]
        return " ".join(words)

    def store_data(self, agent_key: str, url: str, content: str):
        preprocessed_content = self._preprocess_text(content)

        if agent_key not in self.corpus:
            self.corpus[agent_key] = []
            self.url_map[agent_key] = {}

        # Append new content if it's not already there for this URL
        if url not in self.url_map[agent_key]:
            self.corpus[agent_key].append(preprocessed_content)
            self.url_map[agent_key][url] = content # Store original content
            self._revectorize(agent_key)
            self._save_agent_data(agent_key)
        else:
            # If URL already exists, update content and re-vectorize
            old_content_idx = -1
            for i, c in enumerate(self.corpus[agent_key]):
                # This is a bit tricky, ideally we'd map back to original URL
                # For simplicity, we'll re-add and re-vectorize entire corpus
                # A more robust solution might involve mapping indices to URLs
                # For now, if the original content of the URL changes, we update
                if self.url_map[agent_key][url] == content: # Check if content has actually changed
                    return # No update needed
                
                # If content changes, find and replace or just re-add and re-vectorize
                # For simplicity, we'll re-add and update original content
                self.url_map[agent_key][url] = content # Update original content

                # Rebuilding corpus based on url_map to avoid duplicates and keep order
                self.corpus[agent_key] = [self._preprocess_text(self.url_map[agent_key][u]) for u in self.url_map[agent_key]]
                self._revectorize(agent_key)
                self._save_agent_data(agent_key)
                break

    def _revectorize(self, agent_key: str):
        if self.corpus[agent_key]:
            self.vectorizers[agent_key] = TfidfVectorizer()
            self.vectors[agent_key] = self.vectorizers[agent_key].fit_transform(self.corpus[agent_key])
        else:
            self.vectorizers.pop(agent_key, None)
            self.vectors.pop(agent_key, None)

    def retrieve_matched_content(self, agent_key: str, query: str, top_n: int = 1):
        if agent_key not in self.vectorizers or not self.corpus[agent_key]:
            return None

        vectorizer = self.vectorizers[agent_key]
        corpus_vectors = self.vectors[agent_key]

        preprocessed_query = self._preprocess_text(query)
        query_vector = vectorizer.transform([preprocessed_query])

        similarities = cosine_similarity(query_vector, corpus_vectors).flatten()
        
        # Get indices of top_n most similar documents
        # We need to make sure we don't ask for more than available
        top_indices = similarities.argsort()[-min(top_n, len(similarities)):][::-1]

        matched_content = []
        # Reconstruct the original content based on the order of url_map
        original_contents = list(self.url_map[agent_key].values())
        for idx in top_indices:
            if idx < len(original_contents):
                matched_content.append(original_contents[idx])
        
        return " ".join(matched_content) if matched_content else None

    def _save_agent_data(self, agent_key: str):
        # Save corpus and URL map. Vectorizers and vectors are regenerated on load.
        file_path = os.path.join(self.data_dir, f"{agent_key}.json")
        data_to_save = {
            "corpus": self.corpus.get(agent_key, []),
            "url_map": self.url_map.get(agent_key, {})
        }
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=2)

    def load_all_data(self):
        for filename in os.listdir(self.data_dir):
            if filename.endswith(".json"):
                agent_key = filename.replace(".json", "")
                file_path = os.path.join(self.data_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        self.corpus[agent_key] = data.get("corpus", [])
                        self.url_map[agent_key] = data.get("url_map", {})
                        self._revectorize(agent_key) # Re-vectorize on load
                except json.JSONDecodeError as e:
                    print(f"Error loading JSON from {file_path}: {e}")
                except Exception as e:
                    print(f"An unexpected error occurred while loading {file_path}: {e}")
