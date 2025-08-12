#!/usr/bin/env python3
"""
Test text analysis functionality directly using Phase 1 services
"""

import sys
import os
sys.path.append('src')

from services.document_analysis_service import DocumentAnalysisService

def test_text_analysis():
    """Test the text analysis service with sample legal text"""
    
    print("🧪 Testing Text Analysis Service")
    print("=" * 50)
    
    # Read test text
    try:
        with open('test_legal_text.txt', 'r', encoding='utf-8') as f:
            test_text = f.read()
        print(f"✅ Test text loaded: {len(test_text)} characters")
    except Exception as e:
        print(f"❌ Failed to load test text: {e}")
        return
    
    # Initialize service
    try:
        service = DocumentAnalysisService()
        print("✅ DocumentAnalysisService initialized")
    except Exception as e:
        print(f"❌ Failed to initialize service: {e}")
        return
    
    # Test text analysis
    try:
        print("\n📝 Analyzing test legal text...")
        result = service.analyze_document_from_text(test_text, "comprehensive")
        
        if result.success:
            print("✅ Text analysis completed successfully")
            print(f"   Risk level: {result.risk_level}")
            print(f"   Processing time: {result.processing_time:.2f}s")
            print(f"   Legal terms found: {len(result.legal_terms)}")
            print(f"   Summary length: {len(result.summary)} characters")
            
            print("\n📋 Key Points:")
            for i, point in enumerate(result.key_points[:3], 1):
                print(f"   {i}. {point}")
                
            print("\n⚖️ Risk Analysis:")
            print(f"   Risk score: {result.risk_score}")
            print(f"   High priority risks: {len([r for r in result.risks if r.priority == 'high'])}")
            print(f"   Medium priority risks: {len([r for r in result.risks if r.priority == 'medium'])}")
            print(f"   Low priority risks: {len([r for r in result.risks if r.priority == 'low'])}")
            
        else:
            print(f"❌ Text analysis failed: {result.error}")
            
    except Exception as e:
        print(f"❌ Text analysis error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_text_analysis()

