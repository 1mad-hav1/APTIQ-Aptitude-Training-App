


import pathlib
import textwrap
import google.generativeai as genai
import os
from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Google Gemini API Key
GOOGLE_API_KEY = 'AIzaSyBYMXKtvKw2gFgw5c1dlC1fyEuenZrQu2U'
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
bert_model = BertForSequenceClassification.from_pretrained("bert-base-uncased")

def generate_mcq(category, difficulty, num_questions):
    """Generate multiple MCQs based on category, difficulty level, and number of questions."""
    mcq_list = []
    for _ in range(num_questions):
        prompt = (f"Generate a {difficulty} multiple-choice question (MCQ) for {category} reasoning. "
                  f"Include four answer choices, specify the correct answer, and provide a detailed explanation "
                  f"for why the correct answer is right.")
        response = model.generate_content(prompt)
        mcq_list.append(response.text if response else "Error generating question.")
    return mcq_list

def analyze_mcq_with_bert(mcq):
    """Analyze the MCQ using BERT for language understanding."""
    inputs = tokenizer(mcq, return_tensors="pt", truncation=True, padding=True)
    outputs = bert_model(**inputs)
    return outputs.logits.detach().numpy()

if __name__ == '__main__':
    category = input("Choose MCQ category (Logical, Verbal, Cognitive): ")
    difficulty = input("Choose difficulty level (Easy, Medium, Hard): ")
    num_questions = int(input("Enter the number of MCQs to generate: "))
    
    mcq_questions = generate_mcq(category, difficulty, num_questions)
    
    # print(mcq_questions)
    
    for idx, mcq in enumerate(mcq_questions, 1):
        print(f"\nGenerated MCQ {idx}:\n", mcq)
        bert_analysis = analyze_mcq_with_bert(mcq)
        print("\nBERT Analysis Output:\n", bert_analysis)
