
from typing import Dict, Any, List

def analyze(ddf, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates actionable recommendations based on the business insights.
    """
    recommendations = []
    
    # Retrieve insights from p17
    p17_results = analysis_results.get("p17_business_insights", {})
    insights = p17_results.get("insights", [])

    for insight in insights:
        cat = insight.get("category", "")
        text = insight.get("insight", "")
        
        insight_conf = insight.get("confidence_score", 0.5)
        insight_reason = insight.get("confidence_reason", "No specific confidence reason provided.")

        # --- Logic Mapping ---
        
        # 1. Anomaly / Risk -> Audit Action
        if cat == "Risk & Quality":
            # Operational is highly actionable, keeping confidence high
            final_conf = insight_conf * 1.0 
            recommendations.append({
                "action": "Conduct a Root Cause Analysis on identified anomalies.",
                "type": "Operational",
                "priority": "High",
                "rationale": "Outliers often indicate data quality issues or high-risk events (fraud, failure) that require immediate human review.",
                "confidence_score": final_conf,
                "confidence_reason": f"Directly actionable. Source: {insight_reason}"
            })

        # 2. Key Drivers -> Strategic Optimization
        elif cat == "Key Drivers":
            # Strategic is slightly less certain in outcome
            final_conf = insight_conf * 0.85
            recommendations.append({
                "action": "Optimize marketing/operational spend towards the top 3 driver variables.",
                "type": "Strategic",
                "priority": "High",
                "rationale": "Small improvements in these high-impact variables will yield outsized returns on the target metric.",
                "confidence_score": final_conf,
                "confidence_reason": f"Strategic alignment. Source: {insight_reason}"
            })

        # 3. Segmentation -> Personalization
        elif cat == "Customer Segmentation":
            # Marketing is variable
            final_conf = insight_conf * 0.80
            recommendations.append({
                "action": "Develop distinct engagement strategies (e.g., personalized emails) for each identified segment.",
                "type": "Marketing",
                "priority": "Medium",
                "rationale": "One-size-fits-all approaches fail with heterogeneous groups. Clustering reveals distinct needs.",
                "confidence_score": final_conf,
                "confidence_reason": f"Execution variability. Source: {insight_reason}"
            })

        # 4. Drift -> MLOps
        elif cat == "Operational Health":
            # Technical actions are deterministic
            final_conf = insight_conf * 0.95
            recommendations.append({
                "action": "Trigger automated model retraining pipeline immediately.",
                "type": "Technical",
                "priority": "Critical",
                "rationale": "Data drift implies that current models are making decisions based on outdated patterns.",
                "confidence_score": final_conf,
                "confidence_reason": f"Technical necessity. Source: {insight_reason}"
            })

    # Fallback/Generic Recommendations if list is empty
    if not recommendations:
        recommendations.append({
            "action": "Review data collection pipeline for potential gaps.",
            "type": "Technical",
            "priority": "Low",
            "rationale": "No specific high-level insights were generated, suggesting data may be uniform or insufficient."
        })

    return {
        "recommendations": recommendations,
        "count": len(recommendations)
    }
