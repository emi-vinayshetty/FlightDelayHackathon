# Test the Flight Delay API endpoints
# This script demonstrates all the API endpoints and their functionality

import requests
import json

# API base URL
BASE_URL = "http://localhost:5000"

def test_api():
    print("🧪 Testing Flight Delay Prediction API")
    print("=" * 50)
    
    # Test 1: Root endpoint
    print("📋 Test 1: API Information (GET /)")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure the server is running on localhost:5000")
        return
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "-" * 50)
    
    # Test 2: Health check
    print("🏥 Test 2: Health Check (GET /health)")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "-" * 50)
    
    # Test 3: Get all airports
    print("🛫 Test 3: Get All Airports (GET /airports)")
    try:
        response = requests.get(f"{BASE_URL}/airports")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Total airports: {data['total_count']}")
        print("First 5 airports:")
        for airport in data['airports'][:5]:
            print(f"  - {airport['name']} ({airport['city']}, {airport['state']}) - ID: {airport['id']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "-" * 50)
    
    # Test 4: Get specific airport
    print("🛫 Test 4: Get Specific Airport (GET /airports/13930)")
    try:
        response = requests.get(f"{BASE_URL}/airports/13930")  # Chicago O'Hare
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "-" * 50)
    
    # Test 5: Prediction - Monday at Chicago O'Hare
    print("🤖 Test 5: Predict Delay - Monday at Chicago O'Hare (POST /predict)")
    try:
        payload = {
            "day_of_week": 1,  # Monday
            "airport_id": 13930  # Chicago O'Hare
        }
        response = requests.post(f"{BASE_URL}/predict", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Request: {json.dumps(payload, indent=2)}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "-" * 50)
    
    # Test 6: Prediction - Friday at JFK
    print("🤖 Test 6: Predict Delay - Friday at JFK (POST /predict)")
    try:
        payload = {
            "day_of_week": 5,  # Friday
            "airport_id": 12478  # JFK
        }
        response = requests.post(f"{BASE_URL}/predict", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Request: {json.dumps(payload, indent=2)}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "-" * 50)
    
    # Test 7: Prediction - Sunday at LAX
    print("🤖 Test 7: Predict Delay - Sunday at LAX (POST /predict)")
    try:
        payload = {
            "day_of_week": 7,  # Sunday
            "airport_id": 12892  # LAX
        }
        response = requests.post(f"{BASE_URL}/predict", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Request: {json.dumps(payload, indent=2)}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "-" * 50)
    
    # Test 8: Error handling - Invalid day
    print("❌ Test 8: Error Handling - Invalid Day (POST /predict)")
    try:
        payload = {
            "day_of_week": 8,  # Invalid day
            "airport_id": 13930
        }
        response = requests.post(f"{BASE_URL}/predict", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Request: {json.dumps(payload, indent=2)}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "-" * 50)
    
    # Test 9: Error handling - Missing fields
    print("❌ Test 9: Error Handling - Missing Fields (POST /predict)")
    try:
        payload = {
            "day_of_week": 1  # Missing airport_id
        }
        response = requests.post(f"{BASE_URL}/predict", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Request: {json.dumps(payload, indent=2)}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ API Testing Complete!")
    print("\n📋 Summary of API endpoints:")
    print(f"  🌐 Server: {BASE_URL}")
    print("  📍 GET  /           - API information")
    print("  🏥 GET  /health     - Health check")
    print("  🤖 POST /predict    - Predict flight delay")
    print("  🛫 GET  /airports   - Get all airports")
    print("  🛫 GET  /airports/<id> - Get specific airport")

if __name__ == "__main__":
    test_api()