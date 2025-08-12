"""
Simple test FastAPI application to check if the environment is working.
"""

from fastapi import FastAPI
import uvicorn
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create a simple FastAPI app
app = FastAPI(title="Test App", version="1.0.0")

@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {"message": "Hello World", "status": "working"}

@app.get("/health")
async def health():
    logger.info("Health endpoint called")
    return {"status": "healthy"}

if __name__ == "__main__":
    try:
        print("Starting test application on port 8080...")
        logger.info("Starting test application...")
        uvicorn.run(app, host="127.0.0.1", port=8080, log_level="debug")
    except Exception as e:
        print(f"Error starting application: {e}")
        logger.error(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
