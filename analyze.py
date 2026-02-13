# ==============================================================================
# FILE: analyze.py
# PURPOSE: This is an example script demonstrating how to use the 'decyphr'
#          library to generate a comprehensive EDA report.
# LOCATION: Place this file in the root of your 'decyphr_project/' directory.
# ==============================================================================

# --- Step 1: Import the Required Libraries ---
import sys
import os

print("DEBUG: Starting analyze.py...", flush=True)

# Ensure we use the local version of the code
sys.path.insert(0, os.path.abspath("3_Source_Code"))

import decyphr
import pandas as pd
import numpy as np  # <-- CORRECTED: Import numpy directly


def create_sample_dataset(filepath="sample_data.csv"):
    """
    Creates a rich, sample dataset to showcase decyphr's capabilities.
    This function is for demonstration purposes only.
    """
    print("Creating a sample dataset to analyze...")
    data = {
        'user_id': [f'user_{i}' for i in range(500)],
        'age': [int(x) for x in np.random.normal(35, 10, 500)],
        'country': np.random.choice(['USA', 'Canada', 'UK', 'Australia'], 500, p=[0.5, 0.2, 0.2, 0.1]),
        'subscription_tier': np.random.choice(['Free', 'Premium', 'Basic'], 500, p=[0.6, 0.3, 0.1]),
        'monthly_spend': [max(0, x) for x in np.random.normal(50, 25, 500)],
        'last_login_date': pd.to_datetime(np.random.randint(1672531200, 1704067200, 500), unit='s'),
        'satisfaction_score': [int(x) for x in np.random.uniform(1, 6, 500)],
        'feedback_text': [
            "Amazing service, loved it!", "Could be better.", "The UI is a bit confusing.",
            "Best product in the market.", "I found a bug on the checkout page.",
            "Customer support was very helpful.", "It's okay for the price.",
            "I will definitely renew my subscription.", "The new feature is fantastic!",
            "Had some issues with payment processing."
        ] * 50,
        'churned': np.random.choice([0, 1], 500, p=[0.8, 0.2]),
        'latitude': [x for x in np.random.uniform(25, 50, 500)],
        'longitude': [x for x in np.random.uniform(-125, -65, 500)],
        'static_column': ['constant_value'] * 500,
    }
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)
    print(f"Sample dataset saved to '{filepath}'")
    return filepath

def main():
    """
    Main function to run the decyphr analysis.
    """
    sample_filepath = create_sample_dataset()

    print("\n" + "="*80)
    print(" " * 20 + "RUNNING DECYPHR ANALYSIS")
    print("="*80 + "\n")

    try:
        # Option 3: Telco Customer Churn Demo
        print("Decyphr 🚀: Running Telco Customer Churn Demo...")
        decyphr.analyze(
            filepath="telco_customer_churn.csv",
            target="Churn"
        )

    except Exception as e:
        print(f"An error occurred while running the decyphr analysis: {e}")

    finally:
        if os.path.exists(sample_filepath):
            # os.remove(sample_filepath) # You can uncomment this to auto-delete the sample file
            pass

if __name__ == "__main__":
    main()