import sys
import os
import shutil
import glob

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
        print("✅ Analysis completed successfully.")
        
        # Move generated report to home folder
        reports_dir = os.path.join(os.path.dirname(__file__), '..', 'Reports')
        if os.path.exists(reports_dir):
            reports = glob.glob(os.path.join(reports_dir, '*.html'))
            if reports:
                latest_report = max(reports, key=os.path.getctime)
                dest_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'demo_report.html'))
                shutil.copy2(latest_report, dest_path)
                print(f"📄 Demo report cleanly generated at: {dest_path}")
                
            shutil.rmtree(reports_dir)
            
    except Exception as e:
        print(f"❌ An error occurred during analysis: {e}")

if __name__ == "__main__":
    main()