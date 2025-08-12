import logging
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class RiskLevel(Enum):
    """Risk level enumeration."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    MINIMAL = "minimal"

@dataclass
class RiskIndicator:
    """Represents a specific risk indicator found in the document."""
    category: str
    description: str
    severity: str
    score: float
    evidence: str
    line_reference: int
    mitigation_suggestion: str

@dataclass
class RiskAssessment:
    """Comprehensive risk assessment result."""
    overall_risk: RiskLevel
    risk_score: float
    risk_category: str
    risk_indicators: List[RiskIndicator]
    summary: Dict[str, Any]
    recommendations: List[str]

class EnhancedRiskClassifier:
    """Enhanced risk classification system with multi-level assessment."""
    
    def __init__(self):
        # Risk categories and their weightings
        self.risk_categories = {
            'financial': {
                'weight': 0.25,
                'indicators': {
                    'penalties': {'base_score': 8.0, 'severity': 'high'},
                    'liquidated_damages': {'base_score': 9.0, 'severity': 'high'},
                    'payment_terms': {'base_score': 5.0, 'severity': 'medium'},
                    'cost_escalation': {'base_score': 6.0, 'severity': 'medium'},
                    'auto_renewal': {'base_score': 7.0, 'severity': 'high'}
                }
            },
            'operational': {
                'weight': 0.20,
                'indicators': {
                    'performance_standards': {'base_score': 6.0, 'severity': 'medium'},
                    'service_levels': {'base_score': 5.0, 'severity': 'medium'},
                    'compliance_requirements': {'base_score': 7.0, 'severity': 'high'},
                    'reporting_obligations': {'base_score': 4.0, 'severity': 'low'}
                }
            },
            'legal': {
                'weight': 0.30,
                'indicators': {
                    'liability_limits': {'base_score': 8.0, 'severity': 'high'},
                    'indemnification': {'base_score': 9.0, 'severity': 'high'},
                    'jurisdiction': {'base_score': 6.0, 'severity': 'medium'},
                    'dispute_resolution': {'base_score': 7.0, 'severity': 'medium'},
                    'termination_rights': {'base_score': 8.0, 'severity': 'high'}
                }
            },
            'commercial': {
                'weight': 0.15,
                'indicators': {
                    'exclusivity': {'base_score': 6.0, 'severity': 'medium'},
                    'non_compete': {'base_score': 7.0, 'severity': 'medium'},
                    'intellectual_property': {'base_score': 8.0, 'severity': 'high'},
                    'confidentiality': {'base_score': 5.0, 'severity': 'low'}
                }
            },
            'regulatory': {
                'weight': 0.10,
                'indicators': {
                    'data_protection': {'base_score': 8.0, 'severity': 'high'},
                    'industry_regulations': {'base_score': 7.0, 'severity': 'medium'},
                    'export_controls': {'base_score': 9.0, 'severity': 'high'},
                    'compliance_certification': {'base_score': 6.0, 'severity': 'medium'}
                }
            }
        }
        
        # Risk level thresholds
        self.risk_thresholds = {
            RiskLevel.CRITICAL: 8.5,
            RiskLevel.HIGH: 7.0,
            RiskLevel.MEDIUM: 5.0,
            RiskLevel.LOW: 3.0,
            RiskLevel.MINIMAL: 0.0
        }
        
        # Mitigation suggestions
        self.mitigation_suggestions = {
            'financial': {
                'penalties': 'Negotiate penalty caps and grace periods',
                'liquidated_damages': 'Limit damages to actual losses',
                'auto_renewal': 'Add explicit renewal notification requirements'
            },
            'legal': {
                'liability_limits': 'Cap liability at reasonable amounts',
                'indemnification': 'Limit indemnification scope and duration',
                'termination_rights': 'Ensure mutual termination rights'
            },
            'operational': {
                'performance_standards': 'Define clear, achievable performance metrics',
                'compliance_requirements': 'Specify compliance responsibilities and costs'
            }
        }
    
    def classify_risk(self, clauses: List[Any], document_text: str = "") -> RiskAssessment:
        """
        Perform comprehensive risk classification.
        
        Args:
            clauses: List of detected legal clauses
            document_text: Full document text for context
            
        Returns:
            RiskAssessment object with detailed risk analysis
        """
        risk_indicators = []
        category_scores = {}
        
        # Analyze each clause for risk indicators
        for clause in clauses:
            indicators = self._analyze_clause_risk(clause)
            risk_indicators.extend(indicators)
        
        # Calculate category scores
        for category, config in self.risk_categories.items():
            category_score = self._calculate_category_score(category, risk_indicators)
            category_scores[category] = category_score
        
        # Calculate overall risk score
        overall_score = self._calculate_overall_score(category_scores)
        
        # Determine risk level
        risk_level = self._determine_risk_level(overall_score)
        
        # Generate summary and recommendations
        summary = self._generate_risk_summary(category_scores, risk_indicators)
        recommendations = self._generate_recommendations(risk_indicators)
        
        return RiskAssessment(
            overall_risk=risk_level,
            risk_score=overall_score,
            risk_category=self._categorize_risk(risk_level),
            risk_indicators=risk_indicators,
            summary=summary,
            recommendations=recommendations
        )
    
    def _analyze_clause_risk(self, clause: Any) -> List[RiskIndicator]:
        """Analyze a single clause for risk indicators."""
        indicators = []
        
        # Map clause type to risk categories
        clause_risk_mapping = {
            'penalties': ('financial', 'penalties'),
            'liability': ('legal', 'liability_limits'),
            'renewals': ('financial', 'auto_renewal'),
            'termination': ('legal', 'termination_rights'),
            'confidentiality': ('commercial', 'confidentiality')
        }
        
        clause_type = getattr(clause, 'clause_type', 'unknown')
        if clause_type in clause_risk_mapping:
            category, indicator_type = clause_risk_mapping[clause_type]
            
            # Get base score and severity
            base_config = self.risk_categories[category]['indicators'].get(
                indicator_type, {'base_score': 5.0, 'severity': 'medium'}
            )
            
            # Adjust score based on clause importance and confidence
            adjusted_score = self._adjust_risk_score(
                base_config['base_score'],
                getattr(clause, 'importance', 'medium'),
                getattr(clause, 'confidence', 0.5)
            )
            
            # Get mitigation suggestion
            mitigation = self.mitigation_suggestions.get(category, {}).get(
                indicator_type, 'Review and negotiate terms'
            )
            
            indicator = RiskIndicator(
                category=category,
                description=f"{clause_type.title()} clause detected",
                severity=base_config['severity'],
                score=adjusted_score,
                evidence=getattr(clause, 'text', '')[:100] + '...',
                line_reference=getattr(clause, 'start_line', 0),
                mitigation_suggestion=mitigation
            )
            indicators.append(indicator)
        
        return indicators
    
    def _adjust_risk_score(self, base_score: float, importance: str, confidence: float) -> float:
        """Adjust risk score based on importance and confidence."""
        # Importance multiplier
        importance_multipliers = {
            'high': 1.2,
            'medium': 1.0,
            'low': 0.8
        }
        
        # Confidence multiplier
        confidence_multiplier = 0.5 + (confidence * 0.5)  # 0.5 to 1.0
        
        adjusted_score = base_score * importance_multipliers.get(importance, 1.0) * confidence_multiplier
        
        return min(adjusted_score, 10.0)  # Cap at 10.0
    
    def _calculate_category_score(self, category: str, indicators: List[RiskIndicator]) -> float:
        """Calculate risk score for a specific category."""
        category_indicators = [i for i in indicators if i.category == category]
        
        if not category_indicators:
            return 0.0
        
        # Weighted average of indicator scores
        total_weighted_score = sum(i.score for i in category_indicators)
        return total_weighted_score / len(category_indicators)
    
    def _calculate_overall_score(self, category_scores: Dict[str, float]) -> float:
        """Calculate overall weighted risk score."""
        overall_score = 0.0
        
        for category, score in category_scores.items():
            weight = self.risk_categories[category]['weight']
            overall_score += score * weight
        
        return overall_score
    
    def _determine_risk_level(self, score: float) -> RiskLevel:
        """Determine risk level based on score."""
        for level, threshold in sorted(self.risk_thresholds.items(), key=lambda x: x[1], reverse=True):
            if score >= threshold:
                return level
        return RiskLevel.MINIMAL
    
    def _categorize_risk(self, risk_level: RiskLevel) -> str:
        """Categorize risk level into descriptive text."""
        risk_categories = {
            RiskLevel.CRITICAL: "Critical - Immediate attention required",
            RiskLevel.HIGH: "High - Significant risks present",
            RiskLevel.MEDIUM: "Medium - Moderate risks to consider",
            RiskLevel.LOW: "Low - Minimal risks identified",
            RiskLevel.MINIMAL: "Minimal - Very low risk document"
        }
        return risk_categories.get(risk_level, "Unknown risk level")
    
    def _generate_risk_summary(self, category_scores: Dict[str, float], 
                              indicators: List[RiskIndicator]) -> Dict[str, Any]:
        """Generate comprehensive risk summary."""
        return {
            'category_scores': category_scores,
            'total_indicators': len(indicators),
            'high_severity_count': len([i for i in indicators if i.severity == 'high']),
            'medium_severity_count': len([i for i in indicators if i.severity == 'medium']),
            'low_severity_count': len([i for i in indicators if i.severity == 'low']),
            'top_risk_categories': sorted(
                category_scores.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:3]
        }
    
    def _generate_recommendations(self, indicators: List[RiskIndicator]) -> List[str]:
        """Generate actionable recommendations based on risk indicators."""
        recommendations = []
        
        # Group recommendations by category
        category_recommendations = {}
        for indicator in indicators:
            if indicator.category not in category_recommendations:
                category_recommendations[indicator.category] = []
            category_recommendations[indicator.category].append(indicator.mitigation_suggestion)
        
        # Generate category-specific recommendations
        for category, suggestions in category_recommendations.items():
            unique_suggestions = list(set(suggestions))
            recommendations.extend(unique_suggestions)
        
        # Add general recommendations
        if len(indicators) > 5:
            recommendations.append("Consider legal review due to high number of risk indicators")
        
        high_risk_count = len([i for i in indicators if i.severity == 'high'])
        if high_risk_count > 2:
            recommendations.append("Multiple high-risk clauses detected - seek legal counsel")
        
        return recommendations[:10]  # Limit to top 10 recommendations
    
    def get_risk_visualization_data(self, assessment: RiskAssessment) -> Dict[str, Any]:
        """Generate data for risk visualization charts."""
        return {
            'risk_level': assessment.overall_risk.value,
            'risk_score': assessment.risk_score,
            'category_scores': assessment.summary['category_scores'],
            'severity_distribution': {
                'high': assessment.summary['high_severity_count'],
                'medium': assessment.summary['medium_severity_count'],
                'low': assessment.summary['low_severity_count']
            },
            'top_risks': assessment.summary['top_risk_categories'],
            'indicator_count': assessment.summary['total_indicators']
        }
