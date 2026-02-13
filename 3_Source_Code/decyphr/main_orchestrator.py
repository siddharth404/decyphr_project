# ==============================================================================
# FILE: 3_Source_Code/decyphr/main_orchestrator.py
# ==============================================================================
# PURPOSE: This is the central brain of decyphr. It orchestrates the entire
#          analysis pipeline from data loading to final reporting.

import os
import json
import os
import json
import time
import numpy as np
from datetime import datetime
from typing import Dict, Any, Optional

# --- Import Core Modules (Using Absolute Imports) ---
from decyphr.backends.dask_backend import load_dataframe_from_file
from decyphr.report_builder.builder import build_html_report

# --- Import All Analysis Plugin Functions (Using Absolute Imports) ---
from decyphr.analysis_plugins.p01_overview import run_analysis as overview_analysis
from decyphr.analysis_plugins.p02_univariate import run_analysis as univariate_analysis
from decyphr.analysis_plugins.p03_data_quality import run_analysis as data_quality_analysis
from decyphr.analysis_plugins.p04_advanced_outliers import run_analysis as outliers_analysis
from decyphr.analysis_plugins.p05_missing_values import run_analysis as missing_values_analysis
from decyphr.analysis_plugins.p06_correlations import run_analysis as correlations_analysis
from decyphr.analysis_plugins.p07_interactions import run_analysis as interactions_analysis
from decyphr.analysis_plugins.p08_hypothesis_testing import run_analysis as hypothesis_testing_analysis
from decyphr.analysis_plugins.p09_pca import run_analysis as pca_analysis
from decyphr.analysis_plugins.p10_clustering import run_analysis as clustering_analysis
from decyphr.analysis_plugins.p11_target_analysis import run_analysis as target_analysis
from decyphr.analysis_plugins.p12_explainability_shap import run_analysis as shap_analysis
from decyphr.analysis_plugins.p13_data_drift import run_analysis as data_drift_analysis
from decyphr.analysis_plugins.p14_deep_text_analysis import run_analysis as text_analysis
from decyphr.analysis_plugins.p15_timeseries import run_analysis as timeseries_analysis
from decyphr.analysis_plugins.p16_geospatial import run_analysis as geospatial_analysis
from decyphr.analysis_plugins.p17_business_insights import run_analysis as business_insights_analysis
from decyphr.analysis_plugins.p18_decision_engine import run_analysis as decision_engine_analysis


def run_analysis_pipeline(filepath: str, target: Optional[str] = None, compare_filepath: Optional[str] = None) -> Optional[str]:
    """
    Executes the full, end-to-end decyphr analysis pipeline.
    
    Returns:
        The file path to the generated HTML report, or None if it fails.
    """
    ddf = load_dataframe_from_file(filepath)
    if ddf is None:
        print("Decyphr 🚩: Halting execution due to primary data loading failure.")
        return None

    print("\nDecyphr ⚙️: Starting analysis pipeline...")
    start_time = time.time()
    
    print("  -> Running plugin [1/19]: p01_overview")
    overview_results = overview_analysis.analyze(ddf)
    
    analysis_results: Dict[str, Any] = {"p01_overview": overview_results}
    if "error" in overview_results:
        print(f"Decyphr 🚩: Halting execution due to critical failure in overview analysis: {overview_results['error']}")
        return None

    # Note: analysis_results is passed by reference, so plugins running later will see updates.
    pipeline_steps = [
        ("p02_univariate", univariate_analysis.analyze, False, [overview_results]),
        ("p03_data_quality", data_quality_analysis.analyze, False, [overview_results]),
        ("p04_advanced_outliers", outliers_analysis.analyze, False, [overview_results]),
        ("p05_missing_values", missing_values_analysis.analyze, False, [overview_results]),
        ("p06_correlations", correlations_analysis.analyze, False, [overview_results]),
        ("p07_interactions", interactions_analysis.analyze, False, [overview_results]),
        ("p08_hypothesis_testing", hypothesis_testing_analysis.analyze, False, [overview_results]),
        ("p09_pca", pca_analysis.analyze, False, [overview_results]),
        ("p10_clustering", clustering_analysis.analyze, False, [overview_results, target]),
        ("p11_target_analysis", target_analysis.analyze, True, [overview_results, target]),
        ("p12_explainability_shap", shap_analysis.analyze, True, [overview_results, target]),
        ("p14_deep_text_analysis", text_analysis.analyze, False, [overview_results]),
        ("p15_timeseries", timeseries_analysis.analyze, False, [overview_results, target]),
        ("p16_geospatial", geospatial_analysis.analyze, False, [overview_results, target]),
        ("p17_business_insights", business_insights_analysis.analyze, False, [analysis_results]),
        ("p18_decision_engine", decision_engine_analysis.analyze, False, [analysis_results]),
    ]

    for i, (name, func, req_target, args) in enumerate(pipeline_steps, start=2):
        print(f"  -> Running plugin [{i}/19]: {name}")
        if req_target and not target:
            print(f"     ... Skipping '{name}', no target variable provided.")
            continue
        try:
            result = func(ddf, *args)
            analysis_results[name] = result
        except Exception as e:
            print(f"Decyphr ❌: Error in plugin '{name}': {e}")
            analysis_results[name] = {"error": str(e)}

    if compare_filepath:
        pass

    print("Decyphr ✅: Analysis pipeline complete.")
    end_time = time.time()
    execution_time = round(end_time - start_time, 2)

    # --- System Metrics Collection ---
    try:
        # Insights Count
        p17_results = analysis_results.get("p17_business_insights", {})
        insights_count = len(p17_results.get("insights", [])) if "insights" in p17_results else 0

        # Recommendations Count
        p18_results = analysis_results.get("p18_decision_engine", {})
        recommendations_count = len(p18_results.get("recommendations", [])) if "recommendations" in p18_results else 0

        # Anomaly Count (from p04 or p17 summary is easier if p04 output structure varies)
        # Using p04 results directly
        p04_results = analysis_results.get("p04_advanced_outliers", {})
        anomaly_count = 0
        if p04_results and "error" not in p04_results and "message" not in p04_results:
             for col, res in p04_results.items():
                 if isinstance(res, dict):
                     anomaly_count += res.get("total_outliers", 0)

        # Dataset Stats
        p01_stats = analysis_results.get("p01_overview", {}).get("dataset_stats", {})
        
        # Top Feature Importance
        top_feature = "N/A"
        
        # 1. Try direct from p11 (Target Analysis)
        p11_results = analysis_results.get("p11_target_analysis", {})
        if "feature_importances" in p11_results:
            importances = p11_results["feature_importances"]
            if importances:
                # p11 returns sorted ascending (smallest -> largest)
                # So the last key is the most important feature
                # Store as tuple (name, score) if possible, or just name
                top_feature_name = list(importances.keys())[-1]
                top_feature_score = importances[top_feature_name]
                top_feature = {"name": top_feature_name, "score": top_feature_score}
        
        # 2. Fallback: Parse p17 Insights
        if top_feature == "N/A":
             for insight in p17_results.get("insights", []):
                 if insight.get("category") == "Key Drivers":
                     # Text: "The primary factors... are: FeatureA, FeatureB."
                     import re
                     match = re.search(r"are:\s*(.*?)(\.|,)", insight.get("insight", ""))
                     if match:
                         # Heuristic extraction, set score to None
                         top_feature = {"name": match.group(1).split(',')[0].strip(), "score": None}
                     break
        
        # 3. Last Resort: p06 Correlations
        if top_feature == "N/A":
            p06_results = analysis_results.get("p06_correlations", {})
            if "top_correlations" in p06_results:
                # heuristic: grab first significant correlation pair
                pass # implementation detail omitted for brevity, stick to "N/A" if p11/p17 fail

        # --- Health Score and Data Quality Metrics ---
        try:
            # Parse metrics from string "X%" to float
            def parse_pct(val):
                if isinstance(val, (int, float)): return float(val)
                if isinstance(val, str) and '%' in val:
                    return float(val.replace('%', ''))
                return 0.0

            missing_pct = parse_pct(p01_stats.get("Missing Cells (%)", 0))
            duplicate_pct = parse_pct(p01_stats.get("Duplicate Rows (%)", 0))
            
            num_rows = p01_stats.get("Number of Rows", 0)
            if num_rows > 0:
                anomaly_pct = (anomaly_count / num_rows) * 100
                anomaly_ratio = anomaly_count / num_rows
            else:
                anomaly_pct = 0
                anomaly_ratio = 0.0

            # Formula: 100 - (missing) - (duplicate) - (0.5 * anomaly)
            raw_score = 100 - missing_pct - duplicate_pct - (0.5 * anomaly_pct)
            health_score = max(0, min(100, round(raw_score, 1)))

            # Determine Label (Updated Thresholds)
            if health_score >= 90:
                health_label = "Excellent"
            elif health_score >= 80:
                health_label = "Good"
            elif health_score >= 60:
                health_label = "Fair"
            else:
                health_label = "Poor"

            # Create standardized dataset_health object with EXPLICIT conversions
            # Use float() to ensure no numpy types escape
            dataset_health = {
                "health_score": float(health_score),
                "health_label": str(health_label),
                "missing_ratio": float(round(missing_pct / 100, 4)),
                "duplicate_ratio": float(round(duplicate_pct / 100, 4)),
                "anomaly_ratio": float(round(anomaly_ratio, 4)),
                "completeness_ratio": float(round(1.0 - (missing_pct / 100), 4))
            }
            
            # Update p01_stats so valid value appears in report (legacy support)
            p01_stats["Health Score"] = health_score
            p01_stats["Health Label"] = health_label
            
        except Exception as e:
            print(f"Decyphr ⚠️: Health score calculation failed: {e}")
            dataset_health = {
                "health_score": None,
                "health_label": None,
                "missing_ratio": None,
                "duplicate_ratio": None,
                "anomaly_ratio": None,
                "completeness_ratio": None
            }
            # If calculation fails, ensure consistent "N/A" state
            p01_stats["Health Score"] = None  # None triggers "Not Available" in template
            p01_stats["Health Label"] = None  # Explicitly None to trigger hiding in template


        # --- 4. Custom KPIs for Telco Demo ---
        churn_rate = "N/A"
        mtm_pct = "N/A"
        
        # Get column names from overview_results
        columns = list(overview_results.get("column_details", {}).keys())

        # Check if Churn column exists (case-insensitive)
        churn_col = next((c for c in columns if c.lower() == 'churn'), None)
        if churn_col:
             # Assuming 'Yes'/'No' or 1/0
             try:
                 churn_series = ddf[churn_col].compute()
                 churn_count = churn_series.apply(lambda x: 1 if str(x).lower() in ['yes', '1', 'true'] else 0).sum()
                 total_count = len(churn_series)
                 if total_count > 0:
                     churn_rate = (churn_count / total_count) * 100
                 else:
                     churn_rate = 0.0
             except Exception as e:
                 print(f"Warning: Could not calc churn rate: {e}")

        # Check for Contract column
        contract_col = next((c for c in columns if c.lower() == 'contract'), None)
        if contract_col:
            try:
                contract_series = ddf[contract_col].compute()
                mtm_count = contract_series.apply(lambda x: 1 if 'month' in str(x).lower() else 0).sum()
                total_count = len(contract_series)
                if total_count > 0:
                    mtm_pct = (mtm_count / total_count) * 100
                else:
                    mtm_pct = 0.0
            except Exception as e:
                print(f"Warning: Could not calc MTM pct: {e}")

        system_metrics = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "runtime_execution_time": round(time.time() - start_time, 2),
            "number_of_insights_generated": len(p17_results.get("insights", [])),
            "number_of_recommendations_generated": len(p18_results.get("recommendations", [])),
            "anomaly_count": anomaly_count,
            "top_feature_importance": top_feature, # Pass the extracted feature object/string
            "churn_rate": round(churn_rate, 1) if isinstance(churn_rate, float) else "N/A",
            "mtm_pct": round(mtm_pct, 1) if isinstance(mtm_pct, float) else "N/A",
            "dataset_statistics": p01_stats,
            "dataset_health": dataset_health
        }

        # Store in analysis_results for builder to use (CRITICAL: Do this before potential JSON errors)
        analysis_results["system_metrics"] = system_metrics

        # Export to JSON
        json_output_dir = "Reports"
        os.makedirs(json_output_dir, exist_ok=True)
        json_filename = f"metrics_{int(time.time())}.json"
        json_path = os.path.join(json_output_dir, json_filename)
        
        # Helper for JSON serialization of numpy types
        class NpEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, np.integer):
                    return int(obj)
                if isinstance(obj, np.floating):
                    return float(obj)
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                return super(NpEncoder, self).default(obj)

        with open(json_path, 'w') as f:
            json.dump(system_metrics, f, cls=NpEncoder, indent=4)
        print(f"Decyphr 📊: System metrics saved to {json_path}")

    except Exception as e:
        print(f"Decyphr ⚠️: Failed to collect or save system metrics: {e}")
        # Even if metrics collection failed, try to pass whatever we have or an empty dict
        if "system_metrics" not in analysis_results:
             analysis_results["system_metrics"] = {
                 "dataset_statistics": p01_stats,
                 "dataset_health": {
                    "health_score": None, "health_label": None, 
                    "missing_ratio": None, "duplicate_ratio": None, 
                    "anomaly_ratio": None, "completeness_ratio": None
                 }
             }


    from decyphr import __version__ as decyphr_version
    
    output_dir = "Reports"
    # CORRECTED: Use exist_ok=True to prevent errors or nested directories
    # if the 'Reports' folder already exists in the current working directory.
    os.makedirs(output_dir, exist_ok=True)
    
    report_num = 1
    while os.path.exists(os.path.join(output_dir, f"Report_{report_num}.html")):
        report_num += 1
    report_path = os.path.join(output_dir, f"Report_{report_num}.html")

    build_html_report(
        ddf=ddf,
        all_analysis_results=analysis_results,
        output_path=report_path,
        decyphr_version=decyphr_version,
        dataset_name=os.path.basename(filepath)
    )
    
    return report_path
