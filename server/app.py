# Flight Delay Prediction API Server
# This Flask API provides endpoints to predict flight delays and retrieve airport information
# 
# Endpoints:
# 1. /predict - Accepts day of week and airport ID, returns delay probability and confidence
# 2. /airports - Returns list of all airports sorted alphabetically
# 
# The API uses a pre-trained Random Forest model to predict flight delays based on
# day of week (1=Monday, 7=Sunday) and origin airport ID

from flask import Flask, request, jsonify
import pickle
import pandas as pd
import os
import numpy as np
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Global variables to store loaded model and data
model = None
model_info = None
airports_df = None

def load_model_and_data():
    """Load the trained model and airports data on startup"""
    global model, model_info, airports_df
    
    try:
        # Load the trained model
        model_path = os.path.join('..', 'model', 'flight_delay_model.pkl')
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        print("✅ Model loaded successfully")
        
        # Load model information
        model_info_path = os.path.join('..', 'model', 'model_info.pkl')
        with open(model_info_path, 'rb') as file:
            model_info = pickle.load(file)
        print("✅ Model info loaded successfully")
        
        # Load airports data
        airports_path = os.path.join('..', 'data', 'airports.csv')
        airports_df = pd.read_csv(airports_path)
        print("✅ Airports data loaded successfully")
        
        return True
    except Exception as e:
        print(f"❌ Error loading model and data: {str(e)}")
        return False

@app.route('/')
def home():
    """Root endpoint with API information"""
    return jsonify({
        "message": "Flight Delay Prediction API",
        "version": "1.0",
        "endpoints": {
            "/predict": "POST - Predict flight delay probability",
            "/airports": "GET - Get list of airports",
            "/health": "GET - Health check"
        },
        "model_info": {
            "type": model_info["model_type"] if model_info else "Not loaded",
            "accuracy": model_info["accuracy"] if model_info else "Unknown",
            "features": model_info["features"] if model_info else "Unknown"
        }
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "airports_loaded": airports_df is not None
    })

@app.route('/predict', methods=['POST'])
def predict_delay():
    """
    Predict flight delay probability
    
    Expected JSON payload:
    {
        "day_of_week": 1-7 (1=Monday, 7=Sunday),
        "airport_id": integer (airport ID from airports list)
    }
    
    Returns:
    {
        "delay_probability": float (0-1),
        "confidence_percent": float (0-100),
        "delay_chance_percent": float (0-100),
        "input": {...}
    }
    """
    try:
        # Check if model is loaded
        if model is None:
            return jsonify({"error": "Model not loaded"}), 500
        
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Validate required fields
        if 'day_of_week' not in data or 'airport_id' not in data:
            return jsonify({
                "error": "Missing required fields: day_of_week and airport_id"
            }), 400
        
        day_of_week = data['day_of_week']
        airport_id = data['airport_id']
        
        # Validate day_of_week range
        if not isinstance(day_of_week, int) or day_of_week < 1 or day_of_week > 7:
            return jsonify({
                "error": "day_of_week must be an integer between 1 (Monday) and 7 (Sunday)"
            }), 400
        
        # Validate airport_id
        if not isinstance(airport_id, int):
            return jsonify({
                "error": "airport_id must be an integer"
            }), 400
        
        # Check if airport exists in our dataset
        if airports_df is not None:
            if airport_id not in airports_df['AirportID'].values:
                return jsonify({
                    "error": f"Airport ID {airport_id} not found in database"
                }), 400
        
        # Make prediction
        features = [[day_of_week, airport_id]]
        
        # Get probability of delay (class 1)
        delay_probabilities = model.predict_proba(features)[0]
        delay_probability = float(delay_probabilities[1])  # Probability of delay (class 1)
        no_delay_probability = float(delay_probabilities[0])  # Probability of no delay (class 0)
        
        # Calculate confidence as the maximum probability (how sure the model is)
        confidence_percent = float(max(delay_probabilities) * 100)
        
        # Get airport name if available
        airport_name = "Unknown"
        if airports_df is not None:
            airport_row = airports_df[airports_df['AirportID'] == airport_id]
            if not airport_row.empty:
                airport_name = airport_row.iloc[0]['AirportName']
        
        # Day name mapping
        day_names = {
            1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday",
            5: "Friday", 6: "Saturday", 7: "Sunday"
        }
        
        return jsonify({
            "delay_probability": delay_probability,
            "delay_chance_percent": delay_probability * 100,
            "confidence_percent": confidence_percent,
            "no_delay_probability": no_delay_probability,
            "input": {
                "day_of_week": day_of_week,
                "day_name": day_names.get(day_of_week, "Unknown"),
                "airport_id": airport_id,
                "airport_name": airport_name
            },
            "interpretation": {
                "message": f"There is a {delay_probability*100:.2f}% chance of delay on {day_names.get(day_of_week)} at {airport_name}",
                "confidence_level": "High" if confidence_percent > 80 else "Medium" if confidence_percent > 60 else "Low"
            }
        })
        
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

@app.route('/airports', methods=['GET'])
def get_airports():
    """
    Get list of all airports sorted alphabetically by name
    
    Returns:
    {
        "airports": [
            {
                "id": integer,
                "name": string,
                "city": string,
                "state": string
            },
            ...
        ],
        "total_count": integer
    }
    """
    try:
        # Check if airports data is loaded
        if airports_df is None:
            return jsonify({"error": "Airports data not loaded"}), 500
        
        # Sort airports alphabetically by name
        sorted_airports = airports_df.sort_values('AirportName').to_dict('records')
        
        # Format response
        airports_list = []
        for airport in sorted_airports:
            airports_list.append({
                "id": int(airport['AirportID']),
                "name": airport['AirportName'],
                "city": airport['City'],
                "state": airport['State']
            })
        
        return jsonify({
            "airports": airports_list,
            "total_count": len(airports_list)
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve airports: {str(e)}"}), 500

@app.route('/airports/<int:airport_id>', methods=['GET'])
def get_airport_by_id(airport_id):
    """
    Get specific airport by ID
    
    Returns:
    {
        "airport": {
            "id": integer,
            "name": string,
            "city": string,
            "state": string
        }
    }
    """
    try:
        if airports_df is None:
            return jsonify({"error": "Airports data not loaded"}), 500
        
        airport_row = airports_df[airports_df['AirportID'] == airport_id]
        
        if airport_row.empty:
            return jsonify({"error": f"Airport with ID {airport_id} not found"}), 404
        
        airport = airport_row.iloc[0]
        
        return jsonify({
            "airport": {
                "id": int(airport['AirportID']),
                "name": airport['AirportName'],
                "city": airport['City'],
                "state": airport['State']
            }
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve airport: {str(e)}"}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({"error": "Method not allowed"}), 405

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("🚀 Starting Flight Delay Prediction API Server...")
    print("=" * 50)
    
    # Load model and data
    if load_model_and_data():
        print("✅ All data loaded successfully!")
        print("\n📋 Available endpoints:")
        print("  GET  /            - API information")
        print("  GET  /health      - Health check")
        print("  POST /predict     - Predict flight delay")
        print("  GET  /airports    - Get all airports")
        print("  GET  /airports/<id> - Get specific airport")
        print("\n🌐 Starting server on http://localhost:5000")
        print("=" * 50)
        
        # Run the Flask app
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Failed to load model and data. Server not started.")
        print("Make sure the model files exist in ../model/ and ../data/ directories")