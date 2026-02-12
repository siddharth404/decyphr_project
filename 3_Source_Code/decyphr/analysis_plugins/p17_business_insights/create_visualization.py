
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
                <span style="font-size: 0.8em; font-weight: bold; color: {border_color}; text-transform: uppercase;">{severity}</span>
            </div>
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
