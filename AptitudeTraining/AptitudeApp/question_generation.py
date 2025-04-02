import re
import google.generativeai as genai
import torch
from transformers import BertTokenizer, BertForSequenceClassification, pipeline
from random import choice
from .models import Questions 

# Google Gemini API Key
GOOGLE_API_KEY = 'AIzaSyBYMXKtvKw2gFgw5c1dlC1fyEuenZrQu2U'
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize BERT model and tokenizer for grammatical correctness checking
bert_tokenizer = BertTokenizer.from_pretrained("textattack/bert-base-uncased-CoLA")
bert_model = BertForSequenceClassification.from_pretrained("textattack/bert-base-uncased-CoLA")

# Initialize BART for grammatical correction
grammar_corrector = pipeline("text2text-generation", model="facebook/bart-large-cnn")

def check_grammar(sentence):
    """Check grammatical correctness using BERT"""
    inputs = bert_tokenizer(sentence, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = bert_model(**inputs)
    prediction = torch.argmax(outputs.logits, dim=1).item()

    return prediction == 1  # 1 = Correct, 0 = Incorrect

def correct_grammar(sentence):
    """Correct grammar using BART"""
    corrected_text = grammar_corrector(sentence, max_length=100)[0]['generated_text']
    return corrected_text

def get_random_question(category, difficulty):
    """Fetch a random question from the database based on category and difficulty."""
    filtered_questions = Questions.objects.filter(
        question_type=category, 
        difficulty=difficulty
    )

    if not filtered_questions.exists():
        return None  

    selected_question = choice(filtered_questions)

    question_data = {
        "question": selected_question.question,
        "options": {
            "a": selected_question.optiona,
            "b": selected_question.optionb,
            "c": selected_question.optionc,
            "d": selected_question.optiond
        },
        "answer": selected_question.answer,
        "explanation": selected_question.answer_description
    }
    
    return question_data

def generate_mcq(category, difficulty, num_questions):
    """Generate multiple MCQs using a retrieved question as reference."""
    mcq_list = []
    
    for _ in range(num_questions):
        reference_question = get_random_question(category, difficulty)

        prompt = (f"Using the following question as a reference, generate a similar question "
                  f"but with different values and choices, ensuring it remains a {difficulty} "
                  f"level question in {category} reasoning.\n\n"
                  f"Reference Question: {reference_question['question']}\n"
                  f"Options: {reference_question['options']}\n"
                  f"Correct Answer: {reference_question['answer']}\n"
                  f"Explanation: {reference_question['explanation']}\n\n"
                  f"Ensure the new question follows this format:\n"
                  f"<MCQ question text>\n"
                  f"a) <Option A>\n"
                  f"b) <Option B>\n"
                  f"c) <Option C>\n"
                  f"d) <Option D>\n"
                  f"Correct Answer: <Correct option letter (a/b/c/d)>\n"
                  f"Explanation: <Detailed explanation for the correct answer>\n\n"
                  f"Important: Avoid using special characters, emojis, or unsupported symbols. "
                  f"Ensure the output is plain text.")

        response = model.generate_content(prompt)

        generated_mcq = response.text if response else "Error generating question."

        # Extract question text from MCQ
        question_text, _, _, _ = parse_mcq(generated_mcq)

        # *Check grammar correctness*
        if not check_grammar(question_text):
            print(f"Grammar issue detected in: {question_text}")
            corrected_question = correct_grammar(question_text)
            print(f"Corrected Question: {corrected_question}")

            # Replace the incorrect question with the corrected one in the MCQ
            generated_mcq = generated_mcq.replace(question_text, corrected_question)

        mcq_list.append(generated_mcq)
    
    return mcq_list

def parse_mcq(mcq_text):
    """Parse MCQ text to extract the question, options, correct answer, and explanation."""
    question_pattern = r"(.*?)(?=\n[a-d]\))"
    option_pattern = r"([a-d])\) (.*)"
    answer_pattern = r"Correct Answer: ([a-d])"
    explanation_pattern = r"Explanation:\s*(.*)"

    question = re.search(question_pattern, mcq_text, re.DOTALL)
    options = re.findall(option_pattern, mcq_text)
    answer = re.search(answer_pattern, mcq_text)
    explanation = re.search(explanation_pattern, mcq_text, re.DOTALL)

    question_text = question.group(1).strip() if question else "No question found"
    options_dict = {opt[0]: opt[1] for opt in options}
    correct_answer = answer.group(1) if answer else "No answer found"
    explanation_text = explanation.group(1).strip() if explanation else "No explanation found"

    return question_text, options_dict, correct_answer, explanation_text