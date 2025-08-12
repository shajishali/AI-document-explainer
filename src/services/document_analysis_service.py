"""
Document Analysis Service for AI Legal Document Explainer

Main service that orchestrates document processing, summarization, and risk classification.
"""

import logging
import time
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
import tempfile
import shutil

from .document_processor import DocumentProcessor
from .summarization_service import SummarizationService
from .basic_risk_classifier import BasicRiskClassifier

logger = logging.getLogger(__name__)

class DocumentAnalysisService:
    """Main service for analyzing legal documents."""
    
    def __init__(self, openai_api_key: str = None):
        self.document_processor = DocumentProcessor()
        self.summarization_service = SummarizationService(openai_api_key)
        self.risk_classifier = BasicRiskClassifier()
        
        # Create temporary directory for file processing
        self.temp_dir = tempfile.mkdtemp(prefix="legal_doc_analyzer_")
        logger.info(f"Document analysis service initialized. Temp directory: {self.temp_dir}")
    
    def __del__(self):
        """Cleanup temporary directory on service destruction."""
        try:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                logger.info("Temporary directory cleaned up")
        except Exception as e:
            logger.error(f"Failed to cleanup temp directory: {str(e)}")
    
    def analyze_document(self, file_path: str, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """
        Complete document analysis pipeline.
        
        Args:
            file_path: Path to the document file
            analysis_type: Type of analysis (basic, comprehensive, risk_focused)
            
        Returns:
            Dict containing complete analysis results
        """
        start_time = time.time()
        
        try:
            logger.info(f"Starting document analysis: {file_path}")
            
            # Step 1: Document Processing
            logger.info("Step 1: Processing document...")
            processing_result = self.document_processor.process_document(file_path)
            if not processing_result['success']:
                return {
                    'success': False,
                    'error': processing_result['error'],
                    'processing_time': time.time() - start_time
                }
            
            # Step 2: Text Analysis and Legal Term Identification
            logger.info("Step 2: Analyzing text and identifying legal terms...")
            full_text = self._combine_chunks(processing_result['chunks'])
            legal_terms_result = self.summarization_service.identify_legal_terms(full_text)
            
            # Step 3: Document Summarization
            logger.info("Step 3: Generating document summary...")
            summary_result = self.summarization_service.summarize_document_chunks(
                processing_result['chunks'], 
                analysis_type
            )
            
            # Step 4: Risk Classification
            logger.info("Step 4: Classifying document risks...")
            risk_classification = self.risk_classifier.classify_document_risks(full_text)
            specific_risks = self.risk_classifier.identify_specific_risks(full_text)
            
            # Step 5: Generate comprehensive results
            logger.info("Step 5: Compiling analysis results...")
            analysis_results = self._compile_analysis_results(
                processing_result,
                legal_terms_result,
                summary_result,
                risk_classification,
                specific_risks,
                start_time
            )
            
            logger.info(f"Document analysis completed successfully in {analysis_results['processing_time']:.2f} seconds")
            return analysis_results
            
        except Exception as e:
            logger.error(f"Document analysis failed: {str(e)}")
            return {
                'success': False,
                'error': f'Analysis failed: {str(e)}',
                'processing_time': time.time() - start_time
            }
    
    def _combine_chunks(self, chunks: List[Dict[str, Any]]) -> str:
        """Combine all document chunks into full text."""
        try:
            # Sort chunks by chunk_id to maintain order
            sorted_chunks = sorted(chunks, key=lambda x: x.get('chunk_id', 0))
            return " ".join([chunk.get('text', '') for chunk in sorted_chunks])
        except Exception as e:
            logger.error(f"Chunk combination error: {str(e)}")
            return ""
    
    def _compile_analysis_results(self, processing_result: Dict[str, Any], 
                                legal_terms_result: Dict[str, Any],
                                summary_result: Dict[str, Any],
                                risk_classification: Dict[str, Any],
                                specific_risks: Dict[str, Any],
                                start_time: float) -> Dict[str, Any]:
        """Compile all analysis results into a comprehensive response."""
        try:
            processing_time = time.time() - start_time
            
            # Calculate confidence scores
            summary_confidence = self.summarization_service.calculate_confidence_score(summary_result)
            risk_confidence = 0.8 if risk_classification['success'] else 0.0
            
            # Generate risk summary and recommendations
            risk_summary = self.risk_classifier.generate_risk_summary(
                risk_classification, specific_risks
            )
            risk_recommendations = self.risk_classifier.get_risk_recommendations(
                risk_classification
            )
            
            # Compile results
            results = {
                'success': True,
                'processing_time': processing_time,
                'document_info': processing_result['document_info'],
                'processing_info': processing_result['processing_info'],
                
                # Legal Terms Analysis
                'legal_terms': {
                    'success': legal_terms_result['success'],
                    'total_terms': legal_terms_result.get('total_terms', 0),
                    'categories': legal_terms_result.get('categories', {}),
                    'confidence_score': 0.9 if legal_terms_result['success'] else 0.0
                },
                
                # Document Summary
                'summary': {
                    'success': summary_result['success'],
                    'comprehensive_summary': summary_result.get('comprehensive_summary', ''),
                    'summary_type': summary_result.get('summary_type', ''),
                    'total_chunks_processed': summary_result.get('total_chunks_processed', 0),
                    'confidence_score': summary_confidence
                },
                
                # Risk Analysis
                'risk_analysis': {
                    'success': risk_classification['success'],
                    'overall_risk_level': risk_classification.get('overall_risk_level', 'unknown'),
                    'overall_risk_score': risk_classification.get('overall_risk_score', 0),
                    'risk_breakdown': risk_classification.get('risk_breakdown', {}),
                    'specific_risks': specific_risks.get('specific_risks', {}),
                    'risk_summary': risk_summary,
                    'recommendations': risk_recommendations,
                    'confidence_score': risk_confidence
                },
                
                # Analysis Metadata
                'analysis_metadata': {
                    'analysis_type': 'comprehensive',
                    'services_used': [
                        'DocumentProcessor',
                        'SummarizationService', 
                        'BasicRiskClassifier'
                    ],
                    'timestamp': time.time(),
                    'version': '1.0.0'
                }
            }
            
            return results
            
        except Exception as e:
            logger.error(f"Results compilation error: {str(e)}")
            return {
                'success': False,
                'error': f'Results compilation failed: {str(e)}',
                'processing_time': time.time() - start_time
            }
    
    def analyze_document_from_text(self, text: str, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """
        Analyze document from provided text (for testing or direct text input).
        
        Args:
            text: Document text content
            analysis_type: Type of analysis
            
        Returns:
            Dict containing analysis results
        """
        start_time = time.time()
        
        try:
            logger.info("Starting text-based document analysis")
            
            # Step 1: Legal Term Identification
            legal_terms_result = self.summarization_service.identify_legal_terms(text)
            
            # Step 2: Text Summarization
            summary_result = self.summarization_service.summarize_text(text, analysis_type)
            
            # Step 3: Risk Classification
            risk_classification = self.risk_classifier.classify_document_risks(text)
            specific_risks = self.risk_classifier.identify_specific_risks(text)
            
            # Step 4: Compile results
            results = {
                'success': True,
                'processing_time': time.time() - start_time,
                'input_type': 'text',
                'text_length': len(text),
                
                'legal_terms': {
                    'success': legal_terms_result['success'],
                    'total_terms': legal_terms_result.get('total_terms', 0),
                    'categories': legal_terms_result.get('categories', {}),
                    'confidence_score': 0.9 if legal_terms_result['success'] else 0.0
                },
                
                'summary': {
                    'success': summary_result['success'],
                    'summary': summary_result.get('summary', ''),
                    'summary_type': summary_result.get('summary_type', ''),
                    'confidence_score': self.summarization_service.calculate_confidence_score(summary_result)
                },
                
                'risk_analysis': {
                    'success': risk_classification['success'],
                    'overall_risk_level': risk_classification.get('overall_risk_level', 'unknown'),
                    'overall_risk_score': risk_classification.get('overall_risk_score', 0),
                    'risk_breakdown': risk_classification.get('risk_breakdown', {}),
                    'specific_risks': specific_risks.get('specific_risks', {}),
                    'risk_summary': self.risk_classifier.generate_risk_summary(
                        risk_classification, specific_risks
                    ),
                    'recommendations': self.risk_classifier.get_risk_recommendations(
                        risk_classification
                    ),
                    'confidence_score': 0.8 if risk_classification['success'] else 0.0
                },
                
                'analysis_metadata': {
                    'analysis_type': analysis_type,
                    'services_used': ['SummarizationService', 'BasicRiskClassifier'],
                    'timestamp': time.time(),
                    'version': '1.0.0'
                }
            }
            
            return results
            
        except Exception as e:
            logger.error(f"Text-based analysis failed: {str(e)}")
            return {
                'success': False,
                'error': f'Text analysis failed: {str(e)}',
                'processing_time': time.time() - start_time
            }
    
    def get_analysis_status(self) -> Dict[str, Any]:
        """Get the current status of the analysis service."""
        return {
            'service_status': 'operational',
            'services_available': {
                'document_processor': True,
                'summarization_service': self.summarization_service.llm is not None,
                'risk_classifier': True
            },
            'temp_directory': self.temp_dir,
            'supported_formats': self.document_processor.supported_formats,
            'max_file_size': self.document_processor.max_file_size
        }
