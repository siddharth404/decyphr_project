
from typing import Dict, Any, List

def create_visuals(ddf, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates the HTML representation for the Decision Recommendation Engine section.
    """
    recommendations = analysis_results.get("recommendations", [])
    
    if not recommendations:
        return {"details_html": "<p>No specific recommendations generated.</p>", "visuals": []}

    # CSS for Impact Badges
    html_content = """
    <style>
    .impact-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.7em;
        font-weight: bold;
        margin-left: 10px;
        text-transform: uppercase;
        vertical-align: middle;
    }
    .impact-high { background-color: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }
    .impact-medium { background-color: #fef3c7; color: #92400e; border: 1px solid #fde68a; }
    .impact-low { background-color: #d1fae5; color: #065f46; border: 1px solid #a7f3d0; }
    </style>
    <div class="decision-engine-container">
    """
    
    for rec in recommendations:
        action = rec.get("action", "")
        rec_type = rec.get("type", "General")
        priority = rec.get("priority", "Low").lower()
        rationale = rec.get("rationale", "")

        confidence = rec.get("confidence_score", 0.0)
        conf_percent = int(confidence * 100)
        conf_reason = rec.get("confidence_reason", "No specific reason provided.")
        
        # Impact Fields
        impact_level = rec.get("impact_level", "Medium")
        impact_desc = rec.get("estimated_business_impact", "")
        impact_class = f"impact-{impact_level.lower()}"

        # Color coding
        bg_color = "#f0f8ff"
        if rec_type == "Technical": 
            bg_color = "#f0f9ff" # light blue
        elif rec_type == "Strategic": 
            bg_color = "#faf5ff" # light purple
        elif rec_type == "Marketing": 
            bg_color = "#fffbeb" # light yellow
        elif rec_type == "Operational":
             bg_color = "#fef2f2" # light red

        # Border color based on type
        border_color = "#ccc"
        if rec_type == "Technical": border_color = "#0ea5e9"
        elif rec_type == "Strategic": border_color = "#8b5cf6"
        elif rec_type == "Marketing": border_color = "#f59e0b"
        elif rec_type == "Operational": border_color = "#ef4444"

        html_content += f"""
        <div style="background-color: {bg_color}; padding: 20px; margin-bottom: 15px; border-radius: 8px; border-left: 5px solid {border_color}; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <div style="display: flex; align-items: center; margin-bottom: 12px; justify-content: space-between;">
                <div style="display: flex; align-items: center;">
                    <span style="background-color: {border_color}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.75em; text-transform: uppercase; font-weight: bold; margin-right: 10px;">{rec_type}</span>
                    <h3 style="margin: 0; font-size: 1.1em; color: #1f2937;">{action}</h3>
                    <span class="impact-badge {impact_class}">Impact: {impact_level}</span>
                </div>
                 <div style="text-align: right;">
                    <span style="font-size: 0.9em; color: #4b5563; font-weight: bold;">Conf: {conf_percent}%</span>
                    <div style="width: 100px; height: 6px; background: #e5e7eb; border-radius: 3px; margin-top: 4px;">
                        <div style="width: {conf_percent}%; height: 100%; background: {border_color}; border-radius: 3px;"></div>
                    </div>
                </div>
            </div>
            
            <p style="margin: 0 0 10px 0; font-size: 0.95em; color: #374151;">
                <strong>Rationale:</strong> {rationale}
            </p>
            
            <div style="margin-top: 12px; padding-top: 10px; border-top: 1px solid rgba(0,0,0,0.05);">
                 <div style="font-size: 0.85em; color: #4b5563; margin-bottom: 4px;">
                    <strong>Business Impact:</strong> <em>{impact_desc}</em>
                </div>
                <div style="font-size: 0.8em; color: #6b7280;">
                     <span style="opacity: 0.8;">Confidence Source: {conf_reason}</span>
                </div>
            </div>
        </div>
        """
    
    html_content += '</div>'

    return {
        "details_html": html_content,
        "visuals": [],
        "suppress_plot_grid": True
    }
