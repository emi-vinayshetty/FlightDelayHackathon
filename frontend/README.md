# Flight Delay Predictor Frontend

## 🎯 Overview
This is a modern, responsive web frontend for the Flight Delay Prediction API. It provides an intuitive user interface to predict flight delays based on day of the week and origin airport.

## ✨ Features
- **🗓️ Day Selection**: Choose any day of the week
- **🛫 Airport Selection**: Dynamically loaded from API, sorted alphabetically
- **🤖 Real-time Predictions**: Calls the machine learning API
- **📊 Visual Results**: Beautiful cards showing delay probabilities
- **📱 Responsive Design**: Works on desktop, tablet, and mobile
- **🔄 Error Handling**: Graceful handling of API errors
- **⚡ Modern UI**: Gradient backgrounds, smooth animations

## 🚀 Quick Start

### Prerequisites
- API server running on http://localhost:5000
- Python 3.x installed

### Method 1: Using Python Server (Recommended)
```bash
# Navigate to frontend directory
cd frontend

# Start the frontend server
python server.py
```

The frontend will be available at: http://localhost:3000

### Method 2: Direct File Opening
Simply open `index.html` in your web browser. Note: You may encounter CORS issues with this method.

## 🎮 How to Use

1. **Start the API Server** (if not already running):
   ```bash
   cd possible-solution/server
   python app.py
   ```

2. **Start the Frontend Server**:
   ```bash
   cd frontend
   python server.py
   ```

3. **Open your browser** to http://localhost:3000

4. **Make a prediction**:
   - Select a day of the week
   - Choose an origin airport from the dropdown
   - Click "Predict Flight Delay"
   - View the results!

## 📊 What You'll See

The interface will show:
- **Delay Probability**: Chance the flight will be delayed >15 minutes
- **On-Time Probability**: Chance the flight will be on time
- **Interpretation**: Easy-to-understand explanation
- **Flight Details**: Selected day and airport information

## 🔧 Technical Details

### Frontend Stack
- **HTML5**: Semantic structure
- **CSS3**: Modern styling with gradients and animations
- **Vanilla JavaScript**: No frameworks, pure ES6+
- **Fetch API**: For API communication

### API Integration
- Supports both GET and POST methods
- Automatic fallback between request methods
- Comprehensive error handling
- CORS-enabled communication

### Responsive Design
- Mobile-first approach
- CSS Grid and Flexbox
- Smooth animations and transitions
- Touch-friendly interface

## 🎨 Styling Features
- **Gradient Backgrounds**: Beautiful purple-blue gradients
- **Card Layout**: Clean, modern card-based design
- **Loading States**: Visual feedback during API calls
- **Color-coded Results**: Green for low delay risk, red for high risk
- **Smooth Animations**: Hover effects and transitions

## ✅ Success Criteria Met

As per the requirements in `3-create-frontend.md`:

1. ✅ **UI displays list of days of the week** - Dropdown with all 7 days
2. ✅ **UI displays list of airports** - Dynamic dropdown loaded from API
3. ✅ **API is called after user selection** - Prediction API called with selected values
4. ✅ **Result is displayed to user** - Beautiful result cards with interpretation

## 🔍 Troubleshooting

### API Connection Issues
- Make sure the API server is running on http://localhost:5000
- Check browser console for error messages
- Verify CORS is enabled on the API server

### Frontend Server Issues
- Make sure port 3000 is available
- Try opening index.html directly if server fails

### Browser Compatibility
- Works in all modern browsers (Chrome, Firefox, Safari, Edge)
- Requires JavaScript enabled
- Uses modern CSS features (Grid, Flexbox)

## 🌟 Future Enhancements
- Client-side caching of airport data
- Historical prediction tracking
- Multiple airport comparison
- Weather data integration
- Mobile app version