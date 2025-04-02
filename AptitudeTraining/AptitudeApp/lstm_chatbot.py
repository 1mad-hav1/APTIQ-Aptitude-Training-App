import numpy as np
import pandas as pd
import re
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding, SpatialDropout1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Step 1: Load and preprocess data
data = pd.read_csv('chatbot_dataset.csv')
questions = data['question'].astype(str).tolist()
answers = data['answer'].astype(str).tolist()
descriptions = data['description'].astype(str).tolist()
types = data['type'].astype(str).tolist()

# Step 2: Tokenize the data
tokenizer = Tokenizer()
tokenizer.fit_on_texts(questions + answers + descriptions)
vocab_size = len(tokenizer.word_index) + 1

# Step 3: Convert text to sequences
X = tokenizer.texts_to_sequences(questions)
y = tokenizer.texts_to_sequences(answers)
X = pad_sequences(X, padding='post')
y = pad_sequences(y, padding='post')

# Step 4: Define LSTM Model
model = Sequential([
    Embedding(vocab_size, 256, input_length=X.shape[1]),
    SpatialDropout1D(0.2),
    LSTM(256, return_sequences=True),
    LSTM(256),
    Dense(256, activation='relu'),
    Dense(vocab_size, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Step 5: Train Model with progress callback
class ProgressCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        print(f"Epoch {epoch + 1}/{self.params['epochs']} - Loss: {logs['loss']:.4f}, Accuracy: {logs['accuracy']:.4f}")

model.fit(X, np.array(y), epochs=50, batch_size=64, validation_split=0.2, callbacks=[ProgressCallback()])
model.save('lstm_chatbot_model.h5')

# Step 6: Evaluate Model
predictions = model.predict(X)
predicted_labels = np.argmax(predictions, axis=-1)
y_flat = y.flatten()
y_flat = y_flat[y_flat != 0]  # Remove padding values
predicted_labels = predicted_labels.flatten()[:len(y_flat)]

accuracy = accuracy_score(y_flat, predicted_labels)
precision = precision_score(y_flat, predicted_labels, average='weighted', zero_division=0)
recall = recall_score(y_flat, predicted_labels, average='weighted', zero_division=0)
f1 = f1_score(y_flat, predicted_labels, average='weighted')

print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1:.4f}")

# Step 7: Load model and Chat
from tensorflow.keras.models import load_model
model = load_model('lstm_chatbot_model.h5')

def preprocess_text(text):
    text = re.sub(r'[^\w\s]', '', text.lower())
    return text

def predict_response(input_text):
    input_text = preprocess_text(input_text)
    sequence = tokenizer.texts_to_sequences([input_text])
    padded_sequence = pad_sequences(sequence, maxlen=X.shape[1], padding='post')
    prediction = model.predict(padded_sequence)
    response_index = np.argmax(prediction)
    
    if response_index < len(answers):
        return f"Answer: {answers[response_index]}\nDescription: {descriptions[response_index]}\nType: {types[response_index]}"

    return 'I am not sure how to respond.'

# Start Chatting
while True:
    user_input = input('You: ')
    if user_input.lower() in ['exit', 'quit']:
        break
    response = predict_response(user_input)
    print('Bot:', response)
