import google.generativeai as genai
import streamlit as st

# Paste your key here
api_key = st.secrets["Google_API_KEY"] 
genai.configure(api_key=api_key)


print("--- MY AVAILABLE MODELS ---")
for m in genai.list_models():
    # We only want models that can generate text (not image models)
    if 'generateContent' in m.supported_generation_methods:
        print(f"Name: {m.name}")