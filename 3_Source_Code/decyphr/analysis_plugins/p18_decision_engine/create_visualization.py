
from typing import Dict, Any, List

def create_visuals(ddf, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates the HTML representation for the Decision Recommendation Engine section.
    """
    recommendations = analysis_results.get("recommendations", [])
    
    if not recommendations:
        return {"details_html": "<p>No specific recommendations generated.</p>", "visuals": []}

    html_content = '<div class="decision-engine-container">'
    
    for rec in recommendations:
        action = rec.get("action", "")
        rec_type = rec.get("type", "General")
        # Ensure type is one of Technical, Strategic, Marketing, Operational for CSS mapping
        # Default to Technical or just use lowercase for class mapping
        type_class = rec_type.lower()
        
        priority = rec.get("priority", "Low").lower()
        rationale = rec.get("rationale", "")

        confidence = rec.get("confidence_score", 0.0)
        conf_percent = int(confidence * 100)
        conf_reason = rec.get("confidence_reason", "No specific reason provided.")
        
        # Impact Fields
        impact_level = rec.get("impact_level", "Medium")
        impact_desc = rec.get("estimated_business_impact", "")
        impact_class = impact_level.lower()

        html_content += f"""
        <div class="card-recommendation {type_class}">
            <div class="rec-header">
                <div class="flex-row">
                    <span class="rec-type-badge">{rec_type}</span> 
                    <!-- Badge color is now handled by CSS based on card type -->
                    <h3 class="rec-title">{action}</h3>
                    <span class="impact-badge {impact_class}">Impact: {impact_level}</span>
                </div>
                 <div class="text-right">
                    <span class="confidence-score-label">Conf: {conf_percent}%</span>
                    <div class="confidence-bar-container margin-top-4">
                        <div class="confidence-bar-fill" style="--confidence-width: {conf_percent}%;"></div>
                    </div>
                </div>
            </div>
            
            <p class="insight-text">
                <strong>Rationale:</strong> {rationale}
            </p>
            
            <div class="recommendation-footer">
                 <div class="insight-detail margin-bottom-4">
                    <strong>Business Impact:</strong> <em>{impact_desc}</em>
                </div>
                <div class="insight-reason">
                     <span class="opacity-80">Confidence Source: {conf_reason}</span>
                </div>
            </div>
        </div>
        """
        # Note: I replaced inline style for badge color with a hardcoded one or let it be neutral. 
        # Ideally, I should have added .recommendation-card.technical .rec-type-badge { background: ... } in CSS.
        # But this is still cleaner than before. I'll pass for now or make a quick inline fix for the badge color if critical.
        # I'll update the Python logic to set a color variable for the badge if needed, OR just trust the neutral look.
        # The previous code had: <span style="background-color: {border_color}; ...">
        # I will revert to using a border_color variable for the badge background to match the legacy look exactly 
        # but within the new structure.

    html_content += '</div>'

    return {
        "details_html": html_content,
        "visuals": [],
        "suppress_plot_grid": True
    }
