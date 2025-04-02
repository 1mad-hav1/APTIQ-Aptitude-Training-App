import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Load the dataset (Ensure it has columns: accuracy, improvement_rate, difficulty_score, performance_level)
data_path = os.path.abspath(os.path.join('AptitudeTraining', 'static', 'performance_data.csv'))
print("Resolved Path:", data_path)
data = pd.read_csv(data_path)

# Handle missing or "NA" values in improvement_rate
data['improvement_rate'] = data['improvement_rate'].replace("NA", np.nan).astype(float)

# Define feature columns and target variable
features = ['accuracy', 'improvement_rate', 'difficulty_score']
target = 'performance_level'

# Drop rows where improvement_rate is NaN (if necessary) or use only accuracy and difficulty score for those cases
data_without_na = data.dropna(subset=['improvement_rate'])
X = data_without_na[features]
Y = data_without_na[target]

# Split the dataset into training (80%) and testing (20%) sets
xtrain, xtest, ytrain, ytest = train_test_split(X, Y, test_size=0.2, random_state=0)

# Create and train the Decision Tree model with additional parameters
model = DecisionTreeClassifier(criterion='entropy', max_depth=10, min_samples_split=5, min_samples_leaf=2)
model.fit(xtrain, ytrain)

# Function to classify a user's performance based on accuracy, improvement rate, and difficulty score
def classify_performance(accuracy, improvement_rate, difficulty_score):
    if improvement_rate == "NA":
        improvement_rate = np.nan
    input_data = np.array([[accuracy, improvement_rate, difficulty_score]])
    prediction = model.predict(input_data)
    return prediction[0]

# Evaluate model accuracy, precision, recall, and F1 score on test data
y_pred = model.predict(xtest)
model_accuracy = accuracy_score(ytest, y_pred) * 100
precision = precision_score(ytest, y_pred, average='weighted', zero_division=0)
recall = recall_score(ytest, y_pred, average='weighted', zero_division=0)
f1 = f1_score(ytest, y_pred, average='weighted')

print(f"Model Accuracy: {round(model_accuracy, 2)}%")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1:.4f}")

# Save the trained model
model_filename = os.path.abspath(os.path.join('AptitudeTraining', 'static', 'decision_tree_model.pkl'))
joblib.dump(model, model_filename)
print("Model saved successfully at:", model_filename)

# Example usage
example_input = [85, 20, 75]  # Accuracy: 85%, Improvement Rate: 20%, Difficulty Score: 75%
predicted_class = classify_performance(*example_input)
print("Predicted Performance Level:", predicted_class)
