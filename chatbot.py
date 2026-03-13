import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer

import streamlit as st
from sentence_transformers import SentenceTransformer

@st.cache_resource
def load_model():
    return SentenceTransformer("paraphrase-MiniLM-L6-v2")

MODEL = load_model()


class CareerChatbot:

    def __init__(self, faq_file):

        self.df = pd.read_csv(faq_file)
        self.df.fillna("", inplace=True)

        self.questions = self.df["question"].tolist()
        self.answers = self.df["answer"].tolist()

        self.embeddings = MODEL.encode(
            self.questions,
            convert_to_numpy=True
        ).astype("float32")

        faiss.normalize_L2(self.embeddings)

        self.index = faiss.IndexFlatIP(self.embeddings.shape[1])
        self.index.add(self.embeddings)

    def ask(self, question):

        vec = MODEL.encode(
            [question],
            convert_to_numpy=True
        ).astype("float32")

        faiss.normalize_L2(vec)

        _, idx = self.index.search(vec, 1)
        return self.answers[idx[0][0]]
