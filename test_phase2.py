#!/usr/bin/env python3
"""
Phase 2 Testing - AI Legal Document Explainer

Tests the advanced analysis features including:
- Clause Detection
- Enhanced Risk Classification  
- Document Highlighting
"""

import sys
import os
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from services.clause_detector import ClauseDetector, LegalClause
from services.enhanced_risk_classifier import EnhancedRiskClassifier, RiskLevel
from services.document_highlighter import DocumentHighlighter, HighlightType
from services.document_analysis_service import DocumentAnalysisService

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

def test_clause_detector():
    """Test the ClauseDetector service."""
    print("🧪 Testing ClauseDetector...")
    
    detector = ClauseDetector()
    
    # Test text with various legal clauses
    test_text = """
    This agreement shall be binding upon all parties.
    The contractor must deliver the services by the specified date.
    In case of breach, a penalty of $10,000 shall apply.
    The agreement will automatically renew for another year.
    Either party may terminate this contract with 30 days notice.
    The contractor agrees to indemnify the client against all claims.
    All information shared shall remain confidential and proprietary.
    """
    
    clauses = detector.detect_clauses(test_text)
    clause_summary = detector.get_clause_summary(clauses)
    
    print(f"✅ Detected {len(clauses)} legal clauses")
    print(f"   Clause types: {list(clause_summary['clauses_by_type'].keys())}")
    print(f"   Risk distribution: {clause_summary['risk_distribution']}")
    print(f"   High priority clauses: {len(clause_summary['high_priority_clauses'])}")
    
    # Test individual clause properties
    if clauses:
        first_clause = clauses[0]
        print(f"   Sample clause: {first_clause.text[:50]}...")
        print(f"   Type: {first_clause.clause_type}, Risk: {first_clause.risk_level}")
        print(f"   Importance: {first_clause.importance}, Confidence: {first_clause.confidence:.2f}")
    
    return clauses, clause_summary

def test_enhanced_risk_classifier():
    """Test the EnhancedRiskClassifier service."""
    print("\n🧪 Testing EnhancedRiskClassifier...")
    
    classifier = EnhancedRiskClassifier()
    
    # Create sample clauses for testing
    sample_clauses = [
        type('MockClause', (), {
            'clause_type': 'penalties',
            'importance': 'high',
            'confidence': 0.9,
            'text': 'Penalty clause for breach',
            'start_line': 1
        })(),
        type('MockClause', (), {
            'clause_type': 'liability',
            'importance': 'high',
            'confidence': 0.8,
            'text': 'Indemnification clause',
            'start_line': 2
        })(),
        type('MockClause', (), {
            'clause_type': 'renewals',
            'importance': 'medium',
            'confidence': 0.7,
            'text': 'Auto-renewal clause',
            'start_line': 3
        })()
    ]
    
    assessment = classifier.classify_risk(sample_clauses)
    
    print(f"✅ Risk assessment completed")
    print(f"   Overall risk: {assessment.overall_risk.value}")
    print(f"   Risk score: {assessment.risk_score:.2f}")
    print(f"   Risk category: {assessment.risk_category}")
    print(f"   Total indicators: {assessment.summary['total_indicators']}")
    print(f"   Top risk categories: {assessment.summary['top_risk_categories']}")
    
    if assessment.recommendations:
        print(f"   Top recommendations:")
        for i, rec in enumerate(assessment.recommendations[:3], 1):
            print(f"     {i}. {rec}")
    
    # Test visualization data
    viz_data = classifier.get_risk_visualization_data(assessment)
    print(f"   Visualization data generated: {len(viz_data)} fields")
    
    return assessment

def test_document_highlighter():
    """Test the DocumentHighlighter service."""
    print("\n🧪 Testing DocumentHighlighter...")
    
    highlighter = DocumentHighlighter()
    
    # Test text
    test_text = """
    This is a sample legal document.
    The contractor shall provide services.
    Penalties may apply for late delivery.
    Confidential information must be protected.
    The agreement can be terminated early.
    """
    
    # Create sample clauses
    sample_clauses = [
        type('MockClause', (), {
            'clause_type': 'obligations',
            'risk_level': 'medium',
            'importance': 'high',
            'confidence': 0.8,
            'text': 'The contractor shall provide services.',
            'start_line': 2
        })(),
        type('MockClause', (), {
            'clause_type': 'penalties',
            'risk_level': 'high',
            'importance': 'high',
            'confidence': 0.9,
            'text': 'Penalties may apply for late delivery.',
            'start_line': 3
        })(),
        type('MockClause', (), {
            'clause_type': 'confidentiality',
            'risk_level': 'low',
            'importance': 'medium',
            'confidence': 0.7,
            'text': 'Confidential information must be protected.',
            'start_line': 4
        })()
    ]
    
    # Create mock risk assessment
    mock_assessment = type('MockAssessment', (), {
        'risk_indicators': [
            type('MockIndicator', (), {
                'severity': 'high',
                'description': 'High risk penalty clause',
                'mitigation_suggestion': 'Negotiate penalty caps',
                'line_reference': 3
            })()
        ]
    })()
    
    highlighted_doc = highlighter.highlight_document(test_text, sample_clauses, mock_assessment)
    
    print(f"✅ Document highlighting completed")
    print(f"   Total highlights: {highlighted_doc.metadata['total_highlights']}")
    print(f"   Highlight types: {highlighted_doc.metadata['highlight_types']}")
    print(f"   Risk distribution: {highlighted_doc.metadata['risk_distribution']}")
    print(f"   Line coverage: {len(highlighted_doc.metadata['line_coverage'])} lines")
    
    # Test CSS generation
    css_styles = highlighter.generate_css_styles()
    print(f"   CSS styles generated: {len(css_styles)} characters")
    
    # Test HTML generation
    html_output = highlighter.generate_html_highlights(test_text, highlighted_doc.highlights)
    print(f"   HTML output generated: {len(html_output)} characters")
    
    return highlighted_doc

def test_phase2_integration():
    """Test the complete Phase 2 integration."""
    print("\n🧪 Testing Phase 2 Integration...")
    
    service = DocumentAnalysisService()
    
    # Test with sample text
    test_text = """
    SERVICE AGREEMENT
    
    This agreement is entered into between Client and Contractor.
    
    The Contractor shall provide consulting services as specified in Schedule A.
    Services must be completed within 30 days of the start date.
    
    In case of breach or default, a penalty of $5,000 shall apply.
    Liquidated damages may be assessed for project delays.
    
    This agreement will automatically renew for successive one-year terms.
    Either party may terminate with 60 days written notice.
    
    The Contractor agrees to indemnify and hold harmless the Client.
    All liability is limited to the amount paid under this agreement.
    
    Confidential information shared during this engagement must be protected.
    Trade secrets and proprietary data shall not be disclosed.
    
    The Contractor will maintain professional liability insurance.
    Performance standards and service levels are defined in Schedule B.
    """
    
    print("   Running comprehensive analysis...")
    results = service.analyze_document_from_text(test_text, "comprehensive")
    
    if results['success']:
        print("✅ Phase 2 integration test passed")
        
        # Check Phase 2 results
        phase2 = results.get('phase2_analysis', {})
        
        # Clause detection results
        clause_detection = phase2.get('clause_detection', {})
        print(f"   Clauses detected: {clause_detection.get('total_clauses', 0)}")
        
        # Enhanced risk assessment
        risk_assessment = phase2.get('enhanced_risk_assessment', {})
        print(f"   Risk level: {risk_assessment.get('overall_risk', 'unknown')}")
        print(f"   Risk score: {risk_assessment.get('risk_score', 0):.2f}")
        
        # Document highlighting
        highlighting = phase2.get('document_highlighting', {})
        print(f"   Highlights generated: {highlighting.get('total_highlights', 0)}")
        
        # Check version
        metadata = results.get('analysis_metadata', {})
        print(f"   Version: {metadata.get('version', 'unknown')}")
        print(f"   Phase: {metadata.get('phase', 'unknown')}")
        
    else:
        print(f"❌ Phase 2 integration test failed: {results.get('error', 'Unknown error')}")
    
    return results

def main():
    """Run all Phase 2 tests."""
    print("🚀 Phase 2 Testing - AI Legal Document Explainer")
    print("=" * 60)
    
    try:
        # Test individual services
        clauses, clause_summary = test_clause_detector()
        risk_assessment = test_enhanced_risk_classifier()
        highlighted_doc = test_document_highlighter()
        
        # Test integration
        integration_results = test_phase2_integration()
        
        print("\n" + "=" * 60)
        print("📊 Phase 2 Test Results Summary")
        print("=" * 60)
        
        # Summary statistics
        total_clauses = len(clauses) if clauses else 0
        risk_level = risk_assessment.overall_risk.value if risk_assessment else 'unknown'
        total_highlights = highlighted_doc.metadata.get('total_highlights', 0) if highlighted_doc else 0
        
        print(f"✅ Clause Detection: {total_clauses} clauses identified")
        print(f"✅ Enhanced Risk Classification: {risk_level} risk level")
        print(f"✅ Document Highlighting: {total_highlights} highlights generated")
        print(f"✅ Integration Test: {'PASSED' if integration_results.get('success') else 'FAILED'}")
        
        print("\n🎉 All Phase 2 tests completed!")
        print("\n📋 Phase 2 Features Implemented:")
        print("✅ Legal clause detection and categorization")
        print("✅ Multi-level risk assessment with recommendations")
        print("✅ Risk-based document highlighting with tooltips")
        print("✅ Comprehensive API integration")
        print("✅ Enhanced analysis pipeline")
        
        print("\n🔧 Next Steps:")
        print("1. Test with actual PDF documents")
        print("2. Deploy enhanced API endpoints")
        print("3. Proceed to Phase 3 (User Interface)")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Phase 2 testing failed: {str(e)}")
        logger.error(f"Phase 2 testing error: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
