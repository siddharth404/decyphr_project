# Decyphr: AI-Driven Business Decision Intelligence System

## 1. Project Overview

**Decyphr** is an advanced, AI-driven decision intelligence system designed to bridge the gap between raw statistical analysis and actionable business strategy. Unlike traditional Exploratory Data Analysis (EDA) tools that simply visualize data, Decyphr autonomously interprets complex datasets, generating high-level business insights and strategic recommendations.

The system leverages a multi-stage pipeline to ingest structured data, perform rigorous statistical testing, and synthesize findings into a coherent "System Performance Dashboard." By converting technical metrics—such as correlation coefficients, anomaly scores, and feature importance—into plain-language business narratives, Decyphr empowers stakeholders to make data-informed decisions with confidence.

---

## 2. Key Features

Decyphr provides a comprehensive suite of analyses, intelligently triggered based on your data's characteristics:

*   **System Performance Dashboard**: A high-level executive summary featuring a proprietary **Dataset Health Score**, Key Performance Indicators (KPIs), and critical risk alerts.
*   **Deep Univariate Analysis**: Detailed statistical profiles, histograms, and frequency charts for every variable.
*   **Multivariate Analysis**: Interactive heatmaps for both linear (Pearson) and non-linear (Phik) correlations.
*   **Advanced Data Quality**: Automatically detects constant columns, whitespace issues, and potential outliers using multiple methods (IQR, Isolation Forest).
*   **Statistical Inference**: Performs automated Hypothesis Testing (T-Tests, ANOVA, Chi-Squared) to uncover statistically significant relationships.
*   **Machine Learning Insights**:
    *   **PCA**: Analyzes dimensionality reduction possibilities.
    *   **Clustering**: Automatically finds hidden segments in your data using K-Means (e.g., Customer Segmentation).
    *   **Feature Importance**: Trains a baseline model to identify the most predictive features.
    *   **Explainable AI (XAI)**: Generates SHAP summary plots to explain how features impact model predictions.
*   **Specialized Analysis**: dedicated modules for Deep Text Analysis (Sentiment, NER), Time-Series Decomposition, and Geospatial Mapping.
*   **Data Drift Detection**: Compare two datasets to quantify changes in data distribution over time.
*   **High-End Interactive Report**: A beautiful, modern HTML dashboard with a toggleable light/dark theme, responsive charts, and a professional UI/UX.

---

## 3. Quick Start & Demos

### Capabilities
Decyphr is optimized for performance, capable of processing distinct datasets with over 100,000 rows and 100,000 cells in under 3 minutes.

### Running the Telco Customer Churn Demo
Decyphr comes with a built-in demo for the Telco Customer Churn dataset, showcasing its ability to generate business insights, segment customers, and predict churn risks.

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/decyphr.git
    cd decyphr_project
    ```

2.  **Install Dependencies**:
    ```bash
    pip install .
    # Or install requirements directly
    pip install -r requirements.txt
    ```

3.  **Run the Demo**:
    Execute the provided analysis script to generate the report:
    ```bash
    python analyze.py
    ```
    *This will automatically load the synthetic Telco Churn dataset, run the full pipeline, and generate an interactive HTML report in the `Reports/` directory.*

4.  **View the Report**:
    Open the generated HTML file (e.g., `Reports/Report_telco_demo.html`) in your web browser.

---

## 4. Usage

To use Decyphr on your own data:

```python
import decyphr

# specific target for predictive analysis
decyphr.analyze(
    filepath="path/to/your_data.csv",
    target="Target_Column_Name" 
)

# Or for general EDA without a target
decyphr.analyze(filepath="path/to/your_data.csv")
```

---

## 5. Project Structure

This project uses a highly modular "plugin" architecture to ensure it is robust, maintainable, and easy to extend. All analysis and visualization logic is separated into self-contained modules located in the `src/decyphr/analysis_plugins/` directory.

## 6. Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated. Please feel free to fork the repo and create a pull request, or open an issue with suggestions.

## 7. License

Distributed under the MIT License. See LICENSE file for more information.

---
*Designed and Created by - Ayush Singh*