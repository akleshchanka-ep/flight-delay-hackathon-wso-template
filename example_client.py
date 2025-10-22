#!/usr/bin/env python3
"""
Example Client for Flight Delay Prediction API
==============================================

This script demonstrates how to interact with the Flight Delay API.
"""

import requests
import sys

API_BASE_URL = "http://localhost:8000"

def check_server():
    """Check if the API server is running."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        data = response.json()
        if data['status'] == 'healthy' and data['model_loaded']:
            print("✓ API server is running and model is loaded\n")
            return True
        else:
            print("✗ API server is not ready")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to API server")
        print("\nPlease start the server first:")
        print("  cd backend")
        print("  ./run_server.sh\n")
        return False

def get_airports(limit=10):
    """Fetch and display available airports."""
    print("Available Airports (sample):")
    print("-" * 70)
    
    response = requests.get(f"{API_BASE_URL}/airports", params={"limit": limit})
    data = response.json()
    
    print(f"Total airports in database: {data['total']}\n")
    
    for airport in data['airports']:
        print(f"  ID: {airport['airport_id']:5d} | {airport['airport_name']:40s} | {airport['city']}, {airport['state']}")
    
    print()
    return data['airports']

def predict_delay(day_of_week, origin_id, dest_id):
    """Make a flight delay prediction."""
    payload = {
        "day_of_week": day_of_week,
        "origin_airport_id": origin_id,
        "dest_airport_id": dest_id
    }
    
    response = requests.post(f"{API_BASE_URL}/predict", json=payload)
    
    if response.status_code != 200:
        print(f"✗ Error: {response.json()}")
        return None
    
    return response.json()

def day_name(day_num):
    """Convert day number to name."""
    days = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 
            5: "Friday", 6: "Saturday", 7: "Sunday"}
    return days.get(day_num, "Unknown")

def main():
    """Main function."""
    print("=" * 70)
    print("Flight Delay Prediction - Example Client")
    print("=" * 70)
    print()
    
    # Check server status
    if not check_server():
        sys.exit(1)
    
    # Get sample airports
    airports = get_airports(limit=15)
    
    # Example predictions
    examples = [
        {
            "desc": "Chicago O'Hare to Los Angeles (Friday)",
            "day": 5,
            "origin": 13930,
            "dest": 12892
        },
        {
            "desc": "JFK to San Francisco (Monday)",
            "day": 1,
            "origin": 12478,
            "dest": 14771
        },
        {
            "desc": "Atlanta to Miami (Sunday)",
            "day": 7,
            "origin": 10397,
            "dest": 13204
        }
    ]
    
    print("\nExample Predictions:")
    print("=" * 70)
    
    for example in examples:
        print(f"\n{example['desc']}")
        print(f"Day: {day_name(example['day'])}")
        print(f"Origin Airport ID: {example['origin']}")
        print(f"Destination Airport ID: {example['dest']}")
        
        result = predict_delay(example['day'], example['origin'], example['dest'])
        
        if result:
            print(f"\nResults:")
            print(f"  Delay Probability: {result['delay_probability']:.4f} ({result['delay_probability']*100:.2f}%)")
            print(f"  Confidence: {result['confidence']:.4f} ({result['confidence']*100:.2f}%)")
            print(f"  Prediction: {result['prediction']}")
        
        print("-" * 70)
    
    # Interactive mode
    print("\n\nWant to make a custom prediction? (y/n): ", end="")
    try:
        response = input().strip().lower()
        if response == 'y':
            print("\nEnter flight details:")
            day = int(input("Day of week (1=Mon, 2=Tue, ..., 7=Sun): "))
            origin = int(input("Origin airport ID: "))
            dest = int(input("Destination airport ID: "))
            
            print(f"\nPredicting delay for {day_name(day)} flight...")
            result = predict_delay(day, origin, dest)
            
            if result:
                print(f"\nResults:")
                print(f"  Delay Probability: {result['delay_probability']:.4f} ({result['delay_probability']*100:.2f}%)")
                print(f"  Confidence: {result['confidence']:.4f} ({result['confidence']*100:.2f}%)")
                print(f"  Prediction: {result['prediction']}")
                
                if result['delay_probability'] > 0.5:
                    print("\n  ⚠️  This flight has a high probability of being delayed!")
                else:
                    print("\n  ✓ This flight is likely to be on time.")
    except (ValueError, KeyboardInterrupt):
        print("\nSkipping custom prediction.")
    
    print("\n\nFor more information, visit: http://localhost:8000/docs")
    print()

if __name__ == "__main__":
    main()
