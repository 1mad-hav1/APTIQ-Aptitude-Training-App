import os
import joblib
import numpy as np

# Load the trained model
model_path = os.path.abspath(os.path.join('AptitudeTraining', 'static', 'decision_tree_model.pkl'))
print("Loading model from:", model_path)

try:
    model = joblib.load(model_path)
    print("Model loaded successfully.")
except Exception as e:
    print("Error loading model:", str(e))
    exit()

# Function to classify performance
def classify_performance(accuracy, improvement_rate, difficulty_score):
    if improvement_rate == "NA":
        improvement_rate = np.nan
    
    input_data = np.array([[accuracy, improvement_rate, difficulty_score]])
    prediction = model.predict(input_data)
    return prediction[0]

# Sample test cases
test_cases = [
    (2,10,18),   # High accuracy, good improvement rate, high difficulty
]

# Run tests
for idx, (accuracy, improvement_rate, difficulty_score) in enumerate(test_cases, 1):
    predicted_class = classify_performance(accuracy, improvement_rate, difficulty_score)
    print(f"Test Case {idx}: Accuracy={accuracy}, Improvement Rate={improvement_rate}, Difficulty={difficulty_score} -> Predicted Performance Level: {predicted_class}")
