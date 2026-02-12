
from typing import Dict, Any, List

def create_visuals(ddf, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates the HTML representation for the Business Insights section.
    """
    insights = analysis_results.get("insights", [])
    
    if not insights:
        return {"details_html": "<p>No significant business insights detected.</p>", "visuals": []}

    html_content = '<div class="business-insights-container">'
    
    for insight in insights:
        category = insight.get("category", "General")
        severity = insight.get("severity", "Low").lower()
        text = insight.get("insight", "")
        detail = insight.get("detail", "")
        
        confidence = insight.get("confidence_score", 0.0)
        conf_percent = int(confidence * 100)
        conf_reason = insight.get("confidence_reason", "No specific reason provided.")
        
        # Color coding based on severity
        border_color = "#ccc"
        if severity == "critical": border_color = "#ff4444"
        elif severity == "high": border_color = "#ff8800"
        elif severity == "medium": border_color = "#ffbb33"
        elif severity == "low": border_color = "#00C851"

        html_content += f"""
        <div style="border-left: 5px solid {border_color}; background-color: #f9f9f9; padding: 15px; margin-bottom: 10px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                <h4 style="margin: 0; color: #333; font-weight: 600;">{category}</h4>
                <div style="display: flex; flex-direction: column; align-items: flex-end;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 0.8em; color: #666;">Confidence: {conf_percent}%</span>
                        <span style="font-size: 0.8em; font-weight: bold; color: {border_color}; text-transform: uppercase;">{severity}</span>
                    </div>
                </div>
            </div>
            <div style="width: 100%; background-color: #e0e0e0; height: 4px; border-radius: 2px; margin-bottom: 4px;">
                <div style="width: {conf_percent}%; background-color: {border_color}; height: 100%; border-radius: 2px;"></div>
            </div>
            <p style="margin: 0 0 8px 0; font-size: 0.75em; color: #888; font-style: italic;">{conf_reason}</p>
            <p style="margin: 5px 0; font-size: 1.1em; color: #000;">{text}</p>
            <p style="margin: 0; font-size: 0.9em; color: #666;">{detail}</p>
        </div>
        """
    
    html_content += '</div>'

    return {
        "details_html": html_content,
        "visuals": [],
        "suppress_plot_grid": True
    }
