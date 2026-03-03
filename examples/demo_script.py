import sys
import os

# Ensure the local decyphr package is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import decyphr

def main():
    print("🚀 Starting Decyphr Analysis...")
    
    # Analyze the sample dataset
    dataset_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_dataset.csv')
    
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset not found at {dataset_path}")
        return

    try:
        decyphr.analyze(dataset_path)
        print("✅ Analysis completed successfully. Check the generated HTML report.")
    except Exception as e:
        print(f"❌ An error occurred during analysis: {e}")

if __name__ == "__main__":
    main()