"""
Server runner script for Windows to keep the FastAPI server running.
"""

import subprocess
import sys
import time

def main():
    print("Starting AI Legal Document Explainer server...")
    print("This script will keep the server running.")
    print("Press Ctrl+C to stop the server.")
    print()
    
    try:
        # Start the server using subprocess
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "127.0.0.1", 
            "--port", "8000", 
            "--reload"
        ])
        
        print(f"Server started with PID: {process.pid}")
        print("Server is running at: http://127.0.0.1:8000")
        print("API docs: http://127.0.0.1:8000/docs")
        print("Health check: http://127.0.0.1:8000/health")
        print()
        print("Waiting for server to respond...")
        
        # Wait for the process to complete
        process.wait()
        
    except KeyboardInterrupt:
        print("\nShutting down server...")
        if 'process' in locals():
            process.terminate()
            process.wait()
        print("Server stopped.")
    except Exception as e:
        print(f"Error: {e}")
        if 'process' in locals():
            process.terminate()
        sys.exit(1)

if __name__ == "__main__":
    main()

