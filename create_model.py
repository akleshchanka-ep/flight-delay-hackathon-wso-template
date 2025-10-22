#!/usr/bin/env python3
"""
Flight Delay Prediction Model
============================

This script creates a machine learning model to predict flight delays based on the flights.csv dataset.
The model predicts the probability that a flight will be delayed by more than 15 minutes.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import joblib
import json
import os

def load_and_explore_data(file_path):
    """Load the CSV data and perform initial exploration."""
    print("Loading data...")
    df = pd.read_csv(file_path)
    
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("\nFirst few rows:")
    print(df.head())
    
    print(f"\nMissing values per column:")
    print(df.isnull().sum())
    
    print(f"\nTarget variable distribution (ArrDel15):")
    print(df['ArrDel15'].value_counts())
    
    return df

def clean_data(df):
    """Clean the data by handling null values and preparing features."""
    print("\nCleaning data...")
    
    # Handle missing values - replace with 0 as specified in requirements
    df_clean = df.fillna(0)
    
    # Remove cancelled flights as they don't have delay information
    df_clean = df_clean[df_clean['Cancelled'] == 0].copy()
    
    print(f"Data shape after removing cancelled flights: {df_clean.shape}")
    
    # Create additional time-based features
    df_clean['CRSDepTime_Hour'] = (df_clean['CRSDepTime'] // 100).astype(int)
    df_clean['CRSArrTime_Hour'] = (df_clean['CRSArrTime'] // 100).astype(int)
    
    return df_clean

def prepare_features(df):
    """Prepare features for the model."""
    print("\nPreparing features...")
    
    # Select relevant features for prediction
    feature_columns = [
        'Month', 'DayofMonth', 'DayOfWeek',
        'OriginAirportID', 'DestAirportID',
        'CRSDepTime_Hour', 'CRSArrTime_Hour',
        'Carrier'
    ]
    
    X = df[feature_columns].copy()
    y = df['ArrDel15']
    
    # Encode categorical variables
    label_encoders = {}
    categorical_cols = ['Carrier']
    
    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        label_encoders[col] = le
    
    print(f"Feature matrix shape: {X.shape}")
    print(f"Features used: {feature_columns}")
    
    return X, y, label_encoders, feature_columns

def train_model(X, y):
    """Train the Random Forest model."""
    print("\nTraining model...")
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train Random Forest model
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=10,
        min_samples_split=100,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    print("\nModel Performance:")
    print("==================")
    print(f"ROC AUC Score: {roc_auc_score(y_test, y_pred_proba):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nTop 10 Most Important Features:")
    print(feature_importance.head(10))
    
    return model, X_test, y_test

def save_model_and_metadata(model, label_encoders, feature_columns, df):
    """Save the model and create airport metadata file."""
    print("\nSaving model and metadata...")
    
    # Create models directory
    os.makedirs('models', exist_ok=True)
    
    # Save the trained model
    joblib.dump(model, 'models/flight_delay_model.pkl')
    
    # Save label encoders
    joblib.dump(label_encoders, 'models/label_encoders.pkl')
    
    # Save feature columns
    with open('models/feature_columns.json', 'w') as f:
        json.dump(feature_columns, f)
    
    # Create airport names and IDs file (requirement #4)
    airports_origin = df[['OriginAirportID', 'OriginAirportName', 'OriginCity', 'OriginState']].drop_duplicates()
    airports_dest = df[['DestAirportID', 'DestAirportName', 'DestCity', 'DestState']].drop_duplicates()
    
    # Rename columns for consistency
    airports_origin.columns = ['AirportID', 'AirportName', 'City', 'State']
    airports_dest.columns = ['AirportID', 'AirportName', 'City', 'State']
    
    # Combine and remove duplicates
    airports = pd.concat([airports_origin, airports_dest]).drop_duplicates('AirportID').sort_values('AirportID')
    
    # Save airports file
    airports.to_csv('models/airports.csv', index=False)
    
    print(f"Model saved to: models/flight_delay_model.pkl")
    print(f"Label encoders saved to: models/label_encoders.pkl")
    print(f"Feature columns saved to: models/feature_columns.json")
    print(f"Airport data saved to: models/airports.csv ({len(airports)} airports)")

def predict_delay_probability(model, label_encoders, feature_columns, 
                             month, day_of_month, day_of_week, 
                             origin_airport_id, dest_airport_id, 
                             dep_hour, arr_hour, carrier):
    """
    Predict delay probability for a given flight.
    
    Args:
        month: Month (1-12)
        day_of_month: Day of month (1-31)
        day_of_week: Day of week (1=Monday, 7=Sunday)
        origin_airport_id: Origin airport ID
        dest_airport_id: Destination airport ID
        dep_hour: Departure hour (0-23)
        arr_hour: Arrival hour (0-23)
        carrier: Airline carrier code
    
    Returns:
        Probability of delay > 15 minutes
    """
    # Create input data
    input_data = pd.DataFrame({
        'Month': [month],
        'DayofMonth': [day_of_month],
        'DayOfWeek': [day_of_week],
        'OriginAirportID': [origin_airport_id],
        'DestAirportID': [dest_airport_id],
        'CRSDepTime_Hour': [dep_hour],
        'CRSArrTime_Hour': [arr_hour],
        'Carrier': [carrier]
    })
    
    # Encode categorical variables
    if carrier in label_encoders['Carrier'].classes_:
        input_data['Carrier'] = label_encoders['Carrier'].transform([carrier])
    else:
        # Handle unknown carrier
        input_data['Carrier'] = 0
    
    # Make prediction
    probability = model.predict_proba(input_data)[0, 1]
    return probability

def main():
    """Main execution function."""
    print("Flight Delay Prediction Model Creation")
    print("=" * 40)
    
    # Load and explore data
    df = load_and_explore_data('data/flights.csv')
    
    # Clean data
    df_clean = clean_data(df)
    
    # Prepare features
    X, y, label_encoders, feature_columns = prepare_features(df_clean)
    
    # Train model
    model, X_test, y_test = train_model(X, y)
    
    # Save model and metadata
    save_model_and_metadata(model, label_encoders, feature_columns, df_clean)
    
    print("\n" + "=" * 50)
    print("Model creation completed successfully!")
    print("\nTo use the model for predictions, you can:")
    print("1. Load the model: model = joblib.load('models/flight_delay_model.pkl')")
    print("2. Load encoders: encoders = joblib.load('models/label_encoders.pkl')")
    print("3. Use the predict_delay_probability function")
    
    # Example prediction
    print("\nExample prediction:")
    prob = predict_delay_probability(
        model, label_encoders, feature_columns,
        month=12, day_of_month=15, day_of_week=5,  # Friday, Dec 15
        origin_airport_id=13930,  # Chicago O'Hare
        dest_airport_id=12892,    # Los Angeles
        dep_hour=14, arr_hour=17, carrier='AA'
    )
    print(f"Delay probability for example flight: {prob:.4f} ({prob*100:.2f}%)")

if __name__ == "__main__":
    main()