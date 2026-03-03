# Decyphr
**Structured Business Decision Intelligence Framework**

Decyphr is an AI-driven Business Decision Intelligence System that bridges the analytics-to-decision gap by transforming statistical outputs into structured, confidence-weighted managerial recommendations.

## Problem Statement

Traditional BI systems produce descriptive dashboards but fail to generate structured, prescriptive, and confidence-backed managerial actions.

Decyphr solves this by integrating:

*   Statistical modeling
*   Explainable AI (XAI)
*   Rule-based decision mapping
*   Confidence scoring
*   Impact prioritization

## System Architecture

**Pipeline:**

Data Ingestion $\rightarrow$ Statistical Modeling $\rightarrow$ Insight Generation $\rightarrow$ Decision Engine $\rightarrow$ Confidence & Impact Scoring $\rightarrow$ Executive Output

## Key Features

*   Automated feature importance extraction
*   K-Means based segmentation
*   IQR & Isolation Forest anomaly detection
*   Correlation & hypothesis testing
*   Confidence scoring (0–1 scale)
*   Structured executive summaries
*   Prescriptive recommendations

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
import decyphr
decyphr.analyze("data/sample_dataset.csv")
```

## Reproducibility

All experiments were conducted using deterministic seeds (`random_state = 42`).

## Academic Context

Developed as part of the MSc Data Science & Management Capstone Project  
Indian Institute of Technology Ropar  
Indian Institute of Management Amritsar  

**Mentor**: Dr. Aswathy Asokan Ajitha

## License

MIT License