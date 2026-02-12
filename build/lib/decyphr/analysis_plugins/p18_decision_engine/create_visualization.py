
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
        priority = rec.get("priority", "Low").lower()
        rationale = rec.get("rationale", "")

        # Color coding
        bg_color = "#f0f8ff"
        if priority == "critical": bg_color = "#fff0f0"
        elif priority == "high": bg_color = "#fff8e0"

        html_content += f"""
        <div style="background-color: {bg_color}; padding: 20px; margin-bottom: 15px; border-radius: 8px; border: 1px solid #e0e0e0;">
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <span style="background-color: #333; color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.75em; margin-right: 10px;">{rec_type}</span>
                <h3 style="margin: 0; font-size: 1.2em; color: #222;">{action}</h3>
            </div>
            <p style="margin: 0; font-style: italic; color: #555;"><strong>Rationale:</strong> {rationale}</p>
        </div>
        """
    
    html_content += '</div>'

    return {
        "details_html": html_content,
        "visuals": [],
        "suppress_plot_grid": True
    }
