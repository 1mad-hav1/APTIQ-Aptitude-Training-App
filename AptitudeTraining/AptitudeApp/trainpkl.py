import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load dataset
df = pd.read_csv("C:\\Users\\ronsi\\OneDrive\\Desktop\\Main Project\\AptitudeTraining\\static\\classified_careers_updated.csv")  # Ensure this CSV has required columns

# Define feature columns (update based on dataset structure)
feature_columns = ["Numerical Aptitude", "Spatial Aptitude",
                   "Perceptual Aptitude", "Abstract Reasoning", "Verbal Reasoning"]

X = df[feature_columns]  # Features
y = df["Career"]   # Target column (Course Category)

# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Save trained model
joblib.dump(rf_model, "course_prediction_model.pkl")
print("Model saved successfully!")