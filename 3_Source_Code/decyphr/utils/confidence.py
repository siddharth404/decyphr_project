
import numpy as np

def normalize_score(score: float) -> float:
    """Clamps a score between 0.0 and 1.0."""
    return max(0.0, min(1.0, float(score)))

def calculate_outlier_confidence(n_outliers: int, total_rows: int) -> tuple[float, str]:
    """
    Calculates confidence based on the proportion of outliers.
    
    Heuristic:
    - If outliers are < 1% of data: High confidence (95%) - likely true anomalies.
    - If outliers are 1-5% of data: Medium-High confidence (85%) - typical for noisy data.
    - If outliers are 5-10% of data: Medium confidence (70%) - potentially heavy-tailed distribution.
    - If outliers are > 10% of data: Low confidence (50%) - structural issue or wrong distribution assumption.
    """
    if total_rows == 0:
        return 0.0, "No data rows available."
    
    proportion = n_outliers / total_rows
    
    if proportion < 0.01:
        return 0.95, "Anomalies are rare (<1%), indicating strong signal."
    elif proportion < 0.05:
        return 0.85, "Anomalies are distinct but common (1-5%)."
    elif proportion < 0.10:
        return 0.70, "High frequency of outliers (>5%) suggests heavy tails."
    else:
        return 0.50, "Excessive outliers (>10%) may indicate distribution mismatch."

def calculate_correlation_confidence(correlation_val: float, n_samples: int) -> tuple[float, str]:
    """
    Calculates confidence for a correlation insight.
    
    Heuristic:
    - Base confidence derived from absolute correlation strength.
    - Penalized if sample size is small (< 30).
    """
    abs_corr = abs(correlation_val)
    
    # Base score on strength
    if abs_corr > 0.8:
        base_score = 0.95
        strength_desc = "Very strong relationship"
    elif abs_corr > 0.6:
        base_score = 0.85
        strength_desc = "Strong relationship"
    elif abs_corr > 0.4:
        base_score = 0.70
        strength_desc = "Moderate relationship"
    else:
        base_score = 0.50
        strength_desc = "Weak relationship"
        
    # Sample size penalty
    if n_samples < 30:
        base_score *= 0.8
        reason = f"{strength_desc} but low sample size ({n_samples})."
    else:
        reason = f"{strength_desc} supported by sufficient data."
        
    return normalize_score(base_score), reason

def calculate_clustering_confidence(silhouette_score: float) -> tuple[float, str]:
    """
    Calculates confidence based on Silhouette Score (-1 to 1).
    """
    # Map silhouette (-1 to 1) to confidence (0 to 1) roughly
    # > 0.7: Strong structure (95%)
    # > 0.5: Reasonable structure (80%)
    # > 0.25: Weak structure (60%)
    # <= 0.25: No substantial structure (40%)
    
    if silhouette_score > 0.7:
        return 0.95, f"High silhouette score ({silhouette_score:.2f}) indicates distinct clusters."
    elif silhouette_score > 0.5:
        return 0.80, f"Good silhouette score ({silhouette_score:.2f}) indicates reasonable separation."
    elif silhouette_score > 0.25:
        return 0.60, f"Low silhouette score ({silhouette_score:.2f}) indicates weak clusters."
    else:
        return 0.40, f"Very low silhouette score ({silhouette_score:.2f}) suggests data may not be clustered."

def calculate_drift_confidence(p_value: float, drift_detected: bool) -> tuple[float, str]:
    """
    Calculates confidence for data drift detection.
    """
    if drift_detected:
        # If drift is detected, how confident are we?
        # Low p-value means we are confident the distributions are different.
        if p_value < 0.001:
            return 0.99, "Drift highly significant (p < 0.001)."
        elif p_value < 0.05:
            return 0.90, "Drift significant (p < 0.05)."
        else:
            return 0.60, "Drift detected but borderline significance."
    else:
        # If no drift detected
        if p_value > 0.1:
            return 0.90, "No significant drift (p > 0.1)."
        else:
            return 0.70, "No drift detected, but p-value is low."
