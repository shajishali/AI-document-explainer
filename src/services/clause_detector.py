import re
import logging
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class LegalClause:
    """Represents a detected legal clause with metadata."""
    text: str
    clause_type: str
    start_line: int
    end_line: int
    importance: str
    risk_level: str
    confidence: float

class ClauseDetector:
    """Service for detecting and categorizing legal clauses in documents."""
    
    def __init__(self):
        # Legal clause patterns and keywords
        self.clause_patterns = {
            'obligations': {
                'keywords': ['shall', 'must', 'will', 'agree to', 'obligated to', 'required to'],
                'patterns': [
                    r'(?:shall|must|will)\s+(?:be\s+)?(?:required|obligated|bound)\s+to',
                    r'(?:agree\s+to|consent\s+to|undertake\s+to)',
                    r'(?:duty|obligation|responsibility)\s+to'
                ]
            },
            'penalties': {
                'keywords': ['penalty', 'fine', 'damages', 'breach', 'default', 'termination'],
                'patterns': [
                    r'(?:penalty|fine|damage|breach|default)\s+(?:of|for|in\s+the\s+amount\s+of)',
                    r'(?:termination|cancellation|suspension)\s+(?:for|due\s+to)',
                    r'(?:liquidated\s+damages|consequential\s+damages)'
                ]
            },
            'renewals': {
                'keywords': ['renewal', 'extension', 'automatic', 'rollover', 'continue'],
                'patterns': [
                    r'(?:automatic|automatic\s+renewal|rollover)',
                    r'(?:renewal|extension)\s+(?:of|for)',
                    r'(?:continue|continue\s+in\s+effect)'
                ]
            },
            'termination': {
                'keywords': ['terminate', 'cancel', 'end', 'expire', 'cease'],
                'patterns': [
                    r'(?:terminate|cancel|end|expire|cease)',
                    r'(?:notice\s+of\s+termination|cancellation\s+notice)',
                    r'(?:right\s+to\s+terminate|option\s+to\s+cancel)'
                ]
            },
            'liability': {
                'keywords': ['liability', 'indemnify', 'hold harmless', 'damages', 'losses'],
                'patterns': [
                    r'(?:liability|indemnify|indemnification)',
                    r'(?:hold\s+harmless|defend|protect)',
                    r'(?:damages|losses|expenses|costs)'
                ]
            },
            'confidentiality': {
                'keywords': ['confidential', 'secret', 'proprietary', 'non-disclosure', 'privacy'],
                'patterns': [
                    r'(?:confidential|secret|proprietary)',
                    r'(?:non.?disclosure|privacy|secrecy)',
                    r'(?:trade\s+secret|business\s+information)'
                ]
            }
        }
        
        # Risk level mapping
        self.risk_mapping = {
            'obligations': 'medium',
            'penalties': 'high',
            'renewals': 'medium',
            'termination': 'medium',
            'liability': 'high',
            'confidentiality': 'low'
        }
        
        # Importance scoring
        self.importance_indicators = {
            'high': ['shall', 'must', 'penalty', 'termination', 'liability', 'indemnify'],
            'medium': ['will', 'agree to', 'renewal', 'extension'],
            'low': ['may', 'can', 'confidential', 'proprietary']
        }
    
    def detect_clauses(self, text: str, line_numbers: List[int] = None) -> List[LegalClause]:
        """
        Detect legal clauses in the given text.
        
        Args:
            text: The text to analyze
            line_numbers: Optional list of line numbers for each line
            
        Returns:
            List of detected LegalClause objects
        """
        if not text:
            return []
        
        clauses = []
        lines = text.split('\n')
        
        # If no line numbers provided, generate them
        if line_numbers is None:
            line_numbers = list(range(1, len(lines) + 1))
        
        for clause_type, config in self.clause_patterns.items():
            detected = self._detect_clause_type(
                text, lines, line_numbers, clause_type, config
            )
            clauses.extend(detected)
        
        # Sort clauses by importance and confidence
        clauses.sort(key=lambda x: (self._get_importance_score(x.importance), x.confidence), reverse=True)
        
        logger.info(f"Detected {len(clauses)} legal clauses across {len(self.clause_patterns)} categories")
        return clauses
    
    def _detect_clause_type(self, text: str, lines: List[str], line_numbers: List[int], 
                           clause_type: str, config: Dict[str, Any]) -> List[LegalClause]:
        """Detect clauses of a specific type."""
        clauses = []
        
        # Check each line for clause patterns
        for i, (line, line_num) in enumerate(zip(lines, line_numbers)):
            line_lower = line.lower()
            
            # Check keywords first
            keyword_matches = [kw for kw in config['keywords'] if kw.lower() in line_lower]
            
            # Check regex patterns
            pattern_matches = []
            for pattern in config['patterns']:
                if re.search(pattern, line_lower, re.IGNORECASE):
                    pattern_matches.append(pattern)
            
            if keyword_matches or pattern_matches:
                # Calculate confidence based on matches
                confidence = self._calculate_confidence(keyword_matches, pattern_matches, line)
                
                # Determine importance
                importance = self._determine_importance(line_lower)
                
                # Get risk level
                risk_level = self.risk_mapping.get(clause_type, 'medium')
                
                clause = LegalClause(
                    text=line.strip(),
                    clause_type=clause_type,
                    start_line=line_num,
                    end_line=line_num,
                    importance=importance,
                    risk_level=risk_level,
                    confidence=confidence
                )
                clauses.append(clause)
        
        return clauses
    
    def _calculate_confidence(self, keyword_matches: List[str], pattern_matches: List[str], 
                             line: str) -> float:
        """Calculate confidence score for a detected clause."""
        base_confidence = 0.0
        
        # Keyword matches add confidence
        if keyword_matches:
            base_confidence += 0.4
        
        # Pattern matches add confidence
        if pattern_matches:
            base_confidence += 0.3
        
        # Line length and complexity factor
        if len(line.strip()) > 50:  # Longer lines are more likely to be clauses
            base_confidence += 0.1
        
        # Legal terminology density
        legal_terms = ['contract', 'agreement', 'party', 'clause', 'section', 'article']
        legal_term_count = sum(1 for term in legal_terms if term.lower() in line.lower())
        base_confidence += min(legal_term_count * 0.05, 0.2)
        
        return min(base_confidence, 1.0)
    
    def _determine_importance(self, line_lower: str) -> str:
        """Determine the importance level of a clause."""
        for importance, indicators in self.importance_indicators.items():
            if any(indicator.lower() in line_lower for indicator in indicators):
                return importance
        return 'medium'
    
    def _get_importance_score(self, importance: str) -> int:
        """Get numeric score for importance ranking."""
        scores = {'high': 3, 'medium': 2, 'low': 1}
        return scores.get(importance, 2)
    
    def get_clause_summary(self, clauses: List[LegalClause]) -> Dict[str, Any]:
        """Generate a summary of detected clauses."""
        if not clauses:
            return {'total_clauses': 0, 'clauses_by_type': {}, 'risk_distribution': {}}
        
        summary = {
            'total_clauses': len(clauses),
            'clauses_by_type': {},
            'risk_distribution': {},
            'importance_distribution': {},
            'high_priority_clauses': []
        }
        
        # Count clauses by type
        for clause in clauses:
            clause_type = clause.clause_type
            summary['clauses_by_type'][clause_type] = summary['clauses_by_type'].get(clause_type, 0) + 1
            
            # Count by risk level
            risk = clause.risk_level
            summary['risk_distribution'][risk] = summary['risk_distribution'].get(risk, 0) + 1
            
            # Count by importance
            importance = clause.importance
            summary['importance_distribution'][importance] = summary['importance_distribution'].get(importance, 0) + 1
            
            # Track high priority clauses
            if clause.importance == 'high' or clause.risk_level == 'high':
                summary['high_priority_clauses'].append({
                    'text': clause.text[:100] + '...' if len(clause.text) > 100 else clause.text,
                    'type': clause.clause_type,
                    'risk': clause.risk_level,
                    'importance': clause.importance,
                    'line': clause.start_line
                })
        
        return summary
