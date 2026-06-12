# train_model.py
# This script trains a simple machine learning model that predicts a
# career role based on the skills a student enters.
# We use TF-IDF to convert the skill text into numbers, and then
# Logistic Regression to classify which role those skills best match.

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import pickle

# Step 1: Load the dataset
print("Loading dataset...")
data = pd.read_csv("skills_dataset.csv")

# Just to be safe, drop any empty rows
data = data.dropna()

print(f"Dataset loaded. Total rows: {len(data)}")
print("Roles in dataset:", data["role"].unique())

# Step 2: Split into input (X) and output (y)
X = data["skills"]
y = data["role"]

# Step 3: Train-test split so we can check accuracy on unseen data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Step 4: Build a pipeline
# TfidfVectorizer -> turns each skills string into a vector of numbers
# based on how important each word (skill) is in the dataset.
# LogisticRegression -> a simple, fast, and easy-to-explain classifier
# that works well for this kind of text classification task.
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", LogisticRegression(max_iter=1000))
])

# Step 5: Train the model
print("Training model...")
pipeline.fit(X_train, y_train)

# Step 6: Check accuracy on the test set
y_pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model trained successfully!")
print(f"Test Accuracy: {accuracy * 100:.2f}%")

# Step 7: Save the trained pipeline (vectorizer + model together) using pickle
with open("model.pkl", "wb") as f:
    pickle.dump(pipeline, f)

print("Model saved as model.pkl")
