import joblib
import numpy as np
import os
from sklearn.preprocessing import StandardScaler

# Load the model
model_path = os.path.abspath(os.path.join('AptitudeTraining' , 'static', 'career_prediction_model1.pkl'))
model = joblib.load(model_path)

# Load the scaler
scaler = StandardScaler()
scaler_path = os.path.abspath(os.path.join('AptitudeTraining' , 'static', 'scaler1.pkl'))
scaler = joblib.load(scaler_path)

# Provide a sample input (logical, verbal, quantitative)
sample_input = np.array([[12,90,99]])  # Example values

# Scale the input
scaled_input = scaler.transform(sample_input)

# Predict
prediction = model.predict(scaled_input)
print(f"Predicted Career: {prediction[0]}")
