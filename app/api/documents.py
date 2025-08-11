"""
Document management API endpoints
"""

import os
import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from fastapi.responses import JSONResponse
import aiofiles
from datetime import datetime

from ..models.document import (
    Document, DocumentCreate, DocumentUpdate, DocumentResponse,
    DocumentStatus, DocumentType, generate_document_id, calculate_file_hash
)
from ..services.pdf_service import pdf_service
from ..core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/documents", tags=["documents"])

# In-memory storage for demo purposes (replace with database in production)
documents_db = {}

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    document_type: DocumentType = Form(DocumentType.OTHER),
    tags: Optional[str] = Form("")  # Comma-separated tags
):
    """Upload a legal document for analysis"""
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported"
            )
        
        # Validate file size
        if file.size > settings.max_file_size:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds maximum allowed size of {settings.max_file_size} bytes"
            )
        
        # Create upload directory if it doesn't exist
        os.makedirs(settings.upload_dir, exist_ok=True)
        
        # Generate unique filename
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{file.filename.replace(' ', '_')}"
        file_path = os.path.join(settings.upload_dir, safe_filename)
        
        # Save uploaded file
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Calculate file hash
        file_hash = calculate_file_hash(file_path)
        
        # Parse tags
        tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()] if tags else []
        
        # Create document record
        document_id = generate_document_id()
        document_data = DocumentCreate(
            title=title,
            description=description,
            document_type=document_type,
            tags=tag_list,
            file_path=file_path,
            file_size=file.size,
            file_hash=file_hash
        )
        
        # Create document instance
        document = Document(
            id=document_id,
            **document_data.dict()
        )
        
        # Store in database (replace with actual database in production)
        documents_db[document_id] = document
        
        logger.info(f"Document uploaded successfully: {document_id}")
        
        return DocumentResponse(
            success=True,
            message="Document uploaded successfully",
            data=document
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/", response_model=DocumentResponse)
async def list_documents(
    skip: int = 0,
    limit: int = 50,
    document_type: Optional[DocumentType] = None,
    status: Optional[DocumentStatus] = None
):
    """List all documents with optional filtering"""
    try:
        # Filter documents
        filtered_docs = list(documents_db.values())
        
        if document_type:
            filtered_docs = [doc for doc in filtered_docs if doc.document_type == document_type]
        
        if status:
            filtered_docs = [doc for doc in filtered_docs if doc.status == status]
        
        # Apply pagination
        total_count = len(filtered_docs)
        paginated_docs = filtered_docs[skip:skip + limit]
        
        return DocumentResponse(
            success=True,
            message=f"Retrieved {len(paginated_docs)} documents",
            data={
                "documents": paginated_docs,
                "total_count": total_count,
                "skip": skip,
                "limit": limit
            }
        )
        
    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str):
    """Get a specific document by ID"""
    try:
        if document_id not in documents_db:
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )
        
        document = documents_db[document_id]
        
        return DocumentResponse(
            success=True,
            message="Document retrieved successfully",
            data=document
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving document {document_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: str,
    document_update: DocumentUpdate
):
    """Update document information"""
    try:
        if document_id not in documents_db:
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )
        
        document = documents_db[document_id]
        
        # Update fields
        update_data = document_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(document, field, value)
        
        # Update timestamp
        document.updated_at = datetime.utcnow()
        
        # Update in database
        documents_db[document_id] = document
        
        logger.info(f"Document updated successfully: {document_id}")
        
        return DocumentResponse(
            success=True,
            message="Document updated successfully",
            data=document
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating document {document_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.delete("/{document_id}", response_model=DocumentResponse)
async def delete_document(document_id: str):
    """Delete a document"""
    try:
        if document_id not in documents_db:
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )
        
        document = documents_db[document_id]
        
        # Remove file from filesystem
        try:
            if os.path.exists(document.file_path):
                os.remove(document.file_path)
                logger.info(f"File removed: {document.file_path}")
        except Exception as e:
            logger.warning(f"Could not remove file {document.file_path}: {str(e)}")
        
        # Remove from database
        del documents_db[document_id]
        
        logger.info(f"Document deleted successfully: {document_id}")
        
        return DocumentResponse(
            success=True,
            message="Document deleted successfully",
            data={"id": document_id}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document {document_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/{document_id}/process", response_model=DocumentResponse)
async def process_document(document_id: str):
    """Process a document to extract text and metadata"""
    try:
        if document_id not in documents_db:
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )
        
        document = documents_db[document_id]
        
        # Check if document is already processed
        if document.status in [DocumentStatus.PROCESSED, DocumentStatus.ANALYZED]:
            return DocumentResponse(
                success=True,
                message="Document already processed",
                data=document
            )
        
        # Update status to processing
        document.status = DocumentStatus.PROCESSING
        documents_db[document_id] = document
        
        try:
            # Extract text using PDF service
            text_content, metadata = pdf_service.extract_text(document.file_path)
            
            # Update document with extracted information
            document.text_content = text_content
            document.page_count = metadata.get("total_pages", 0)
            document.word_count = metadata.get("total_words", 0)
            document.status = DocumentStatus.PROCESSED
            document.processed_at = datetime.utcnow()
            document.updated_at = datetime.utcnow()
            
            # Store additional metadata
            document.metadata.update(metadata)
            
            # Update in database
            documents_db[document_id] = document
            
            logger.info(f"Document processed successfully: {document_id}")
            
            return DocumentResponse(
                success=True,
                message="Document processed successfully",
                data=document
            )
            
        except Exception as e:
            # Update status to failed
            document.status = DocumentStatus.FAILED
            document.updated_at = datetime.utcnow()
            documents_db[document_id] = document
            
            logger.error(f"Error processing document {document_id}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error processing document: {str(e)}"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing document {document_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/{document_id}/text")
async def get_document_text(document_id: str):
    """Get the extracted text content of a document"""
    try:
        if document_id not in documents_db:
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )
        
        document = documents_db[document_id]
        
        if not document.text_content:
            raise HTTPException(
                status_code=400,
                detail="Document text not yet extracted. Process the document first."
            )
        
        return {
            "document_id": document_id,
            "title": document.title,
            "text_content": document.text_content,
            "page_count": document.page_count,
            "word_count": document.word_count
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving document text {document_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
