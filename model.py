import string
import numpy as np
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

# Load lightweight model
import streamlit as st
from sentence_transformers import SentenceTransformer

@st.cache_resource
def load_model():
    return SentenceTransformer("paraphrase-MiniLM-L6-v2")

MODEL = load_model()


class JobRecommendationSystem:

    def __init__(self, jobs_csv):

        self.jobs_df = pd.read_csv(jobs_csv)

        self.jobs_df["job_text"] = (
            self.jobs_df["workplace"].astype(str) + " " +
            self.jobs_df["working_mode"].astype(str) + " " +
            self.jobs_df["position"].astype(str) + " " +
            self.jobs_df["job_role_and_duties"].astype(str) + " " +
            self.jobs_df["requisite_skill"].astype(str)
        )

        self.jobs_texts = self.jobs_df["job_text"].tolist()
        self.job_info = self.jobs_df.copy()

        self.job_embeddings = MODEL.encode(
            self.jobs_texts,
            convert_to_numpy=True
        ).astype("float32")

        faiss.normalize_L2(self.job_embeddings)

        self.dim = self.job_embeddings.shape[1]
        self.index = faiss.IndexFlatIP(self.dim)
        self.index.add(self.job_embeddings)

    def clean_text(self, text):
        return text.lower().translate(
            str.maketrans("", "", string.punctuation)
        ).strip()

    def filter_top_jobs(self, resume_text, top_n=100):

        vectorizer = TfidfVectorizer()
        job_vectors = vectorizer.fit_transform(self.jobs_texts)
        resume_vector = vectorizer.transform([resume_text])

        scores = (job_vectors @ resume_vector.T).toarray().flatten()
        top_indices = np.argsort(scores)[-top_n:]

        return (
            self.job_info.iloc[top_indices].reset_index(drop=True),
            self.job_embeddings[top_indices]
        )

    def recommend_jobs(self, resume_text, top_n=20):

        resume_text = self.clean_text(resume_text)

        filtered_df, filtered_embeddings = self.filter_top_jobs(resume_text)

        resume_embedding = MODEL.encode(
            [resume_text],
            convert_to_numpy=True
        ).astype("float32")

        faiss.normalize_L2(resume_embedding)

        index = faiss.IndexFlatIP(self.dim)
        index.add(filtered_embeddings)

        _, indices = index.search(resume_embedding, top_n)

        results = filtered_df.iloc[indices[0]].to_dict(
            orient="records"
        )

        return {"recommended_jobs": results}
