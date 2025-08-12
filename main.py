"""
AI Legal Document Explainer - Main Application

A FastAPI-based application for analyzing and explaining legal documents using AI.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from typing import Dict, Any, Optional
import logging
import os
import tempfile
from pathlib import Path

# Import our Phase 1 services
from src.services.document_analysis_service import DocumentAnalysisService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Legal Document Explainer",
    description="An intelligent system for analyzing and explaining legal documents using AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Initialize the document analysis service
document_analysis_service = None

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class HealthResponse(BaseModel):
    status: str
    message: str
    version: str

class DocumentAnalysisRequest(BaseModel):
    document_url: str = None
    document_text: str = None
    analysis_type: str = "comprehensive"  # basic, comprehensive, risk_focused

class DocumentAnalysisResponse(BaseModel):
    success: bool
    summary: str
    key_points: list[str]
    legal_terms: list[str]
    confidence_score: float
    risk_level: str
    processing_time: float
    error: Optional[str] = None

class DocumentUploadResponse(BaseModel):
    success: bool
    message: str
    file_name: str
    file_size: int
    analysis_results: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

# Health check endpoint
@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint with health check information."""
    return HealthResponse(
        status="healthy",
        message="AI Legal Document Explainer is running successfully!",
        version="1.0.0"
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for monitoring."""
    return HealthResponse(
        status="healthy",
        message="Service is operational",
        version="1.0.0"
    )

@app.get("/api/v1/info")
async def get_api_info():
    """Get API information and capabilities."""
    return {
        "name": "AI Legal Document Explainer API",
        "version": "1.0.0",
        "description": "API for analyzing and explaining legal documents using AI",
        "endpoints": {
            "health": "/health",
            "upload": "/api/v1/upload",
            "analyze": "/api/v1/analyze",
            "analyze_text": "/api/v1/analyze_text",
            "status": "/api/v1/status",
            "info": "/api/v1/info"
        },
        "supported_formats": ["PDF"],
        "analysis_types": ["basic", "comprehensive", "risk_focused"],
        "phase": "Phase 1 - Foundation & Core Document Processing"
    }

@app.post("/api/v1/upload", response_model=DocumentUploadResponse)
async def upload_and_analyze_document(
    file: UploadFile = File(...),
    analysis_type: str = Form("comprehensive")
):
    """
    Upload and analyze a legal document (PDF).
    
    This endpoint implements Phase 1 functionality:
    - PDF document processing and validation
    - Text extraction and chunking
    - AI-powered summarization
    - Basic risk classification
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400, 
                detail="Only PDF files are supported in Phase 1"
            )
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Initialize service if not already done
            global document_analysis_service
            if document_analysis_service is None:
                # Get OpenAI API key from environment
                openai_api_key = os.getenv('OPENAI_API_KEY')
                document_analysis_service = DocumentAnalysisService(openai_api_key)
            
            # Analyze document
            analysis_results = document_analysis_service.analyze_document(
                temp_file_path, 
                analysis_type
            )
            
            # Clean up temporary file
            os.unlink(temp_file_path)
            
            if analysis_results['success']:
                return DocumentUploadResponse(
                    success=True,
                    message="Document analyzed successfully",
                    file_name=file.filename,
                    file_size=len(content),
                    analysis_results=analysis_results
                )
            else:
                return DocumentUploadResponse(
                    success=False,
                    message="Document analysis failed",
                    file_name=file.filename,
                    file_size=len(content),
                    error=analysis_results.get('error', 'Unknown error')
                )
                
        except Exception as e:
            # Clean up temporary file on error
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            raise e
            
    except Exception as e:
        logger.error(f"Document upload and analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/analyze_text", response_model=DocumentAnalysisResponse)
async def analyze_text(request: DocumentAnalysisRequest):
    """
    Analyze legal document text directly.
    
    This endpoint implements Phase 1 functionality for text input:
    - Legal term identification
    - Text summarization
    - Risk classification
    """
    try:
        if not request.document_text:
            raise HTTPException(
                status_code=400, 
                detail="Document text is required"
            )
        
        # Initialize service if not already done
        global document_analysis_service
        if document_analysis_service is None:
            openai_api_key = os.getenv('OPENAI_API_KEY')
            document_analysis_service = DocumentAnalysisService(openai_api_key)
        
        # Analyze text
        analysis_results = document_analysis_service.analyze_document_from_text(
            request.document_text,
            request.analysis_type
        )
        
        if analysis_results['success']:
            # Extract key points from summary
            summary = analysis_results['summary']['summary']
            key_points = self._extract_key_points(summary)
            
            # Extract legal terms
            legal_terms = []
            if analysis_results['legal_terms']['success']:
                for category, terms in analysis_results['legal_terms']['categories'].items():
                    legal_terms.extend(terms)
            
            return DocumentAnalysisResponse(
                success=True,
                summary=summary,
                key_points=key_points,
                legal_terms=legal_terms,
                confidence_score=analysis_results['summary']['confidence_score'],
                risk_level=analysis_results['risk_analysis']['overall_risk_level'],
                processing_time=analysis_results['processing_time']
            )
        else:
            return DocumentAnalysisResponse(
                success=False,
                summary="",
                key_points=[],
                legal_terms=[],
                confidence_score=0.0,
                risk_level="unknown",
                processing_time=0.0,
                error=analysis_results.get('error', 'Unknown error')
            )
            
    except Exception as e:
        logger.error(f"Text analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/status")
async def get_service_status():
    """Get the current status of the analysis services."""
    try:
        global document_analysis_service
        if document_analysis_service is None:
            return {
                "service_status": "not_initialized",
                "message": "Document analysis service not yet initialized"
            }
        
        return document_analysis_service.get_analysis_status()
        
    except Exception as e:
        logger.error(f"Status check error: {str(e)}")
        return {
            "service_status": "error",
            "error": str(e)
        }

@app.post("/api/v1/analyze", response_model=DocumentAnalysisResponse)
async def analyze_document(request: DocumentAnalysisRequest):
    """
    Analyze a legal document and provide insights.
    
    This endpoint is maintained for backward compatibility.
    For new implementations, use /api/v1/upload for file uploads
    or /api/v1/analyze_text for text analysis.
    """
    logger.info(f"Document analysis request received: {request.analysis_type}")
    
    if request.document_text:
        # Redirect to text analysis endpoint
        return await analyze_text(request)
    elif request.document_url:
        # TODO: Implement URL-based analysis in future phases
        raise HTTPException(
            status_code=501, 
            detail="URL-based analysis not implemented in Phase 1"
        )
    else:
        raise HTTPException(
            status_code=400, 
            detail="Either document_text or document_url must be provided"
        )

def _extract_key_points(summary: str) -> list[str]:
    """Extract key points from summary text."""
    try:
        # Simple extraction - split by sentences and take first few
        sentences = summary.split('. ')
        key_points = []
        
        for sentence in sentences[:5]:  # Take first 5 sentences
            sentence = sentence.strip()
            if sentence and len(sentence) > 10:
                key_points.append(sentence + '.')
        
        return key_points
    except Exception as e:
        logger.error(f"Key points extraction error: {str(e)}")
        return ["Key points extraction failed"]

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors gracefully."""
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint not found", "message": "The requested endpoint does not exist"}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handle internal server errors gracefully."""
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "message": "Something went wrong on our end"}
    )

if __name__ == "__main__":
    """Run the application directly."""
    logger.info("Starting AI Legal Document Explainer...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
