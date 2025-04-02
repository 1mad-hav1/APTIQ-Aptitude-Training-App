import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import xgboost as xgb
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load new dataset
file_path = os.path.abspath(os.path.join('AptitudeTraining', 'static', 'career_prediction_dataset.csv'))
df = pd.read_csv(file_path)
logging.info(f"New dataset loaded from {file_path}")

# Handle missing values
df.fillna(df.mean(), inplace=True)
logging.info("Missing values filled with column means.")

# Remove outliers using z-score
z_scores = np.abs((df.iloc[:, :-1] - df.iloc[:, :-1].mean()) / df.iloc[:, :-1].std())
df = df[(z_scores < 3).all(axis=1)]
logging.info("Outliers removed using Z-score method.")

# Define feature columns with new attributes
feature_columns = ["logical", "verbal", "quantitative", "logical_improvement", "verbal_improvement", "quantitative_improvement"]
X = df[feature_columns]
y = df["prediction"]

# Apply SMOTE to balance classes
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)
logging.info("Class imbalance handled using SMOTE.")

# Apply feature scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_resampled)
scaler_path = os.path.abspath(os.path.join('AptitudeTraining', 'static', 'scaler_random_forest.pkl'))
joblib.dump(scaler, scaler_path)
logging.info(f"Scaler saved successfully at {scaler_path}")

# Shuffle and split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_resampled, test_size=0.2, random_state=42, shuffle=True)
logging.info("Data split into training and test sets.")

# Perform GridSearchCV for hyperparameter tuning with Random Forest
param_grid_rf = {
    'n_estimators': [100, 200],
    'max_depth': [10, 30, None],
    'min_samples_split': [2, 10],
    'min_samples_leaf': [1, 4]
}
grid_search_rf = GridSearchCV(RandomForestClassifier(random_state=42), param_grid_rf, cv=5, n_jobs=-1)
grid_search_rf.fit(X_train, y_train)
best_rf = grid_search_rf.best_estimator_
logging.info(f"Best Random Forest parameters: {grid_search_rf.best_params_}")

# Train Gradient Boosting Classifier
gb_model = GradientBoostingClassifier(random_state=42)
gb_model.fit(X_train, y_train)

# Train XGBoost Classifier
xgb_model = xgb.XGBClassifier(random_state=42)
xgb_model.fit(X_train, y_train)

# Evaluate models
for name, model in zip(['Random Forest', 'Gradient Boosting', 'XGBoost'], [best_rf, gb_model, xgb_model]):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    logging.info(f"{name} Accuracy: {accuracy:.4f}")
    logging.info(f"Classification Report for {name}:\n" + classification_report(y_test, y_pred, zero_division=1))

# Save best model
best_model = max([(best_rf, accuracy_score(y_test, best_rf.predict(X_test))),
                   (gb_model, accuracy_score(y_test, gb_model.predict(X_test))),
                   (xgb_model, accuracy_score(y_test, xgb_model.predict(X_test)))], key=lambda x: x[1])[0]
model_path = os.path.abspath(os.path.join('AptitudeTraining', 'static', 'career_prediction_model_random_forest.pkl'))
joblib.dump(best_model, model_path)
logging.info(f"Best Model saved successfully at {model_path}")
