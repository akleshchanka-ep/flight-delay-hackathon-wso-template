#!/usr/bin/env python3
"""
Test script for the Flight Delay Prediction API
================================================

This script tests the API endpoints to ensure they work correctly.
"""

import requests
import time
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint."""
    print("Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        response.raise_for_status()
        data = response.json()
        print(f"  ✓ Status: {data['status']}")
        print(f"  ✓ Model loaded: {data['model_loaded']}")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_airports():
    """Test the airports endpoint."""
    print("\nTesting /airports endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/airports?limit=5&offset=0", timeout=5)
        response.raise_for_status()
        data = response.json()
        print(f"  ✓ Total airports: {data['total']}")
        print(f"  ✓ Returned: {len(data['airports'])} airports")
        if data['airports']:
            print(f"  ✓ First airport: {data['airports'][0]['airport_name']}")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_prediction():
    """Test the prediction endpoint."""
    print("\nTesting /predict endpoint...")
    try:
        payload = {
            "day_of_week": 5,
            "origin_airport_id": 13930,
            "dest_airport_id": 12892
        }
        response = requests.post(f"{BASE_URL}/predict", json=payload, timeout=5)
        response.raise_for_status()
        data = response.json()
        print(f"  ✓ Delay probability: {data['delay_probability']:.4f} ({data['delay_probability']*100:.2f}%)")
        print(f"  ✓ Confidence: {data['confidence']:.4f}")
        print(f"  ✓ Prediction: {data['prediction']}")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_invalid_prediction():
    """Test prediction with invalid data."""
    print("\nTesting /predict with invalid data...")
    try:
        payload = {
            "day_of_week": 10,  # Invalid: should be 1-7
            "origin_airport_id": 13930,
            "dest_airport_id": 12892
        }
        response = requests.post(f"{BASE_URL}/predict", json=payload, timeout=5)
        if response.status_code == 400 or response.status_code == 422:
            print(f"  ✓ Correctly rejected invalid data (status {response.status_code})")
            return True
        else:
            print(f"  ✗ Should have rejected invalid data (got status {response.status_code})")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 50)
    print("Flight Delay Prediction API - Test Suite")
    print("=" * 50)
    
    # Check if server is running
    print("\nChecking if server is running...")
    try:
        response = requests.get(BASE_URL, timeout=5)
        print("  ✓ Server is responding")
    except requests.exceptions.ConnectionError:
        print("  ✗ Cannot connect to server")
        print("\nPlease start the server first:")
        print("  cd backend")
        print("  ./run_server.sh")
        print("\nor:")
        print("  cd backend")
        print("  uvicorn main:app --reload")
        sys.exit(1)
    except Exception as e:
        print(f"  ✗ Error: {e}")
        sys.exit(1)
    
    # Run tests
    results = []
    results.append(("Health Check", test_health()))
    results.append(("Airports List", test_airports()))
    results.append(("Prediction", test_prediction()))
    results.append(("Invalid Input Handling", test_invalid_prediction()))
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
