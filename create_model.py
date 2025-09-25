# Flight Delay Prediction Model
# This script creates a machine learning model to predict flight delays

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os

print("🚀 Starting Flight Delay Model Creation")
print("=" * 50)

# Step 1: Load the flight data
print("📊 Step 1: Loading flight data...")
df = pd.read_csv('data/flights.csv')
print(f"✅ Dataset loaded: {df.shape[0]:,} rows, {df.shape[1]} columns")
print(f"   First few rows preview:")
print(df.head())

# Step 2: Explore the dataset structure
print("\n📋 Step 2: Exploring dataset structure...")
print("Dataset information:")
print(df.info())

print("\nColumn descriptions:")
print("- DayOfWeek: Day of the week (1=Monday, 7=Sunday)")
print("- OriginAirportID: Unique identifier for origin airport")
print("- DepDel15: 1 if departure delayed >15 minutes, 0 otherwise")
print("- ArrDel15: 1 if arrival delayed >15 minutes, 0 otherwise")

# Step 3: Check for missing values
print("\n🔍 Step 3: Checking for missing values...")
missing_values = df.isnull().sum()
print("Missing values per column:")
print(missing_values[missing_values > 0])

print("\nUnique values in key columns:")
print(f"Days of week: {sorted(df['DayOfWeek'].unique())}")
print(f"Number of unique airports: {df['OriginAirportID'].nunique()}")
print(f"Delay distribution (DepDel15): {df['DepDel15'].value_counts().to_dict()}")

# Step 4: Data cleaning
print("\n🧹 Step 4: Cleaning data...")
print("Replacing null values with 0...")

# Fill missing values with 0
df_clean = df.fillna(0)

print(f"After cleaning - Missing values: {df_clean.isnull().sum().sum()}")

# Ensure DepDel15 is binary (0 or 1)
df_clean['DepDel15'] = df_clean['DepDel15'].astype(int)
print(f"Delay distribution after cleaning: {df_clean['DepDel15'].value_counts().to_dict()}")

# Step 5: Prepare data for machine learning
print("\n🎯 Step 5: Preparing data for machine learning...")
features = ['DayOfWeek', 'OriginAirportID']
X = df_clean[features]
y = df_clean['DepDel15']

print(f"Features shape: {X.shape}")
print(f"Target shape: {y.shape}")
print(f"Feature statistics:")
print(X.describe())

# Step 6: Split data
print("\n📊 Step 6: Splitting data into training and testing sets...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training set size: {X_train.shape[0]:,}")
print(f"Testing set size: {X_test.shape[0]:,}")
print(f"Class distribution in training set:")
print(y_train.value_counts(normalize=True))

# Step 7: Create and train the model
print("\n🤖 Step 7: Training Random Forest model...")
model = RandomForestClassifier(
    n_estimators=100,  # Number of trees
    random_state=42,   # For reproducibility
    max_depth=10,      # Prevent overfitting
    min_samples_split=5
)

# Train the model
model.fit(X_train, y_train)
print("✅ Model training completed!")

# Step 8: Evaluate the model
print("\n📈 Step 8: Evaluating model performance...")
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]  # Probability of delay

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Feature importance
feature_importance = pd.DataFrame({
    'feature': features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nFeature Importance:")
print(feature_importance)

# Step 9: Test with examples
print("\n🧪 Step 9: Testing model with real examples...")

# Example: Monday (1) at Chicago O'Hare (13930)
example_1 = [[1, 13930]]
prob_1 = model.predict_proba(example_1)[0][1]
print(f"📍 Monday at Chicago O'Hare: {prob_1:.4f} ({prob_1*100:.2f}% chance of delay)")

# Example: Friday (5) at JFK (12478)
example_2 = [[5, 12478]]
prob_2 = model.predict_proba(example_2)[0][1]
print(f"📍 Friday at JFK: {prob_2:.4f} ({prob_2*100:.2f}% chance of delay)")

# Example: Sunday (7) at LAX (12892)
example_3 = [[7, 12892]]
prob_3 = model.predict_proba(example_3)[0][1]
print(f"📍 Sunday at LAX: {prob_3:.4f} ({prob_3*100:.2f}% chance of delay)")

# Step 10: Save the model
print("\n💾 Step 10: Saving the trained model...")
os.makedirs('model', exist_ok=True)

# Save the model using pickle
model_filename = 'model/flight_delay_model.pkl'
with open(model_filename, 'wb') as file:
    pickle.dump(model, file)

print(f"✅ Model saved to: {model_filename}")

# Also save feature names for reference
feature_info = {
    'features': features,
    'model_type': 'RandomForestClassifier',
    'accuracy': accuracy,
    'description': 'Predicts probability of flight delay >15 minutes based on day of week and airport'
}

with open('model/model_info.pkl', 'wb') as file:
    pickle.dump(feature_info, file)

print("✅ Model information saved to: model/model_info.pkl")

# Step 11: Create airports CSV file
print("\n🛫 Step 11: Creating airports CSV file...")

# Extract unique airports from both origin and destination
origin_airports = df_clean[['OriginAirportID', 'OriginAirportName', 'OriginCity', 'OriginState']].copy()
origin_airports.columns = ['AirportID', 'AirportName', 'City', 'State']

dest_airports = df_clean[['DestAirportID', 'DestAirportName', 'DestCity', 'DestState']].copy()
dest_airports.columns = ['AirportID', 'AirportName', 'City', 'State']

# Combine and remove duplicates
all_airports = pd.concat([origin_airports, dest_airports]).drop_duplicates(subset=['AirportID'])
all_airports = all_airports.sort_values('AirportID').reset_index(drop=True)

print(f"✅ Total unique airports: {len(all_airports)}")
print("\nFirst 5 airports:")
print(all_airports.head())

# Save to CSV
airports_filename = 'data/airports.csv'
all_airports.to_csv(airports_filename, index=False)
print(f"✅ Airports data saved to: {airports_filename}")

# Final Summary
print("\n" + "=" * 50)
print("🎉 MODEL CREATION COMPLETED SUCCESSFULLY!")
print("=" * 50)
print(f"✅ Loaded and cleaned {df.shape[0]:,} flight records")
print(f"✅ Created Random Forest model with {accuracy:.4f} accuracy")
print(f"✅ Saved model to: {model_filename}")
print(f"✅ Created airports file with {len(all_airports)} unique airports")
print(f"✅ Saved airports to: {airports_filename}")
print("\n🎯 The model can now predict flight delay probabilities!")
print("\n📁 Files created:")
print(f"   - {model_filename}")
print(f"   - model/model_info.pkl")
print(f"   - {airports_filename}")