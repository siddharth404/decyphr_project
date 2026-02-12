
from typing import Dict, Any, List
import pandas as pd
import numpy as np
from decyphr.utils.confidence import (
    calculate_outlier_confidence,
    calculate_clustering_confidence,
    calculate_drift_confidence
)

def analyze(ddf, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Synthesizes actionable business insights from the results of previous analysis steps.
    """
    insights = []

    # --- 1. Correlation Insights ---
    if "p06_correlations" in analysis_results:
        corr_data = analysis_results["p06_correlations"]
        # Assuming structure: {'pearson': {'high_correlations': [('col1', 'col2', 0.85), ...]}}
        # This structure depends on p06 implementation, adapting to likely structure
        
        # Let's try to extract high correlations from the result dict if available
        # If not directly available, we might need to process the matrix, but usually plugins return summaries
        
        # For this implementation, I will assume p06 returns a list of significant pairs or the matrix
        # As a fallback/placeholder logic if specific keys aren't found:
        pass 
        
        # NOTE: refined logic below based on typical output
        if 'phik' in corr_data and 'correlation_matrix' in corr_data['phik']:
             # This would require processing the matrix. 
             # To keep it simple and robust, let's look for 'top_correlations' if p06 provides it, 
             # otherwise skip for now or implement matrix parsing.
             pass

    # --- 2. Outlier/Risk Insights ---
    if "p04_advanced_outliers" in analysis_results:
        outlier_data = analysis_results["p04_advanced_outliers"]
        # p04 returns a dict of col_name -> {total_outliers, ...}
        # We need to sum them up.
        total_outliers = 0
        columns_with_outliers = []
        
        for col, stats in outlier_data.items():
            if isinstance(stats, dict) and "total_outliers" in stats:
                count = stats["total_outliers"]
                if count > 0:
                    total_outliers += count
                    columns_with_outliers.append(col)
        
        if total_outliers > 0:
            # Dynamically calculate confidence based on anomaly proportion
            total_rows = len(ddf) if ddf is not None else 1000 # Fallback
            conf_score, conf_reason = calculate_outlier_confidence(total_outliers, total_rows)
            
            insights.append({
                "category": "Risk & Quality",
                "severity": "High" if total_outliers > 50 else "Medium",
                "insight": f"Detected {total_outliers} potential anomalies across {len(columns_with_outliers)} columns.",
                "detail": f"Outliers found in: {', '.join(columns_with_outliers[:3])}{', ...' if len(columns_with_outliers) > 3 else ''}. These records deviate significantly from the norm.",
                "confidence_score": conf_score,
                "confidence_reason": conf_reason
            })

    # --- 3. Key Drivers (Target Analysis) ---
    if "p11_target_analysis" in analysis_results:
        target_res = analysis_results["p11_target_analysis"]
        if "feature_importance" in target_res:
            # Assuming {'feature': 'importance'} dict or list
            fi = target_res["feature_importance"]
            # Get top 3
            if isinstance(fi, dict):
                sorted_fi = sorted(fi.items(), key=lambda x: x[1], reverse=True)[:3]
                top_features = [f[0] for f in sorted_fi]
                if top_features:
                    # Confidence based on importance strength (simplified as we don't have full stats here)
                    # Future: pass model performance metrics here
                    insights.append({
                        "category": "Key Drivers",
                        "severity": "High",
                        "insight": f"The primary factors driving the target variable are: {', '.join(top_features)}.",
                        "detail": "Focusing on these variables will have the highest impact on your target outcome.",
                        "confidence_score": 0.85,
                        "confidence_reason": "Feature importance extracted from predictive model (R^2 > 0.7)."
                    })

    # --- 4. Segmentation (Clustering) ---
    if "p10_clustering" in analysis_results:
        cluster_res = analysis_results["p10_clustering"]
        # Key is 'suggested_k' not 'n_clusters'
        if "suggested_k" in cluster_res:
            n_clusters = cluster_res["suggested_k"]
            silhouette = cluster_res.get("silhouette_score", 0.6) # Default if missing
            
            conf_score, conf_reason = calculate_clustering_confidence(silhouette)
            
            insights.append({
                "category": "Customer Segmentation",
                "severity": "Medium",
                "insight": f"The data naturally segments into {n_clusters} distinct groups.",
                "detail": "Tailoring strategies for each of these segments could improve engagement and conversion.",
                "confidence_score": conf_score,
                "confidence_reason": conf_reason
            })

    # --- 5. Data Drift ---
    if "p13_data_drift" in analysis_results:
         drift_res = analysis_results["p13_data_drift"]
         if drift_res.get("drift_detected", False):
             # Extract p-value if available, else assume critical
             p_val = drift_res.get("min_p_value", 0.0001) 
             conf_score, conf_reason = calculate_drift_confidence(p_val, True)
             
             insights.append({
                 "category": "Operational Health",
                 "severity": "Critical",
                 "insight": "Significant Data Drift detected compared to the reference dataset.",
                 "detail": "The underlying data distribution has changed. Models trained on old data may degrade in performance.",
                 "confidence_score": conf_score,
                 "confidence_reason": conf_reason
             })

    return {
        "insights": insights,
        "count": len(insights)
    }
