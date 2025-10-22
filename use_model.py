#!/usr/bin/env python3
"""
Flight Delay Prediction - Model Usage Script
============================================

This script demonstrates how to use the trained flight delay prediction model.
"""

import joblib
import pandas as pd
import json

def load_model():
    """Load the trained model and associated metadata."""
    try:
        model = joblib.load('models/flight_delay_model.pkl')
        label_encoders = joblib.load('models/label_encoders.pkl')
        
        with open('models/feature_columns.json', 'r') as f:
            feature_columns = json.load(f)
            
        airports_df = pd.read_csv('models/airports.csv')
        
        print("Model loaded successfully!")
        print(f"Available airports: {len(airports_df)}")
        
        return model, label_encoders, feature_columns, airports_df
    
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please run create_model.py first to train the model.")
        return None, None, None, None

def predict_flight_delay(model, label_encoders, feature_columns,
                        month, day_of_month, day_of_week,
                        origin_airport_id, dest_airport_id,
                        dep_hour, arr_hour, carrier):
    """Predict delay probability for a specific flight."""
    
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
        print(f"Warning: Unknown carrier '{carrier}', using default encoding")
        input_data['Carrier'] = 0
    
    # Make prediction
    probability = model.predict_proba(input_data)[0, 1]
    prediction = model.predict(input_data)[0]
    
    return probability, prediction

def get_airport_info(airports_df, airport_id):
    """Get airport information by ID."""
    airport = airports_df[airports_df['AirportID'] == airport_id]
    if not airport.empty:
        return airport.iloc[0]
    return None

def main():
    """Main function for interactive prediction."""
    print("Flight Delay Prediction Tool")
    print("=" * 30)
    
    # Load model
    model, label_encoders, feature_columns, airports_df = load_model()
    
    if model is None:
        return
    
    # Show some example airports
    print("\nSample airports:")
    print(airports_df.head(10)[['AirportID', 'AirportName', 'City', 'State']])
    
    # Example predictions
    examples = [
        {
            'desc': 'Chicago O\'Hare to Los Angeles (Friday afternoon)',
            'month': 12, 'day_of_month': 15, 'day_of_week': 5,
            'origin': 13930, 'dest': 12892, 'dep_hour': 14, 'arr_hour': 17, 'carrier': 'AA'
        },
        {
            'desc': 'JFK to San Francisco (Monday morning)',
            'month': 6, 'day_of_month': 10, 'day_of_week': 1,
            'origin': 12478, 'dest': 14771, 'dep_hour': 8, 'arr_hour': 11, 'carrier': 'UA'
        },
        {
            'desc': 'Atlanta to Miami (Sunday evening)',
            'month': 3, 'day_of_month': 20, 'day_of_week': 7,
            'origin': 10397, 'dest': 13204, 'dep_hour': 19, 'arr_hour': 21, 'carrier': 'DL'
        }
    ]
    
    print("\nExample Predictions:")
    print("-" * 50)
    
    for example in examples:
        prob, pred = predict_flight_delay(
            model, label_encoders, feature_columns,
            example['month'], example['day_of_month'], example['day_of_week'],
            example['origin'], example['dest'], example['dep_hour'], 
            example['arr_hour'], example['carrier']
        )
        
        origin_info = get_airport_info(airports_df, example['origin'])
        dest_info = get_airport_info(airports_df, example['dest'])
        
        print(f"\nFlight: {example['desc']}")
        if origin_info is not None and dest_info is not None:
            print(f"Route: {origin_info['AirportName']} → {dest_info['AirportName']}")
        print(f"Carrier: {example['carrier']}")
        print(f"Delay Probability: {prob:.4f} ({prob*100:.2f}%)")
        print(f"Prediction: {'LIKELY DELAYED' if pred == 1 else 'ON TIME'}")
    
    # Interactive prediction
    print("\n" + "=" * 50)
    print("Want to make a custom prediction? (y/n): ", end="")
    
    try:
        response = input().lower().strip()
        if response == 'y':
            print("\nEnter flight details:")
            month = int(input("Month (1-12): "))
            day_of_month = int(input("Day of month (1-31): "))
            day_of_week = int(input("Day of week (1=Mon, 7=Sun): "))
            origin_id = int(input("Origin airport ID: "))
            dest_id = int(input("Destination airport ID: "))
            dep_hour = int(input("Departure hour (0-23): "))
            arr_hour = int(input("Arrival hour (0-23): "))
            carrier = input("Carrier code (e.g., AA, UA, DL): ").strip().upper()
            
            prob, pred = predict_flight_delay(
                model, label_encoders, feature_columns,
                month, day_of_month, day_of_week,
                origin_id, dest_id, dep_hour, arr_hour, carrier
            )
            
            print(f"\nPrediction Results:")
            print(f"Delay Probability: {prob:.4f} ({prob*100:.2f}%)")
            print(f"Prediction: {'LIKELY DELAYED (>15 min)' if pred == 1 else 'LIKELY ON TIME'}")
            
    except (ValueError, KeyboardInterrupt):
        print("\nSkipping interactive prediction.")
    
    print("\nModel usage complete!")

if __name__ == "__main__":
    main()