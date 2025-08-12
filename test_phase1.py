"""
Test script for Phase 1 implementation of AI Legal Document Explainer.

This script tests the core functionality implemented in Phase 1:
- Document processing
- Text summarization
- Risk classification
- Service orchestration
"""

import os
import sys
import logging
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from services.document_processor import DocumentProcessor
from services.summarization_service import SummarizationService
from services.basic_risk_classifier import BasicRiskClassifier
from services.document_analysis_service import DocumentAnalysisService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_document_processor():
    """Test the DocumentProcessor service."""
    print("🧪 Testing DocumentProcessor...")
    
    try:
        processor = DocumentProcessor()
        
        # Test validation
        test_file = "test_document.pdf"
        validation = processor.validate_document(test_file)
        
        if not validation['valid']:
            print(f"✅ Document validation working (expected error: {validation['error']})")
        else:
            print("❌ Document validation should have failed for non-existent file")
            return False
        
        print("✅ DocumentProcessor tests passed")
        return True
        
    except Exception as e:
        print(f"❌ DocumentProcessor test failed: {str(e)}")
        return False

def test_summarization_service():
    """Test the SummarizationService."""
    print("\n🧪 Testing SummarizationService...")
    
    try:
        # Test without API key (should work for term identification)
        service = SummarizationService()
        
        # Test legal term identification
        test_text = """
        This agreement is made between Party A and Party B. 
        Party A agrees to pay $1000 per month in rent. 
        The lease term is 12 months with automatic renewal.
        Breach of this agreement results in immediate termination.
        """
        
        terms_result = service.identify_legal_terms(test_text)
        
        if terms_result['success']:
            print(f"✅ Legal term identification working: {terms_result['total_terms']} terms found")
            for category, terms in terms_result['categories'].items():
                print(f"   {category}: {terms}")
        else:
            print(f"❌ Legal term identification failed: {terms_result['error']}")
            return False
        
        print("✅ SummarizationService tests passed")
        return True
        
    except Exception as e:
        print(f"❌ SummarizationService test failed: {str(e)}")
        return False

def test_risk_classifier():
    """Test the BasicRiskClassifier service."""
    print("\n🧪 Testing BasicRiskClassifier...")
    
    try:
        classifier = BasicRiskClassifier()
        
        # Test risk classification
        test_text = """
        This contract includes penalties of $500 for late payment.
        The agreement automatically renews for another year.
        Party A has sole discretion to modify terms.
        Breach results in immediate termination.
        """
        
        risk_result = classifier.classify_document_risks(test_text)
        
        if risk_result['success']:
            print(f"✅ Risk classification working: {risk_result['overall_risk_level']} risk level")
            print(f"   Risk score: {risk_result['overall_risk_score']}")
            print(f"   Total indicators: {risk_result['total_risk_indicators']}")
        else:
            print(f"❌ Risk classification failed: {risk_result['error']}")
            return False
        
        # Test specific risk identification
        specific_risks = classifier.identify_specific_risks(test_text)
        
        if specific_risks['success']:
            print(f"✅ Specific risk identification working:")
            print(f"   High priority: {specific_risks['total_high_priority']}")
            print(f"   Medium priority: {specific_risks['total_medium_priority']}")
            print(f"   Low priority: {specific_risks['total_low_priority']}")
        else:
            print(f"❌ Specific risk identification failed: {specific_risks['error']}")
            return False
        
        print("✅ BasicRiskClassifier tests passed")
        return True
        
    except Exception as e:
        print(f"❌ BasicRiskClassifier test failed: {str(e)}")
        return False

def test_document_analysis_service():
    """Test the main DocumentAnalysisService."""
    print("\n🧪 Testing DocumentAnalysisService...")
    
    try:
        # Test without API key (should work for basic analysis)
        service = DocumentAnalysisService()
        
        # Test text-based analysis
        test_text = """
        This lease agreement is between Tenant and Landlord.
        Monthly rent is $1500 due on the 1st of each month.
        Late payment incurs a $50 penalty.
        The lease automatically renews for 6 months.
        Either party may terminate with 30 days notice.
        """
        
        analysis_result = service.analyze_document_from_text(test_text, "comprehensive")
        
        if analysis_result['success']:
            print("✅ Document analysis working")
            print(f"   Processing time: {analysis_result['processing_time']:.2f}s")
            print(f"   Risk level: {analysis_result['risk_analysis']['overall_risk_level']}")
            print(f"   Legal terms found: {analysis_result['legal_terms']['total_terms']}")
        else:
            print(f"❌ Document analysis failed: {analysis_result['error']}")
            return False
        
        # Test service status
        status = service.get_analysis_status()
        print(f"✅ Service status: {status['service_status']}")
        
        print("✅ DocumentAnalysisService tests passed")
        return True
        
    except Exception as e:
        print(f"❌ DocumentAnalysisService test failed: {str(e)}")
        return False

def test_api_endpoints():
    """Test that the API endpoints are properly configured."""
    print("\n🧪 Testing API Configuration...")
    
    try:
        # Import main app to check endpoints
        from main import app
        
        # Check if endpoints are registered
        routes = [route.path for route in app.routes]
        required_endpoints = [
            "/",
            "/health", 
            "/api/v1/info",
            "/api/v1/upload",
            "/api/v1/analyze_text",
            "/api/v1/status",
            "/api/v1/analyze"
        ]
        
        missing_endpoints = [ep for ep in required_endpoints if ep not in routes]
        
        if not missing_endpoints:
            print("✅ All required API endpoints are registered")
            print(f"   Available endpoints: {len(routes)}")
        else:
            print(f"❌ Missing endpoints: {missing_endpoints}")
            return False
        
        print("✅ API configuration tests passed")
        return True
        
    except Exception as e:
        print(f"❌ API configuration test failed: {str(e)}")
        return False

def main():
    """Run all Phase 1 tests."""
    print("🚀 Phase 1 Testing - AI Legal Document Explainer")
    print("=" * 60)
    
    tests = [
        test_document_processor,
        test_summarization_service,
        test_risk_classifier,
        test_document_analysis_service,
        test_api_endpoints
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All Phase 1 tests passed! The system is ready for use.")
        print("\n📋 Phase 1 Features Implemented:")
        print("✅ PDF document processing and validation")
        print("✅ Text extraction and chunking")
        print("✅ AI-powered summarization (requires OpenAI API key)")
        print("✅ Legal term identification")
        print("✅ Basic risk classification")
        print("✅ Comprehensive API endpoints")
        print("✅ Service orchestration")
        
        print("\n🔧 Next Steps:")
        print("1. Set OPENAI_API_KEY environment variable for AI features")
        print("2. Test with actual PDF documents")
        print("3. Proceed to Phase 2 when ready")
        
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
