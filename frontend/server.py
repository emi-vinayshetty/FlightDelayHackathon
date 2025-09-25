# Simple HTTP Server for Frontend
# This serves the HTML file and handles CORS issues

import http.server
import socketserver
import os
import webbrowser
from urllib.parse import urlparse, parse_qs

PORT = 3000

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def start_server():
    # Change to the directory containing the HTML file
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), CORSHTTPRequestHandler) as httpd:
        print("🚀 Frontend Server Starting...")
        print("=" * 50)
        print(f"📁 Serving files from: {os.getcwd()}")
        print(f"🌐 Frontend URL: http://localhost:{PORT}")
        print(f"📱 Open in browser: http://localhost:{PORT}/index.html")
        print("=" * 50)
        print("✅ Server is ready!")
        print("💡 Make sure your API server is running on http://localhost:5000")
        print("\nPress Ctrl+C to stop the server")
        
        # Try to open browser automatically
        try:
            webbrowser.open(f'http://localhost:{PORT}/index.html')
            print("🌐 Browser opened automatically")
        except:
            print("🌐 Please open http://localhost:{PORT}/index.html in your browser")
        
        print("\n" + "=" * 50)
        httpd.serve_forever()

if __name__ == "__main__":
    start_server()