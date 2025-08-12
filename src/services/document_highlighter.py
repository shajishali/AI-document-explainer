import logging
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class HighlightType(Enum):
    """Types of highlighting for different risk levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

@dataclass
class DocumentHighlight:
    """Represents a highlighted section of the document."""
    start_line: int
    end_line: int
    start_char: int
    end_char: int
    highlight_type: HighlightType
    clause_type: str
    risk_level: str
    importance: str
    text: str
    tooltip: str
    css_class: str

@dataclass
class HighlightedDocument:
    """Complete document with highlighting information."""
    original_text: str
    highlights: List[DocumentHighlight]
    metadata: Dict[str, Any]
    summary: Dict[str, Any]

class DocumentHighlighter:
    """Service for highlighting document sections based on risk analysis."""
    
    def __init__(self):
        # Color scheme for different risk levels
        self.color_scheme = {
            HighlightType.CRITICAL: {
                'background': '#ffebee',
                'border': '#f44336',
                'text': '#c62828',
                'css_class': 'highlight-critical'
            },
            HighlightType.HIGH: {
                'background': '#fff3e0',
                'border': '#ff9800',
                'text': '#e65100',
                'css_class': 'highlight-high'
            },
            HighlightType.MEDIUM: {
                'background': '#fff8e1',
                'border': '#ffc107',
                'text': '#f57f17',
                'css_class': 'highlight-medium'
            },
            HighlightType.LOW: {
                'background': '#f1f8e9',
                'border': '#8bc34a',
                'text': '#558b2f',
                'css_class': 'highlight-low'
            },
            HighlightType.INFO: {
                'background': '#e3f2fd',
                'border': '#2196f3',
                'text': '#1565c0',
                'css_class': 'highlight-info'
            }
        }
        
        # Risk level to highlight type mapping
        self.risk_highlight_mapping = {
            'critical': HighlightType.CRITICAL,
            'high': HighlightType.HIGH,
            'medium': HighlightType.MEDIUM,
            'low': HighlightType.LOW,
            'minimal': HighlightType.INFO
        }
    
    def highlight_document(self, text: str, clauses: List[Any], 
                          risk_assessment: Any = None) -> HighlightedDocument:
        """
        Highlight document based on detected clauses and risk assessment.
        
        Args:
            text: Original document text
            clauses: List of detected legal clauses
            risk_assessment: Optional risk assessment for additional context
            
        Returns:
            HighlightedDocument with highlighting information
        """
        highlights = []
        
        # Generate highlights for each clause
        for clause in clauses:
            clause_highlights = self._highlight_clause(clause, text)
            highlights.extend(clause_highlights)
        
        # Add risk-based highlights if assessment available
        if risk_assessment:
            risk_highlights = self._highlight_risk_sections(risk_assessment, text)
            highlights.extend(risk_highlights)
        
        # Sort highlights by line number
        highlights.sort(key=lambda x: (x.start_line, x.start_char))
        
        # Generate metadata and summary
        metadata = self._generate_highlight_metadata(highlights)
        summary = self._generate_highlight_summary(highlights)
        
        return HighlightedDocument(
            original_text=text,
            highlights=highlights,
            metadata=metadata,
            summary=summary
        )
    
    def _highlight_clause(self, clause: Any, text: str) -> List[DocumentHighlight]:
        """Generate highlights for a specific clause."""
        highlights = []
        
        # Get clause properties
        clause_type = getattr(clause, 'clause_type', 'unknown')
        risk_level = getattr(clause, 'risk_level', 'medium')
        importance = getattr(clause, 'importance', 'medium')
        confidence = getattr(clause, 'confidence', 0.5)
        
        # Determine highlight type
        highlight_type = self.risk_highlight_mapping.get(risk_level.lower(), HighlightType.MEDIUM)
        
        # Get color scheme
        colors = self.color_scheme[highlight_type]
        
        # Create tooltip text
        tooltip = self._create_clause_tooltip(clause)
        
        # Find text position in document
        text_position = self._find_text_position(clause.text, text)
        
        if text_position:
            start_line, end_line, start_char, end_char = text_position
            
            highlight = DocumentHighlight(
                start_line=start_line,
                end_line=end_line,
                start_char=start_char,
                end_char=end_char,
                highlight_type=highlight_type,
                clause_type=clause_type,
                risk_level=risk_level,
                importance=importance,
                text=clause.text,
                tooltip=tooltip,
                css_class=colors['css_class']
            )
            highlights.append(highlight)
        
        return highlights
    
    def _highlight_risk_sections(self, risk_assessment: Any, text: str) -> List[DocumentHighlight]:
        """Generate highlights for high-risk sections based on assessment."""
        highlights = []
        
        # Highlight sections with high-risk indicators
        if hasattr(risk_assessment, 'risk_indicators'):
            for indicator in risk_assessment.risk_indicators:
                if indicator.severity == 'high':
                    # Find the section in text
                    section_highlight = self._highlight_risk_section(indicator, text)
                    if section_highlight:
                        highlights.append(section_highlight)
        
        return highlights
    
    def _highlight_risk_section(self, indicator: Any, text: str) -> Optional[DocumentHighlight]:
        """Highlight a specific risk section."""
        # Find the section containing the risk indicator
        lines = text.split('\n')
        
        # Look for the line reference
        line_num = getattr(indicator, 'line_reference', 0)
        if 0 < line_num <= len(lines):
            line_text = lines[line_num - 1]
            
            # Determine highlight type based on severity
            severity = getattr(indicator, 'severity', 'medium')
            highlight_type = self.risk_highlight_mapping.get(severity, HighlightType.MEDIUM)
            colors = self.color_scheme[highlight_type]
            
            # Create tooltip
            tooltip = f"Risk: {indicator.description}\nMitigation: {indicator.mitigation_suggestion}"
            
            highlight = DocumentHighlight(
                start_line=line_num,
                end_line=line_num,
                start_char=0,
                end_char=len(line_text),
                highlight_type=highlight_type,
                clause_type=getattr(indicator, 'category', 'risk'),
                risk_level=severity,
                importance='high',
                text=line_text,
                tooltip=tooltip,
                css_class=colors['css_class']
            )
            return highlight
        
        return None
    
    def _find_text_position(self, clause_text: str, document_text: str) -> Optional[Tuple[int, int, int, int]]:
        """Find the position of clause text within the document."""
        if not clause_text or not document_text:
            return None
        
        # Find the clause text in the document
        start_pos = document_text.find(clause_text)
        if start_pos == -1:
            return None
        
        end_pos = start_pos + len(clause_text)
        
        # Calculate line numbers and character positions
        lines = document_text.split('\n')
        current_pos = 0
        start_line = 1
        start_char = 0
        
        for i, line in enumerate(lines):
            line_length = len(line) + 1  # +1 for newline
            if current_pos <= start_pos < current_pos + line_length:
                start_line = i + 1
                start_char = start_pos - current_pos
                break
            current_pos += line_length
        
        # Find end line
        current_pos = 0
        end_line = start_line
        end_char = 0
        
        for i, line in enumerate(lines):
            line_length = len(line) + 1
            if current_pos <= end_pos <= current_pos + line_length:
                end_line = i + 1
                end_char = end_pos - current_pos
                break
            current_pos += line_length
        
        return start_line, end_line, start_char, end_char
    
    def _create_clause_tooltip(self, clause: Any) -> str:
        """Create tooltip text for a clause highlight."""
        tooltip_parts = []
        
        # Add clause type
        clause_type = getattr(clause, 'clause_type', 'Unknown')
        tooltip_parts.append(f"Type: {clause_type.title()}")
        
        # Add risk level
        risk_level = getattr(clause, 'risk_level', 'Unknown')
        tooltip_parts.append(f"Risk: {risk_level.title()}")
        
        # Add importance
        importance = getattr(clause, 'importance', 'Unknown')
        tooltip_parts.append(f"Importance: {importance.title()}")
        
        # Add confidence if available
        confidence = getattr(clause, 'confidence', None)
        if confidence is not None:
            confidence_pct = int(confidence * 100)
            tooltip_parts.append(f"Confidence: {confidence_pct}%")
        
        return "\n".join(tooltip_parts)
    
    def _generate_highlight_metadata(self, highlights: List[DocumentHighlight]) -> Dict[str, Any]:
        """Generate metadata about the highlighting."""
        if not highlights:
            return {'total_highlights': 0, 'highlight_types': {}}
        
        metadata = {
            'total_highlights': len(highlights),
            'highlight_types': {},
            'risk_distribution': {},
            'clause_distribution': {},
            'line_coverage': set()
        }
        
        for highlight in highlights:
            # Count highlight types
            highlight_type = highlight.highlight_type.value
            metadata['highlight_types'][highlight_type] = metadata['highlight_types'].get(highlight_type, 0) + 1
            
            # Count risk levels
            risk_level = highlight.risk_level
            metadata['risk_distribution'][risk_level] = metadata['risk_distribution'].get(risk_level, 0) + 1
            
            # Count clause types
            clause_type = highlight.clause_type
            metadata['clause_distribution'][clause_type] = metadata['clause_distribution'].get(clause_type, 0) + 1
            
            # Track line coverage
            for line_num in range(highlight.start_line, highlight.end_line + 1):
                metadata['line_coverage'].add(line_num)
        
        # Convert set to list for JSON serialization
        metadata['line_coverage'] = sorted(list(metadata['line_coverage']))
        
        return metadata
    
    def _generate_highlight_summary(self, highlights: List[DocumentHighlight]) -> Dict[str, Any]:
        """Generate summary of highlighting results."""
        if not highlights:
            return {'summary': 'No highlights found'}
        
        # Group highlights by type
        by_type = {}
        by_risk = {}
        by_clause = {}
        
        for highlight in highlights:
            # Group by highlight type
            highlight_type = highlight.highlight_type.value
            if highlight_type not in by_type:
                by_type[highlight_type] = []
            by_type[highlight_type].append(highlight)
            
            # Group by risk level
            risk_level = highlight.risk_level
            if risk_level not in by_risk:
                by_risk[risk_level] = []
            by_risk[risk_level].append(highlight)
            
            # Group by clause type
            clause_type = highlight.clause_type
            if clause_type not in by_clause:
                by_clause[clause_type] = []
            by_clause[clause_type].append(highlight)
        
        summary = {
            'total_highlights': len(highlights),
            'highlights_by_type': {k: len(v) for k, v in by_type.items()},
            'highlights_by_risk': {k: len(v) for k, v in by_risk.items()},
            'highlights_by_clause': {k: len(v) for k, v in by_clause.items()},
            'most_highlighted_type': max(by_type.items(), key=lambda x: len(x[1]))[0] if by_type else None,
            'highest_risk_highlights': len([h for h in highlights if h.risk_level in ['high', 'critical']])
        }
        
        return summary
    
    def generate_css_styles(self) -> str:
        """Generate CSS styles for the highlighting."""
        css = []
        
        for highlight_type, colors in self.color_scheme.items():
            css_class = colors['css_class']
            css.append(f"""
.{css_class} {{
    background-color: {colors['background']};
    border-left: 4px solid {colors['border']};
    padding: 8px 12px;
    margin: 4px 0;
    border-radius: 4px;
    position: relative;
    cursor: pointer;
}}

.{css_class}:hover {{
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}}

.{css_class}::before {{
    content: attr(data-tooltip);
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    background: #333;
    color: white;
    padding: 8px;
    border-radius: 4px;
    font-size: 12px;
    white-space: pre-line;
    z-index: 1000;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s;
}}

.{css_class}:hover::before {{
    opacity: 1;
}}
""")
        
        return "\n".join(css)
    
    def generate_html_highlights(self, text: str, highlights: List[DocumentHighlight]) -> str:
        """Generate HTML with embedded highlights."""
        if not highlights:
            return text
        
        # Sort highlights by position
        sorted_highlights = sorted(highlights, key=lambda x: (x.start_line, x.start_char))
        
        # Split text into lines
        lines = text.split('\n')
        html_lines = []
        
        for line_num, line in enumerate(lines, 1):
            line_highlights = [h for h in sorted_highlights if h.start_line == line_num]
            
            if not line_highlights:
                html_lines.append(f"<div class='line' data-line='{line_num}'>{line}</div>")
                continue
            
            # Apply highlights to this line
            highlighted_line = self._apply_line_highlights(line, line_highlights, line_num)
            html_lines.append(highlighted_line)
        
        return "\n".join(html_lines)
    
    def _apply_line_highlights(self, line: str, line_highlights: List[DocumentHighlight], 
                              line_num: int) -> str:
        """Apply highlights to a single line."""
        if not line_highlights:
            return f"<div class='line' data-line='{line_num}'>{line}</div>"
        
        # Sort highlights by character position
        sorted_highlights = sorted(line_highlights, key=lambda x: x.start_char)
        
        # Build highlighted line
        highlighted_parts = []
        current_pos = 0
        
        for highlight in sorted_highlights:
            # Add text before highlight
            if highlight.start_char > current_pos:
                highlighted_parts.append(line[current_pos:highlight.start_char])
            
            # Add highlighted text
            highlight_text = line[highlight.start_char:highlight.end_char]
            tooltip = highlight.tooltip.replace('"', '&quot;')
            
            highlighted_part = f'<span class="{highlight.css_class}" data-tooltip="{tooltip}" data-type="{highlight.clause_type}" data-risk="{highlight.risk_level}">{highlight_text}</span>'
            highlighted_parts.append(highlighted_part)
            
            current_pos = highlight.end_char
        
        # Add remaining text
        if current_pos < len(line):
            highlighted_parts.append(line[current_pos:])
        
        highlighted_text = "".join(highlighted_parts)
        return f'<div class="line" data-line="{line_num}">{highlighted_text}</div>'
