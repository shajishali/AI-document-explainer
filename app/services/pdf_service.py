"""
PDF processing service for legal documents
"""

import os
import logging
from typing import Dict, Any, Optional, Tuple
from pathlib import Path
import pdfplumber
import fitz  # PyMuPDF
from PIL import Image
import io

logger = logging.getLogger(__name__)

class PDFProcessingService:
    """Service for processing PDF documents"""
    
    def __init__(self):
        self.supported_extensions = ['.pdf']
    
    def validate_pdf(self, file_path: str) -> bool:
        """Validate if the file is a valid PDF"""
        try:
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return False
            
            if not any(file_path.lower().endswith(ext) for ext in self.supported_extensions):
                logger.error(f"Unsupported file type: {file_path}")
                return False
            
            # Try to open with PyMuPDF to validate
            with fitz.open(file_path) as doc:
                if doc.page_count == 0:
                    logger.error(f"PDF has no pages: {file_path}")
                    return False
                
            return True
            
        except Exception as e:
            logger.error(f"Error validating PDF {file_path}: {str(e)}")
            return False
    
    def extract_text_with_pdfplumber(self, file_path: str) -> Tuple[str, Dict[str, Any]]:
        """Extract text using pdfplumber for better text extraction"""
        try:
            text_content = ""
            metadata = {
                "pages": [],
                "total_pages": 0,
                "total_words": 0,
                "extraction_method": "pdfplumber"
            }
            
            with pdfplumber.open(file_path) as pdf:
                metadata["total_pages"] = len(pdf.pages)
                
                for page_num, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text_content += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
                        
                        # Store page metadata
                        page_meta = {
                            "page_number": page_num + 1,
                            "word_count": len(page_text.split()),
                            "char_count": len(page_text),
                            "width": page.width,
                            "height": page.height
                        }
                        metadata["pages"].append(page_meta)
                        metadata["total_words"] += page_meta["word_count"]
                
                # Add PDF metadata
                if pdf.metadata:
                    metadata["pdf_metadata"] = pdf.metadata
                
            logger.info(f"Successfully extracted text from {file_path} using pdfplumber")
            return text_content.strip(), metadata
            
        except Exception as e:
            logger.error(f"Error extracting text with pdfplumber from {file_path}: {str(e)}")
            raise
    
    def extract_text_with_pymupdf(self, file_path: str) -> Tuple[str, Dict[str, Any]]:
        """Extract text using PyMuPDF for coordinate information"""
        try:
            text_content = ""
            metadata = {
                "pages": [],
                "total_pages": 0,
                "total_words": 0,
                "extraction_method": "pymupdf"
            }
            
            with fitz.open(file_path) as doc:
                metadata["total_pages"] = doc.page_count
                
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    page_text = page.get_text()
                    
                    if page_text:
                        text_content += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
                        
                        # Store page metadata with coordinates
                        page_meta = {
                            "page_number": page_num + 1,
                            "word_count": len(page_text.split()),
                            "char_count": len(page_text),
                            "width": page.rect.width,
                            "height": page.rect.height,
                            "rotation": page.rotation
                        }
                        metadata["pages"].append(page_meta)
                        metadata["total_words"] += page_meta["word_count"]
                
                # Add PDF metadata
                metadata["pdf_metadata"] = doc.metadata
                
            logger.info(f"Successfully extracted text from {file_path} using PyMuPDF")
            return text_content.strip(), metadata
            
        except Exception as e:
            logger.error(f"Error extracting text with PyMuPDF from {file_path}: {str(e)}")
            raise
    
    def extract_text(self, file_path: str, method: str = "pdfplumber") -> Tuple[str, Dict[str, Any]]:
        """Extract text from PDF using specified method"""
        if not self.validate_pdf(file_path):
            raise ValueError(f"Invalid PDF file: {file_path}")
        
        if method == "pdfplumber":
            return self.extract_text_with_pdfplumber(file_path)
        elif method == "pymupdf":
            return self.extract_text_with_pymupdf(file_path)
        else:
            raise ValueError(f"Unsupported extraction method: {method}")
    
    def get_page_as_image(self, file_path: str, page_number: int = 0, dpi: int = 150) -> Optional[Image.Image]:
        """Convert a specific page to an image"""
        try:
            with fitz.open(file_path) as doc:
                if page_number >= doc.page_count:
                    logger.error(f"Page {page_number} does not exist in {file_path}")
                    return None
                
                page = doc.load_page(page_number)
                mat = fitz.Matrix(dpi/72, dpi/72)  # Convert DPI to zoom factor
                pix = page.get_pixmap(matrix=mat)
                
                # Convert to PIL Image
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                
                logger.info(f"Successfully converted page {page_number} to image from {file_path}")
                return img
                
        except Exception as e:
            logger.error(f"Error converting page {page_number} to image from {file_path}: {str(e)}")
            return None
    
    def extract_text_with_coordinates(self, file_path: str) -> Dict[str, Any]:
        """Extract text with coordinate information for highlighting"""
        try:
            result = {
                "text_blocks": [],
                "total_pages": 0,
                "extraction_method": "coordinates"
            }
            
            with fitz.open(file_path) as doc:
                result["total_pages"] = doc.page_count
                
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    blocks = page.get_text("dict")
                    
                    page_blocks = []
                    for block in blocks["blocks"]:
                        if "lines" in block:
                            for line in block["lines"]:
                                for span in line["spans"]:
                                    text_block = {
                                        "page": page_num + 1,
                                        "text": span["text"],
                                        "bbox": span["bbox"],  # [x0, y0, x1, y1]
                                        "font": span["font"],
                                        "size": span["size"],
                                        "color": span["color"]
                                    }
                                    page_blocks.append(text_block)
                    
                    result["text_blocks"].extend(page_blocks)
                
            logger.info(f"Successfully extracted text with coordinates from {file_path}")
            return result
            
        except Exception as e:
            logger.error(f"Error extracting text with coordinates from {file_path}: {str(e)}")
            raise
    
    def get_document_info(self, file_path: str) -> Dict[str, Any]:
        """Get comprehensive document information"""
        try:
            info = {
                "file_path": file_path,
                "file_size": os.path.getsize(file_path),
                "file_name": os.path.basename(file_path)
            }
            
            with fitz.open(file_path) as doc:
                info.update({
                    "page_count": doc.page_count,
                    "metadata": doc.metadata,
                    "is_encrypted": doc.needs_pass,
                    "is_scanned": self._is_scanned_document(doc)
                })
                
                # Get first page dimensions
                if doc.page_count > 0:
                    first_page = doc.load_page(0)
                    info["page_dimensions"] = {
                        "width": first_page.rect.width,
                        "height": first_page.rect.height
                    }
            
            return info
            
        except Exception as e:
            logger.error(f"Error getting document info for {file_path}: {str(e)}")
            raise
    
    def _is_scanned_document(self, doc) -> bool:
        """Check if the document appears to be scanned"""
        try:
            # Simple heuristic: check if text extraction yields very little text
            total_text = ""
            for page_num in range(min(3, doc.page_count)):  # Check first 3 pages
                page = doc.load_page(page_num)
                total_text += page.get_text()
            
            # If we get very little text, it's likely scanned
            return len(total_text.strip()) < 100
            
        except:
            return False
    
    def cleanup_text(self, text: str) -> str:
        """Clean up extracted text"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = " ".join(text.split())
        
        # Remove page separators
        text = text.replace("--- Page", "\n\n")
        
        # Basic cleanup
        text = text.replace("  ", " ")
        text = text.strip()
        
        return text

# Create global service instance
pdf_service = PDFProcessingService()
