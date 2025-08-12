"""
Simple HTTP server for testing.
"""

import http.server
import socketserver
import threading
import time

def start_server():
    PORT = 8000
    
    class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                response = """
                <html>
                <head><title>AI Legal Document Explainer</title></head>
                <body>
                    <h1>AI Legal Document Explainer</h1>
                    <p>Server is running successfully!</p>
                    <p>Status: Healthy</p>
                    <p>Version: 1.0.0</p>
                </body>
                </html>
                """
                self.wfile.write(response.encode())
            elif self.path == '/health':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = '{"status": "healthy", "message": "Server is operational"}'
                self.wfile.write(response.encode())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Not Found')
    
    try:
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            print(f"Server started at http://localhost:{PORT}")
            print("Press Ctrl+C to stop the server")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.shutdown()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    start_server()
