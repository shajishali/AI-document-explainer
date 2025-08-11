"""
AI Legal Document Explainer - Main Application
FastAPI application for analyzing and explaining legal documents using AI
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Import application modules
from app.api import documents
from app.core.config import settings, validate_settings

# Load environment variables
load_dotenv()

# Create FastAPI app instance
app = FastAPI(
    title="AI Legal Document Explainer",
    description="An intelligent AI-powered system for analyzing, explaining, and extracting insights from legal documents",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(documents.router)

@app.get("/")
async def root():
    """Root endpoint with application information"""
    return {
        "message": "AI Legal Document Explainer API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2025-01-27T00:00:00Z",
        "version": "1.0.0"
    }

@app.get("/api/info")
async def api_info():
    """API information and configuration"""
    return {
        "name": "AI Legal Document Explainer API",
        "version": "1.0.0",
        "description": "AI-powered legal document analysis and explanation",
        "features": [
            "PDF Document Processing",
            "AI-Powered Analysis",
            "Legal Entity Recognition",
            "Document Summarization",
            "Interactive Visualizations"
        ],
        "tech_stack": [
            "FastAPI",
            "OpenAI",
            "LangChain",
            "LlamaIndex",
            "PyMuPDF",
            "pdfplumber"
        ]
    }

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": "The requested resource was not found",
            "path": str(request.url.path)
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Custom 500 handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "path": str(request.url.path)
        }
    )

if __name__ == "__main__":
    # Validate configuration
    validate_settings()
    
    # Get configuration from environment variables
    host = settings.host
    port = settings.port
    reload = settings.reload
    
    print(f"🚀 Starting AI Legal Document Explainer API...")
    print(f"📍 Server: http://{host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    print(f"🔄 Auto-reload: {reload}")
    
    # Run the application
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
