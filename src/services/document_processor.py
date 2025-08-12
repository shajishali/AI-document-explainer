"""
Document Processor Service for AI Legal Document Explainer

Handles PDF document processing, text extraction, and chunking for AI analysis.
"""

import fitz  # PyMuPDF
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import hashlib
import json

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Handles PDF document processing and text extraction."""
    
    def __init__(self):
        self.supported_formats = ['.pdf']
        self.max_file_size = 50 * 1024 * 1024  # 50MB limit
        
    def validate_document(self, file_path: str) -> Dict[str, Any]:
        """
        Validate uploaded document for processing.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Dict containing validation results and metadata
        """
        try:
            path = Path(file_path)
            
            # Check file extension
            if path.suffix.lower() not in self.supported_formats:
                return {
                    'valid': False,
                    'error': f'Unsupported file format. Supported: {", ".join(self.supported_formats)}'
                }
            
            # Check file size
            file_size = path.stat().st_size
            if file_size > self.max_file_size:
                return {
                    'valid': False,
                    'error': f'File too large. Maximum size: {self.max_file_size // (1024*1024)}MB'
                }
            
            # Check if file exists and is readable
            if not path.exists():
                return {
                    'valid': False,
                    'error': 'File not found'
                }
            
            return {
                'valid': True,
                'file_size': file_size,
                'file_name': path.name,
                'file_extension': path.suffix.lower()
            }
            
        except Exception as e:
            logger.error(f"Document validation error: {str(e)}")
            return {
                'valid': False,
                'error': f'Validation error: {str(e)}'
            }
    
    def extract_text(self, file_path: str) -> Dict[str, Any]:
        """
        Extract text content from PDF document.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Dict containing extracted text and metadata
        """
        try:
            # Validate document first
            validation = self.validate_document(file_path)
            if not validation['valid']:
                return {
                    'success': False,
                    'error': validation['error']
                }
            
            # Open PDF with PyMuPDF
            doc = fitz.open(file_path)
            
            # Extract text from each page
            pages_text = []
            total_pages = len(doc)
            
            for page_num in range(total_pages):
                page = doc.load_page(page_num)
                text = page.get_text()
                pages_text.append({
                    'page_number': page_num + 1,
                    'text': text,
                    'text_length': len(text)
                })
            
            # Calculate document hash for caching
            doc_hash = self._calculate_document_hash(file_path)
            
            doc.close()
            
            return {
                'success': True,
                'total_pages': total_pages,
                'pages': pages_text,
                'total_text_length': sum(page['text_length'] for page in pages_text),
                'document_hash': doc_hash,
                'file_path': file_path
            }
            
        except Exception as e:
            logger.error(f"Text extraction error: {str(e)}")
            return {
                'success': False,
                'error': f'Text extraction failed: {str(e)}'
            }
    
    def chunk_document(self, extracted_text: Dict[str, Any], chunk_size: int = 1000, overlap: int = 200) -> Dict[str, Any]:
        """
        Split document text into chunks for AI processing.
        
        Args:
            extracted_text: Output from extract_text method
            chunk_size: Maximum characters per chunk
            overlap: Number of characters to overlap between chunks
            
        Returns:
            Dict containing text chunks and metadata
        """
        try:
            if not extracted_text['success']:
                return {
                    'success': False,
                    'error': 'Cannot chunk invalid extracted text'
                }
            
            chunks = []
            chunk_id = 0
            
            for page in extracted_text['pages']:
                text = page['text']
                page_num = page['page_number']
                
                # Split page text into chunks
                page_chunks = self._split_text_into_chunks(
                    text, chunk_size, overlap, page_num, chunk_id
                )
                chunks.extend(page_chunks)
                chunk_id += len(page_chunks)
            
            return {
                'success': True,
                'total_chunks': len(chunks),
                'chunk_size': chunk_size,
                'overlap': overlap,
                'chunks': chunks,
                'document_hash': extracted_text['document_hash']
            }
            
        except Exception as e:
            logger.error(f"Document chunking error: {str(e)}")
            return {
                'success': False,
                'error': f'Chunking failed: {str(e)}'
            }
    
    def _split_text_into_chunks(self, text: str, chunk_size: int, overlap: int, page_num: int, start_chunk_id: int) -> List[Dict[str, Any]]:
        """Split text into overlapping chunks."""
        chunks = []
        chunk_id = start_chunk_id
        
        if len(text) <= chunk_size:
            chunks.append({
                'chunk_id': chunk_id,
                'page_number': page_num,
                'text': text,
                'start_char': 0,
                'end_char': len(text),
                'chunk_size': len(text)
            })
        else:
            start = 0
            while start < len(text):
                end = start + chunk_size
                
                # Try to break at word boundary
                if end < len(text):
                    # Look for the last space in the chunk
                    last_space = text.rfind(' ', start, end)
                    if last_space > start:
                        end = last_space + 1
                
                chunk_text = text[start:end]
                
                chunks.append({
                    'chunk_id': chunk_id,
                    'page_number': page_num,
                    'text': chunk_text,
                    'start_char': start,
                    'end_char': end,
                    'chunk_size': len(chunk_text)
                })
                
                chunk_id += 1
                start = end - overlap
                
                if start >= len(text):
                    break
        
        return chunks
    
    def _calculate_document_hash(self, file_path: str) -> str:
        """Calculate SHA-256 hash of document for caching purposes."""
        try:
            with open(file_path, 'rb') as f:
                file_hash = hashlib.sha256()
                chunk = f.read(8192)
                while chunk:
                    file_hash.update(chunk)
                    chunk = f.read(8192)
            return file_hash.hexdigest()
        except Exception as e:
            logger.error(f"Hash calculation error: {str(e)}")
            return ""

    def process_document(self, file_path: str, chunk_size: int = 1000, overlap: int = 200) -> Dict[str, Any]:
        """
        Complete document processing pipeline.
        
        Args:
            file_path: Path to the document file
            chunk_size: Maximum characters per chunk
            overlap: Number of characters to overlap between chunks
            
        Returns:
            Dict containing complete processing results
        """
        try:
            # Step 1: Extract text
            extraction_result = self.extract_text(file_path)
            if not extraction_result['success']:
                return extraction_result
            
            # Step 2: Chunk document
            chunking_result = self.chunk_document(extraction_result, chunk_size, overlap)
            if not chunking_result['success']:
                return chunking_result
            
            # Combine results
            return {
                'success': True,
                'document_info': {
                    'file_path': file_path,
                    'file_name': Path(file_path).name,
                    'total_pages': extraction_result['total_pages'],
                    'total_text_length': extraction_result['total_text_length'],
                    'document_hash': extraction_result['document_hash']
                },
                'processing_info': {
                    'chunk_size': chunk_size,
                    'overlap': overlap,
                    'total_chunks': chunking_result['total_chunks']
                },
                'chunks': chunking_result['chunks'],
                'processing_time': None  # Will be set by calling function
            }
            
        except Exception as e:
            logger.error(f"Document processing error: {str(e)}")
            return {
                'success': False,
                'error': f'Document processing failed: {str(e)}'
            }
