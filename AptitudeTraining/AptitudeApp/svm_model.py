
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load dataset dynamically from previous file
file_path = os.path.abspath(os.path.join('AptitudeTraining', 'static', 'career_prediction_dataset.csv'))
df = pd.read_csv(file_path)
logging.info(f"Dataset loaded from {file_path}")

# Reduce dataset size to 1000 samples using stratified sampling
if len(df) > 10000:
    df = df.groupby('prediction', group_keys=False).apply(lambda x: x.sample(min(len(x), 1000 // len(df['prediction'].unique()))))
    logging.info("Dataset reduced to 1000 samples using stratified sampling.")

# Handle missing values
if df.isnull().sum().sum() > 0:
    df.fillna(df.mean(numeric_only=True), inplace=True)
    logging.info("Missing values filled with column means.")

# Remove outliers using z-score
z_scores = np.abs((df.iloc[:, :-1] - df.iloc[:, :-1].mean()) / df.iloc[:, :-1].std())
df = df[(z_scores < 3).all(axis=1)]
logging.info("Outliers removed using Z-score method.")

# Define feature columns
feature_columns = ["logical", "verbal", "quantitative"]
X = df[feature_columns]
y = df["prediction"]

# Apply SMOTE to balance classes
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)
logging.info("Class imbalance handled using SMOTE.")

# Apply feature scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_resampled)
scaler_path = os.path.abspath(os.path.join('AptitudeTraining', 'static', 'scaler.pkl'))
joblib.dump(scaler, scaler_path)
logging.info(f"Scaler saved successfully at {scaler_path}")
logging.info("Features scaled using StandardScaler.")

# Shuffle and split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_resampled, test_size=0.2, random_state=42, shuffle=True)
logging.info("Data split into training and test sets.")

# Perform GridSearchCV for hyperparameter tuning with parallel processing
param_grid = {'C': [0.01, 0.1, 1, 10, 100], 'kernel': ['linear', 'rbf'], 'gamma': ['scale', 'auto', 0.001, 0.01, 0.1]}
grid_search = GridSearchCV(SVC(class_weight='balanced', random_state=42), param_grid, cv=3, n_jobs=-1)
grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_
logging.info(f"Best parameters found: {grid_search.best_params_}")

# Train the model using best parameters
best_model.fit(X_train, y_train)
y_pred = best_model.predict(X_test)

# Final evaluation
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted', zero_division=1)
recall = recall_score(y_test, y_pred, average='weighted', zero_division=1)
f1 = f1_score(y_test, y_pred, average='weighted')

logging.info(f"Final Accuracy: {accuracy:.4f}")
logging.info(f"Precision: {precision:.4f}")
logging.info(f"Recall: {recall:.4f}")
logging.info(f"F1 Score: {f1:.4f}")
logging.info("Classification Report:\n" + classification_report(y_test, y_pred, zero_division=1))

# Save trained model using OS pathing
model_path = os.path.abspath(os.path.join('AptitudeTraining', 'static', 'career_prediction_model.pkl'))
joblib.dump(best_model, model_path)
logging.info(f"Model saved successfully at {model_path}")
