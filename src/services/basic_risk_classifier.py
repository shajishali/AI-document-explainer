"""
Basic Risk Classifier Service for AI Legal Document Explainer

Provides simple risk identification and classification for legal documents.
"""

import logging
import re
from typing import List, Dict, Any, Optional
from enum import Enum

logger = logging.getLogger(__name__)

class RiskLevel(Enum):
    """Risk level enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class BasicRiskClassifier:
    """Basic risk classification for legal documents."""
    
    def __init__(self):
        # Risk patterns for different categories
        self.risk_patterns = {
            'high_risk': {
                'penalties': [
                    r'\b(penalty|fine|damages|liquidated damages|punitive)\b',
                    r'\b(breach|violation|default|non-compliance)\b',
                    r'\b(termination|cancellation|void|unenforceable)\b'
                ],
                'auto_renewals': [
                    r'\b(auto.?renew|automatic renewal|evergreen|perpetual)\b',
                    r'\b(continues until|renewal without notice)\b'
                ],
                'one_sided_terms': [
                    r'\b(sole discretion|unilateral|one.?way|non-negotiable)\b',
                    r'\b(waiver|release|indemnification|hold harmless)\b',
                    r'\b(no recourse|no liability|disclaimer|exclusion)\b'
                ],
                'financial_risks': [
                    r'\b(interest rate|penalty rate|late fees|overdue charges)\b',
                    r'\b(security deposit|escrow|collateral|guarantee)\b'
                ]
            },
            'medium_risk': {
                'standard_obligations': [
                    r'\b(obligation|duty|responsibility|requirement)\b',
                    r'\b(comply|adhere|follow|maintain)\b'
                ],
                'moderate_terms': [
                    r'\b(reasonable|standard|customary|industry practice)\b',
                    r'\b(notice period|grace period|cure period)\b'
                ],
                'financial_terms': [
                    r'\b(payment|fee|cost|expense|charge)\b',
                    r'\b(due date|payment terms|billing)\b'
                ]
            },
            'low_risk': {
                'protections': [
                    r'\b(protection|safeguard|security|guarantee)\b',
                    r'\b(right|entitlement|benefit|advantage)\b'
                ],
                'fair_terms': [
                    r'\b(mutual|both parties|agreed|negotiated)\b',
                    r'\b(reasonable|fair|equitable|balanced)\b'
                ],
                'standard_clauses': [
                    r'\b(governing law|jurisdiction|dispute resolution)\b',
                    r'\b(entire agreement|amendment|modification)\b'
                ]
            }
        }
        
        # Risk scoring weights
        self.risk_weights = {
            'high_risk': 3.0,
            'medium_risk': 2.0,
            'low_risk': 1.0
        }
    
    def classify_document_risks(self, text: str) -> Dict[str, Any]:
        """
        Classify risks in the document text.
        
        Args:
            text: Document text to analyze
            
        Returns:
            Dict containing risk classification results
        """
        try:
            text_lower = text.lower()
            risk_results = {}
            total_risk_score = 0
            
            for risk_level, categories in self.risk_patterns.items():
                level_results = {}
                level_score = 0
                
                for category, patterns in categories.items():
                    category_matches = []
                    category_score = 0
                    
                    for pattern in patterns:
                        matches = re.findall(pattern, text_lower, re.IGNORECASE)
                        if matches:
                            category_matches.extend(matches)
                            category_score += len(matches)
                    
                    if category_matches:
                        level_results[category] = {
                            'matches': list(set(category_matches)),  # Remove duplicates
                            'count': len(set(category_matches)),
                            'score': category_score
                        }
                        level_score += category_score
                
                if level_results:
                    risk_results[risk_level] = {
                        'categories': level_results,
                        'total_score': level_score,
                        'weighted_score': level_score * self.risk_weights[risk_level]
                    }
                    total_risk_score += level_score * self.risk_weights[risk_level]
            
            # Determine overall risk level
            overall_risk = self._determine_overall_risk(total_risk_score)
            
            return {
                'success': True,
                'overall_risk_level': overall_risk.value,
                'overall_risk_score': total_risk_score,
                'risk_breakdown': risk_results,
                'total_risk_indicators': sum(
                    sum(cat['count'] for cat in level['categories'].values())
                    for level in risk_results.values()
                )
            }
            
        except Exception as e:
            logger.error(f"Risk classification error: {str(e)}")
            return {
                'success': False,
                'error': f'Risk classification failed: {str(e)}'
            }
    
    def _determine_overall_risk(self, total_score: float) -> RiskLevel:
        """Determine overall risk level based on total score."""
        if total_score >= 15:
            return RiskLevel.HIGH
        elif total_score >= 8:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def identify_specific_risks(self, text: str) -> Dict[str, Any]:
        """
        Identify specific risk factors in the text.
        
        Args:
            text: Document text to analyze
            
        Returns:
            Dict containing specific risk factors
        """
        try:
            specific_risks = {
                'high_priority': [],
                'medium_priority': [],
                'low_priority': []
            }
            
            # High priority risk indicators
            high_priority_patterns = [
                (r'\b(penalty|fine)\s+of\s+\$?[\d,]+', 'Financial penalty amount'),
                (r'\b(breach|violation)\s+results\s+in', 'Breach consequences'),
                (r'\b(auto.?renew|automatic renewal)', 'Automatic renewal clause'),
                (r'\b(sole discretion|unilateral)', 'One-sided decision making'),
                (r'\b(waiver|release)\s+of\s+all\s+rights', 'Broad rights waiver')
            ]
            
            # Medium priority risk indicators
            medium_priority_patterns = [
                (r'\b(obligation|duty)\s+to\s+pay', 'Payment obligation'),
                (r'\b(termination|cancellation)\s+clause', 'Termination terms'),
                (r'\b(notice|notification)\s+period', 'Notice requirements'),
                (r'\b(interest|rate)\s+of\s+[\d.]+%', 'Interest rate specification')
            ]
            
            # Low priority risk indicators
            low_priority_patterns = [
                (r'\b(governing law|jurisdiction)', 'Legal jurisdiction'),
                (r'\b(entire agreement|integration)', 'Agreement scope'),
                (r'\b(amendment|modification)', 'Modification terms')
            ]
            
            # Process each priority level
            for priority, patterns in [
                ('high_priority', high_priority_patterns),
                ('medium_priority', medium_priority_patterns),
                ('low_priority', low_priority_patterns)
            ]:
                for pattern, description in patterns:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    for match in matches:
                        specific_risks[priority].append({
                            'text': match,
                            'description': description,
                            'context': self._get_context(text, match, 100)
                        })
            
            return {
                'success': True,
                'specific_risks': specific_risks,
                'total_high_priority': len(specific_risks['high_priority']),
                'total_medium_priority': len(specific_risks['medium_priority']),
                'total_low_priority': len(specific_risks['low_priority'])
            }
            
        except Exception as e:
            logger.error(f"Specific risk identification error: {str(e)}")
            return {
                'success': False,
                'error': f'Specific risk identification failed: {str(e)}'
            }
    
    def _get_context(self, text: str, match: str, context_length: int) -> str:
        """Get context around a matched text."""
        try:
            match_start = text.lower().find(match.lower())
            if match_start == -1:
                return match
            
            start = max(0, match_start - context_length // 2)
            end = min(len(text), match_start + len(match) + context_length // 2)
            
            context = text[start:end]
            if start > 0:
                context = "..." + context
            if end < len(text):
                context = context + "..."
            
            return context
            
        except Exception as e:
            logger.error(f"Context extraction error: {str(e)}")
            return match
    
    def generate_risk_summary(self, classification_result: Dict[str, Any], specific_risks: Dict[str, Any]) -> str:
        """
        Generate a human-readable risk summary.
        
        Args:
            classification_result: Result from classify_document_risks
            specific_risks: Result from identify_specific_risks
            
        Returns:
            Formatted risk summary string
        """
        try:
            if not classification_result['success'] or not specific_risks['success']:
                return "Risk analysis could not be completed."
            
            summary = f"Document Risk Assessment\n"
            summary += f"{'='*50}\n\n"
            
            # Overall risk level
            overall_risk = classification_result['overall_risk_level'].upper()
            summary += f"Overall Risk Level: {overall_risk}\n"
            summary += f"Risk Score: {classification_result['overall_risk_score']:.1f}\n\n"
            
            # Risk breakdown
            summary += "Risk Breakdown:\n"
            for risk_level, data in classification_result['risk_breakdown'].items():
                summary += f"- {risk_level.replace('_', ' ').title()}: {data['total_score']} indicators\n"
            
            summary += "\n"
            
            # Specific risks by priority
            for priority in ['high_priority', 'medium_priority', 'low_priority']:
                priority_title = priority.replace('_', ' ').title()
                risks = specific_risks['specific_risks'][priority]
                
                if risks:
                    summary += f"{priority_title} Risks:\n"
                    for i, risk in enumerate(risks[:5], 1):  # Show top 5
                        summary += f"  {i}. {risk['description']}: {risk['text']}\n"
                    summary += "\n"
            
            return summary
            
        except Exception as e:
            logger.error(f"Risk summary generation error: {str(e)}")
            return "Risk summary generation failed."
    
    def get_risk_recommendations(self, classification_result: Dict[str, Any]) -> List[str]:
        """
        Get risk-based recommendations.
        
        Args:
            classification_result: Result from classify_document_risks
            
        Returns:
            List of recommendations
        """
        try:
            recommendations = []
            overall_risk = classification_result['overall_risk_level']
            
            if overall_risk == 'high':
                recommendations.extend([
                    "⚠️ This document contains several high-risk elements that require careful review.",
                    "🔍 Pay special attention to penalty clauses and automatic renewal terms.",
                    "⚖️ Consider consulting with a legal professional before signing.",
                    "📋 Review all financial obligations and potential consequences carefully."
                ])
            elif overall_risk == 'medium':
                recommendations.extend([
                    "📝 This document has moderate risk factors that should be reviewed.",
                    "💰 Pay attention to payment terms and financial obligations.",
                    "⏰ Note any deadlines or notice periods that may affect you.",
                    "✅ Overall terms appear reasonable but require careful reading."
                ])
            else:  # low risk
                recommendations.extend([
                    "✅ This document appears to have standard, low-risk terms.",
                    "📖 Still review all terms to ensure you understand your obligations.",
                    "📅 Note any important dates or deadlines.",
                    "💡 Document appears to be fair and balanced."
                ])
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Recommendation generation error: {str(e)}")
            return ["Unable to generate recommendations at this time."]
