# Decyphr: AI-Driven Business Decision Intelligence System

## 1. Project Overview

**Decyphr** is an advanced, AI-driven decision intelligence system designed to bridge the gap between raw statistical analysis and actionable business strategy. Unlike traditional Exploratory Data Analysis (EDA) tools that simply visualize data, Decyphr autonomously interprets complex datasets, generating high-level business insights and strategic recommendations.

The system leverages a multi-stage pipeline to ingest structured data, perform rigorous statistical testing, and synthesize findings into a coherent "System Performance Dashboard." By converting technical metrics—such as correlation coefficients, anomaly scores, and feature importance—into plain-language business narratives, Decyphr empowers stakeholders to make data-informed decisions with confidence.

---

## 2. Key Features

Decyphr integrates a suite of advanced capabilities to deliver a holistic analysis experience:

*   **Automated EDA Pipeline**: autonomously executes a comprehensive battery of statistical tests, including univariate analysis, correlation mapping (Pearson/Phik), and hypothesis testing.
*   **Business Insight Generator**: Transforms abstract statistical patterns into clear, actionable business insights, detailing the "what" and "why" behind data trends.
*   **Decision Recommendation Engine**: Maps synthesized insights to concrete strategic actions, categorized by domain (e.g., Strategic, Operational, Marketing).
*   **Confidence Scoring**: Assigns a reliability score to every insight and recommendation based on data quality, sample size, and statistical significance, ensuring transparency.
*   **Business Impact Estimation**: Predicts the potential impact (High/Medium/Low) of implementing recommended actions, helping prioritize initiatives.
*   **Executive Summary Dashboard**: A high-level, interactive HTML report that presents the most critical findings at a glance, designed for C-level consumption.
*   **System Performance Evaluation**: Tracks the efficiency of the analysis pipeline itself, monitoring execution time and resource utilization.
*   **Dataset Health Monitoring**: continuously evaluates data quality through a proprietary "Health Score" (0-100), factoring in missingness, duplication, and anomaly ratios.

---

## 3. System Architecture

The Decyphr architecture is built upon a modular plugin system (`p01`–`p18`), ensuring extensibility and maintainability.

### Core Analysis Pipeline
*   **p01_overview**: Initial schema inference and dataset statistics.
*   **p02_univariate**: Distribution analysis for numeric and categorical variables.
*   **p03_data_quality**: Detection of constants, mixed types, and whitespace issues.
*   **p04_advanced_outliers**: IQR and Z-score based anomaly detection.
*   **p05_missing_values**: Nullity correlation and pattern analysis.
*   **p06_correlations**: Non-linear (Phik) and linear (Pearson) relationship mapping.

### Advanced Analytics
*   **p09_pca**: Dimensionality reduction for variance explanation.
*   **p10_clustering**: Unsupervised learning (K-Means/DBSCAN) for segmentation.
*   **p11_target_analysis**: Predictive power score (PPS) and feature importance relative to a target.
*   **p12_explainability_shap**: Model-agnostic explanations for driver analysis.

### Intelligence Layer
*   **p17_business_insights**: Synthesizes output from p01-p16 into narrative insights using heuristic logic.
*   **p18_decision_engine**: The apex module that derives final recommendations and calculates impact/confidence scores.

---

## 4. Installation

Decyphr requires Python 3.9+ and can be installed via pip (assuming local package availability) or by cloning the repository.

```bash
# Clone the repository
git clone https://github.com/your-org/decyphr.git
cd decyphr

# Install dependencies (including Dask, Plotly, Jinja2, Scikit-learn)
pip install -r requirements.txt

# detailed installation for development
pip install -e "."
```

---

## 5. Usage

Decyphr is designed for "one-line" execution. The primary entry point is the `analyze` function on the `main_orchestrator`.

```python
import decyphr

# Run the complete analysis pipeline
report_path = decyphr.analyze(
    filepath="data/customer_churn.csv",
    target="churned"  # Optional: Specify a target variable for supervised analysis
)

print(f"Analysis complete. Report generated at: {report_path}")
```

---

## 6. Example Outputs

Decyphr generates a rich HTML report containing interactive visualizations and text-based intelligence. Key outputs include:

### automated Insights
> "High correlation (φk = 0.82) detected between **Monthly Spend** and **Customer Lifetime Value**. This suggests that early monetization strategies are effectively compounding over time."

### Strategic Recommendations
> **Action**: Implement tiered loyalty rewards for high-spend cohorts.
> **Impact**: HIGH | **Confidence**: 92% (Robust statistical evidence)
> **Rationale**: Top-decile spenders show a 40% lower churn probability (p < 0.05).

### System Metrics
*   **Execution Time**: 2.01s (High-Performance Dask Backend)
*   **Dataset Health**: 99.9/100 (Label: **Good**)
*   **Anomalies Detected**: 1 (0.2% of dataset)

---

## 7. Research Motivation

The exponential growth of data availability has outpaced the human capacity for manual analysis. While statistical learning provides the tools to find patterns, bridging the "last mile" from pattern to decision remains a bottleneck.

**Decyphr** was motivated by the need for an automated **Decision Support System (DSS)** that does not merely present charts but "thinks" alongside the analyst. By encoding expert heuristics into a modular pipeline, Decyphr aims to standardize the quality of business analysis and democratize access to advanced data science techniques.

---

## 8. Technology Stack

*   **Language**: Python 3.10+
*   **Compute Engine**: Dask (Parallelized Dataframe functionality)
*   **Visualization**: Plotly (Interactive Web-GL charts)
*   **Machine Learning**: Scikit-learn, XGBoost, SHAP
*   **Statistical Analysis**: Phik, SciPy, Statsmodels
*   **Reporting**: Jinja2 Templating Engine, HTML5/CSS3 (Grid/Flexbox)