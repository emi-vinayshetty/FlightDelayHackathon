# Create a base Flask server

import pickle
from flask import Flask, request, jsonify

app = Flask(__name__)

# Enable cors
@app.after_request
def after_request(response):
    """
    Enable CORS
    """
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response


# Load model from pickle file
model = pickle.load(open('model.pkl', 'rb'))

# Model takes two parameters - day of week and airport id, then returns a prediction of flight delay
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """
    Takes two parameters - day of week and airport id, then returns a prediction of flight delay
    Accepts both GET (query parameters) and POST (JSON body) requests
    """
    try:
        # Handle POST request with JSON data
        if request.method == 'POST':
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No JSON data provided'}), 400
            
            day_of_week = data.get('day_of_week')
            airport_id = data.get('airport_id')
        
        # Handle GET request with query parameters
        else:
            day_of_week = request.args.get('day_of_week')
            airport_id = request.args.get('airport_id')
        
        # Validate parameters
        if day_of_week is None or airport_id is None:
            return jsonify({'error': 'Missing required parameters: day_of_week and airport_id'}), 400
        
        # Convert to integers
        day_of_week = int(day_of_week)
        airport_id = int(airport_id)
        
        # Validate ranges
        if day_of_week < 1 or day_of_week > 7:
            return jsonify({'error': 'day_of_week must be between 1 (Monday) and 7 (Sunday)'}), 400
        
        # Make prediction
        prediction = model.predict_proba([[day_of_week, airport_id]])[0]
        
        # Split prediction string by space
        prediction = str(prediction).split(' ')

        # store first value from prediction as certainty, and remove the first character
        certainty = float(prediction[0][2:])

        # store second value from prediction as delay, and remove the last character
        delay = float(prediction[1][:-1])

        # return prediction as json
        return jsonify({'certainty': certainty, 'delay': delay})
    
    except ValueError as e:
        return jsonify({'error': f'Invalid parameter format: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

# Create a new route called airports with method of get
@app.route('/airports', methods=['GET'])
def airports():
    # Load airports from csv file
    airports = open('airports.csv', 'r').readlines()

    # Remove first line of airports
    airports.pop(0)

    # Create list with dictionary of airports
    # First value is id, second is name
    # Convert id to integer
    # Remove last character from name
    airports = [{'id': int(airport.split(',')[0]), 'name': airport.split(',')[1][:-1]} for airport in airports]
    # Sort by name
    airports = sorted(airports, key=lambda k: k['name'])

    return jsonify(airports)

if __name__ == '__main__':
    app.run(debug=True)