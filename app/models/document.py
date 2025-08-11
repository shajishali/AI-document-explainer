"""
Data models for legal documents
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum

class DocumentStatus(str, Enum):
    """Document processing status"""
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"
    ANALYZED = "analyzed"

class DocumentType(str, Enum):
    """Types of legal documents"""
    CONTRACT = "contract"
    AGREEMENT = "agreement"
    LEGISLATION = "legislation"
    CASE_LAW = "case_law"
    REGULATION = "regulation"
    POLICY = "policy"
    OTHER = "other"

class DocumentBase(BaseModel):
    """Base document model"""
    title: str = Field(..., description="Document title")
    description: Optional[str] = Field(None, description="Document description")
    document_type: DocumentType = Field(..., description="Type of legal document")
    tags: List[str] = Field(default=[], description="Document tags for categorization")
    metadata: Dict[str, Any] = Field(default={}, description="Additional metadata")

class DocumentCreate(DocumentBase):
    """Model for creating a new document"""
    file_path: str = Field(..., description="Path to the uploaded file")
    file_size: int = Field(..., description="File size in bytes")
    file_hash: str = Field(..., description="File hash for integrity checking")

class DocumentUpdate(BaseModel):
    """Model for updating document information"""
    title: Optional[str] = None
    description: Optional[str] = None
    document_type: Optional[DocumentType] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None

class Document(DocumentBase):
    """Complete document model"""
    id: str = Field(..., description="Unique document identifier")
    file_path: str = Field(..., description="Path to the uploaded file")
    file_size: int = Field(..., description="File size in bytes")
    file_hash: str = Field(..., description="File hash for integrity checking")
    status: DocumentStatus = Field(default=DocumentStatus.UPLOADED, description="Document processing status")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Document creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Document last update timestamp")
    processed_at: Optional[datetime] = Field(None, description="Document processing completion timestamp")
    
    # Processing results
    text_content: Optional[str] = Field(None, description="Extracted text content")
    page_count: Optional[int] = Field(None, description="Number of pages in the document")
    word_count: Optional[int] = Field(None, description="Total word count")
    
    # AI Analysis results
    summary: Optional[str] = Field(None, description="AI-generated document summary")
    key_entities: Optional[List[str]] = Field(None, description="Key legal entities identified")
    legal_terms: Optional[List[str]] = Field(None, description="Legal terms found in the document")
    risk_factors: Optional[List[str]] = Field(None, description="Identified risk factors")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "doc_123456",
                "title": "Employment Contract Agreement",
                "description": "Standard employment contract for software engineers",
                "document_type": "contract",
                "tags": ["employment", "contract", "software"],
                "file_path": "/uploads/employment_contract.pdf",
                "file_size": 1024000,
                "file_hash": "sha256:abc123...",
                "status": "processed",
                "page_count": 15,
                "word_count": 2500,
                "summary": "This employment contract outlines the terms and conditions...",
                "key_entities": ["Company Inc.", "John Doe", "Software Engineer"],
                "legal_terms": ["at-will employment", "non-compete", "confidentiality"]
            }
        }
    }

class DocumentAnalysis(BaseModel):
    """Model for document analysis results"""
    document_id: str = Field(..., description="ID of the analyzed document")
    analysis_type: str = Field(..., description="Type of analysis performed")
    analysis_date: datetime = Field(default_factory=datetime.utcnow, description="Analysis timestamp")
    results: Dict[str, Any] = Field(..., description="Analysis results")
    confidence_score: Optional[float] = Field(None, description="Confidence score of the analysis")
    processing_time: Optional[float] = Field(None, description="Time taken for analysis in seconds")

class DocumentSearch(BaseModel):
    """Model for document search queries"""
    query: str = Field(..., description="Search query text")
    document_type: Optional[DocumentType] = Field(None, description="Filter by document type")
    tags: Optional[List[str]] = Field(None, description="Filter by tags")
    date_from: Optional[datetime] = Field(None, description="Filter by creation date from")
    date_to: Optional[datetime] = Field(None, description="Filter by creation date to")
    status: Optional[DocumentStatus] = Field(None, description="Filter by document status")
    limit: int = Field(default=50, description="Maximum number of results")
    offset: int = Field(default=0, description="Number of results to skip")

class DocumentResponse(BaseModel):
    """Response model for document operations"""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: Optional[Any] = Field(None, description="Response data")
    errors: Optional[List[str]] = Field(None, description="List of errors if any")

# Utility functions
def generate_document_id() -> str:
    """Generate a unique document ID"""
    import uuid
    return f"doc_{uuid.uuid4().hex[:8]}"

def validate_file_type(filename: str) -> bool:
    """Validate if the file type is supported"""
    allowed_extensions = ['.pdf']
    return any(filename.lower().endswith(ext) for ext in allowed_extensions)

def calculate_file_hash(file_path: str) -> str:
    """Calculate SHA256 hash of a file"""
    import hashlib
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return f"sha256:{hash_sha256.hexdigest()}"
