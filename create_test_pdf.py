#!/usr/bin/env python3
"""
Create a test PDF document for Phase 1 testing
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

def create_test_pdf():
    """Create a simple test PDF with legal-like content"""
    
    filename = "test_legal_document.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 100, "Test Legal Agreement")
    
    # Content
    c.setFont("Helvetica", 12)
    y_position = height - 150
    
    content = [
        "This is a test legal document for Phase 1 testing.",
        "",
        "TERMS AND CONDITIONS:",
        "1. This agreement is entered into between Party A and Party B.",
        "2. The term of this agreement shall be 12 months with automatic renewal.",
        "3. Either party may terminate this agreement with 30 days written notice.",
        "4. Breach of any term may result in immediate termination.",
        "5. This agreement is governed by the laws of the jurisdiction.",
        "",
        "RISK CLAUSES:",
        "6. High-risk clause: Automatic renewal without consent.",
        "7. Medium-risk clause: 30-day termination notice.",
        "8. Low-risk clause: Standard governing law provision.",
        "",
        "This document contains various risk levels for testing purposes."
    ]
    
    for line in content:
        c.drawString(100, y_position, line)
        y_position -= 20
    
    c.save()
    print(f"✅ Test PDF created: {filename}")
    print(f"   File size: {len(open(filename, 'rb').read())} bytes")
    return filename

if __name__ == "__main__":
    create_test_pdf()

