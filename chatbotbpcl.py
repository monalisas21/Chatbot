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

st.title("BharatGas Services FAQ Chatbot")

# ✅ Check if the dataset exists before loading
file_path = "bpcl_chatbot_newdataset.csv"

if not os.path.exists(file_path):
    st.error(f"Error: The file '{file_path}' was not found. Please check the file path.")
else:
    # ✅ Load the dataset with caching
    @st.cache_data
    def load_data():
        return pd.read_csv(file_path)

    faq_df = load_data()
    st.write("FAQ Dataset Loaded ✅")

    # ✅ Load pre-trained Sentence Transformer model with caching
    @st.cache_resource
    def load_model():
        return SentenceTransformer("all-MiniLM-L6-v2")

    model = load_model()
    st.write("Model Loaded ✅")

    # ✅ Encode all FAQ questions
    faq_questions = faq_df["Question"].str.lower().tolist()
    faq_embeddings = model.encode(faq_questions, convert_to_tensor=True)

    # ✅ Define explicit greeting responses
    greeting_responses = {
        "hi": "Hello! How can I assist you with BPCL services?",
        "hello": "Hi there! How can I help you today?",
        "hey": "Hey! What can I do for you?",
        "good morning": "Good morning! How may I assist you?",
        "good afternoon": "Good afternoon! How can I help?",
        "good evening": "Good evening! How can I assist you?"
    }

    # ✅ Function to get the best matching answer
    def get_best_match(user_question):
        user_question = user_question.lower().strip()  # Normalize input
        
        # ✅ Check for greetings explicitly
        if user_question in greeting_responses:
            return greeting_responses[user_question]
        
        user_embedding = model.encode(user_question, convert_to_tensor=True)
        scores = util.pytorch_cos_sim(user_embedding, faq_embeddings)

        best_match_idx = scores.argmax().item()
        best_score = scores[0][best_match_idx].item()

        # ✅ Set a similarity threshold to filter poor matches
        threshold = 0.5  # Adjust as needed
        if best_score < threshold:
            return "I'm sorry, I couldn't find an exact answer. Please try rephrasing your question."

        return faq_df.iloc[best_match_idx]["Answer"]

    # ✅ Get user input from Streamlit
    user_question = st.text_input("Ask me a question:")

    if user_question:
        answer = get_best_match(user_question)
        st.subheader("Bot Response:")
        st.write(answer)
