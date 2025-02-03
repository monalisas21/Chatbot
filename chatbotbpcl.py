# -*- coding: utf-8 -*-
"""ChatBotBPCL.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1y-pX3y_HuOBrA0nr5uwFAl59C2fVoPjX
"""





 # Opens file upload dialog

# Install necessary libraries (if not already installed)
import os
import streamlit as st
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util

st.title("BPCL FAQ Chatbot")

# ✅ Remove `!pip install` commands. Instead, install dependencies manually before running:
# pip install streamlit sentence-transformers torch pandas 

# ✅ Check if the CSV file exists before loading
file_path = "BPCL_FAQ_Dataset.csv"

if not os.path.exists(file_path):
    st.error(f"Error: The file '{file_path}' was not found. Please check the file path.")
else:
    # ✅ Load the dataset using Streamlit caching
    @st.cache_data
    def load_data():
        return pd.read_csv(file_path)

    faq_df = load_data()
    st.write("FAQ Dataset Loaded ✅")

    # ✅ Load pre-trained Sentence Transformer model
    @st.cache_resource
    def load_model():
        return SentenceTransformer("all-MiniLM-L6-v2")

    model = load_model()
    st.write("Model Loaded ✅")

    # ✅ Encode all FAQ questions
    faq_embeddings = model.encode(faq_df["Question"].tolist(), convert_to_tensor=True)

    # ✅ Function to get the best matching answer
    def get_best_match(user_question):
        user_embedding = model.encode(user_question, convert_to_tensor=True)
        scores = util.pytorch_cos_sim(user_embedding, faq_embeddings)
        best_match_idx = scores.argmax().item()
        return faq_df.iloc[best_match_idx]["Answer"]

    # ✅ Replace `print()` with Streamlit's `st.write()`
    user_question = st.text_input("Ask me a question:")

    if user_question:
        answer = get_best_match(user_question)
        st.subheader("Bot Response:")
        st.write(answer)
