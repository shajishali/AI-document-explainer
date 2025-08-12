"""
Summarization Service for AI Legal Document Explainer

Provides AI-powered document summarization using LangChain and legal term identification.
"""

import logging
from typing import List, Dict, Any, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain_openai import ChatOpenAI
from langchain.schema import Document
import re
import time

logger = logging.getLogger(__name__)

class SummarizationService:
    """Handles AI-powered document summarization and legal term identification."""
    
    def __init__(self, openai_api_key: str = None):
        self.openai_api_key = openai_api_key
        self.llm = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Legal terms patterns for identification
        self.legal_terms_patterns = {
            'contract_terms': [
                r'\b(agreement|contract|terms|conditions|clause|section|article)\b',
                r'\b(party|parties|obligation|liability|indemnification|warranty)\b',
                r'\b(termination|renewal|amendment|modification|assignment)\b'
            ],
            'financial_terms': [
                r'\b(payment|fee|cost|expense|penalty|fine|damages|compensation)\b',
                r'\b(interest|rate|percentage|amount|total|balance|due|overdue)\b'
            ],
            'legal_actions': [
                r'\b(breach|violation|default|enforcement|litigation|arbitration)\b',
                r'\b(notice|demand|cease|desist|injunction|specific performance)\b'
            ],
            'time_terms': [
                r'\b(effective date|commencement|duration|period|deadline|timeline)\b',
                r'\b(notice period|grace period|extension|renewal|expiration)\b'
            ]
        }
        
        if openai_api_key:
            self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize the language model for summarization."""
        try:
            self.llm = ChatOpenAI(
                api_key=self.openai_api_key,
                model="gpt-4o-mini",  # Using GPT-4o-mini for cost efficiency
                temperature=0.3,
                max_tokens=1000
            )
            logger.info("Language model initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize language model: {str(e)}")
            self.llm = None
    
    def identify_legal_terms(self, text: str) -> Dict[str, Any]:
        """
        Identify legal terms and concepts in the text.
        
        Args:
            text: Text content to analyze
            
        Returns:
            Dict containing identified legal terms by category
        """
        try:
            identified_terms = {}
            text_lower = text.lower()
            
            for category, patterns in self.legal_terms_patterns.items():
                category_terms = set()
                for pattern in patterns:
                    matches = re.findall(pattern, text_lower, re.IGNORECASE)
                    category_terms.update(matches)
                
                if category_terms:
                    identified_terms[category] = list(category_terms)
            
            return {
                'success': True,
                'total_terms': sum(len(terms) for terms in identified_terms.values()),
                'categories': identified_terms
            }
            
        except Exception as e:
            logger.error(f"Legal term identification error: {str(e)}")
            return {
                'success': False,
                'error': f'Term identification failed: {str(e)}'
            }
    
    def create_summary_prompt(self, text: str, summary_type: str = "general") -> str:
        """
        Create appropriate prompt for different types of summaries.
        
        Args:
            text: Text to summarize
            summary_type: Type of summary (general, legal_focused, risk_assessment)
            
        Returns:
            Formatted prompt for the LLM
        """
        base_prompt = f"""
        Please analyze the following legal document text and provide a clear, concise summary.
        
        Document Text:
        {text[:2000]}...
        
        Requirements:
        - Use plain, easy-to-understand language
        - Avoid legal jargon when possible
        - Highlight key points and important information
        - Focus on what the reader needs to know
        """
        
        if summary_type == "legal_focused":
            base_prompt += """
            - Emphasize legal obligations and rights
            - Identify key legal terms and concepts
            - Note any deadlines or important dates
            """
        elif summary_type == "risk_assessment":
            base_prompt += """
            - Identify potential risks and concerns
            - Highlight unusual or one-sided terms
            - Note any penalties or consequences
            """
        
        base_prompt += """
        
        Please provide a structured summary with:
        1. Main purpose of the document
        2. Key obligations and rights
        3. Important deadlines or dates
        4. Any notable terms or conditions
        """
        
        return base_prompt
    
    def summarize_text(self, text: str, summary_type: str = "general") -> Dict[str, Any]:
        """
        Generate AI-powered summary of the text.
        
        Args:
            text: Text content to summarize
            summary_type: Type of summary to generate
            
        Returns:
            Dict containing summary and metadata
        """
        try:
            if not self.llm:
                return {
                    'success': False,
                    'error': 'Language model not initialized. Please provide OpenAI API key.'
                }
            
            # Create summary prompt
            prompt = self.create_summary_prompt(text, summary_type)
            
            # Generate summary
            start_time = time.time()
            response = self.llm.invoke(prompt)
            processing_time = time.time() - start_time
            
            summary = response.content if hasattr(response, 'content') else str(response)
            
            return {
                'success': True,
                'summary': summary,
                'summary_type': summary_type,
                'processing_time': processing_time,
                'text_length': len(text),
                'summary_length': len(summary)
            }
            
        except Exception as e:
            logger.error(f"Text summarization error: {str(e)}")
            return {
                'success': False,
                'error': f'Summarization failed: {str(e)}'
            }
    
    def summarize_document_chunks(self, chunks: List[Dict[str, Any]], summary_type: str = "general") -> Dict[str, Any]:
        """
        Summarize document by processing chunks and creating a comprehensive summary.
        
        Args:
            chunks: List of document chunks from DocumentProcessor
            summary_type: Type of summary to generate
            
        Returns:
            Dict containing comprehensive summary and metadata
        """
        try:
            if not chunks:
                return {
                    'success': False,
                    'error': 'No chunks provided for summarization'
                }
            
            # Process each chunk
            chunk_summaries = []
            total_processing_time = 0
            
            for chunk in chunks:
                chunk_text = chunk.get('text', '')
                if chunk_text.strip():
                    chunk_result = self.summarize_text(chunk_text, summary_type)
                    if chunk_result['success']:
                        chunk_summaries.append({
                            'chunk_id': chunk.get('chunk_id'),
                            'page_number': chunk.get('page_number'),
                            'summary': chunk_result['summary'],
                            'processing_time': chunk_result['processing_time']
                        })
                        total_processing_time += chunk_result['processing_time']
            
            if not chunk_summaries:
                return {
                    'success': False,
                    'error': 'Failed to generate summaries for any chunks'
                }
            
            # Create comprehensive summary from chunk summaries
            comprehensive_summary = self._create_comprehensive_summary(chunk_summaries, summary_type)
            
            return {
                'success': True,
                'comprehensive_summary': comprehensive_summary,
                'chunk_summaries': chunk_summaries,
                'total_chunks_processed': len(chunk_summaries),
                'total_processing_time': total_processing_time,
                'summary_type': summary_type
            }
            
        except Exception as e:
            logger.error(f"Document chunk summarization error: {str(e)}")
            return {
                'success': False,
                'error': f'Chunk summarization failed: {str(e)}'
            }
    
    def _create_comprehensive_summary(self, chunk_summaries: List[Dict[str, Any]], summary_type: str) -> str:
        """Create a comprehensive summary from individual chunk summaries."""
        try:
            # Combine all chunk summaries
            combined_text = "\n\n".join([cs['summary'] for cs in chunk_summaries])
            
            # Create a meta-summary prompt
            meta_prompt = f"""
            I have analyzed a legal document and created summaries for different sections. 
            Please create a comprehensive, coherent summary that combines all this information.
            
            Section Summaries:
            {combined_text[:3000]}...
            
            Please provide:
            1. A clear overview of the entire document
            2. Key points from all sections
            3. Important obligations, rights, and deadlines
            4. Any notable risks or concerns
            5. A conclusion with main takeaways
            
            Make it easy to understand for someone without legal expertise.
            """
            
            if self.llm:
                response = self.llm.invoke(meta_prompt)
                return response.content if hasattr(response, 'content') else str(response)
            else:
                # Fallback: combine summaries manually
                return self._manual_summary_combination(chunk_summaries)
                
        except Exception as e:
            logger.error(f"Comprehensive summary creation error: {str(e)}")
            return self._manual_summary_combination(chunk_summaries)
    
    def _manual_summary_combination(self, chunk_summaries: List[Dict[str, Any]]) -> str:
        """Manually combine chunk summaries when LLM is not available."""
        try:
            combined_summary = "Document Summary:\n\n"
            
            for cs in chunk_summaries:
                combined_summary += f"Section {cs['chunk_id']} (Page {cs['page_number']}):\n"
                combined_summary += f"{cs['summary']}\n\n"
            
            return combined_summary
            
        except Exception as e:
            logger.error(f"Manual summary combination error: {str(e)}")
            return "Summary generation failed. Please try again."
    
    def calculate_confidence_score(self, summary_result: Dict[str, Any]) -> float:
        """
        Calculate confidence score for the summary.
        
        Args:
            summary_result: Result from summarization methods
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        try:
            if not summary_result['success']:
                return 0.0
            
            # Base confidence factors
            confidence_factors = {
                'text_length': min(summary_result.get('text_length', 0) / 1000, 1.0),  # Normalize to 0-1
                'processing_success': 1.0 if summary_result['success'] else 0.0,
                'summary_quality': min(summary_result.get('summary_length', 0) / 500, 1.0)  # Reasonable summary length
            }
            
            # Calculate weighted average
            weights = [0.3, 0.4, 0.3]  # Adjust weights as needed
            confidence_score = sum(
                factor * weight 
                for factor, weight in zip(confidence_factors.values(), weights)
            )
            
            return min(max(confidence_score, 0.0), 1.0)  # Ensure 0.0 <= score <= 1.0
            
        except Exception as e:
            logger.error(f"Confidence score calculation error: {str(e)}")
            return 0.5  # Default confidence score
