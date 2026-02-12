
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
        
        # Severity class mapping (ensure lowercase)
        sev_class = severity
        
        html_content += f"""
        <div class="insight-card {sev_class}">
            <div class="insight-header">
                <h4 class="insight-title">{category}</h4>
                <div class="insight-meta">
                    <div class="confidence-wrapper">
                        <span class="confidence-label">Confidence: {conf_percent}%</span>
                        <span class="severity-badge {sev_class}">{severity}</span>
                    </div>
                </div>
            </div>
            <div class="confidence-bar-container">
                <div class="confidence-bar-fill" style="width: {conf_percent}%;"></div>
            </div>
            <p class="insight-reason"><em>{conf_reason}</em></p>
            <p class="insight-text">{text}</p>
            <p class="insight-detail">{detail}</p>
        </div>
        """
    
    html_content += '</div>'

    return {
        "details_html": html_content,
        "visuals": [],
        "suppress_plot_grid": True
    }
