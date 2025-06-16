# ==============================================================================
# FILE: 4_Testing/test_suite.py
# ==============================================================================
# PURPOSE: This file contains the automated tests for the decyphr library.
#          It uses the pytest framework to verify functionality.

import os
import pytest
import pandas as pd
import numpy as np

# Import the main function from the library we are testing
import decyphr

# --- Test Fixtures ---
# Fixtures are functions that provide a fixed baseline state for tests.
# This fixture creates a temporary, valid dataset for our tests to use.
@pytest.fixture(scope="module")
def sample_test_data_path():
    """
    Creates a temporary sample CSV file for testing and yields its path.
    Deletes the file after tests in the module are complete.
    """
    filepath = "temp_test_data.csv"
    data = {
        'numeric_col': np.random.randn(100),
        'categorical_col': np.random.choice(['A', 'B', 'C'], 100),
        'date_col': pd.to_datetime(pd.date_range(start='2023-01-01', periods=100, freq='D'))
    }
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)
    
    # 'yield' provides the data to the test function
    yield filepath
    
    # This code runs after the test has finished, cleaning up the file
    print(f"\nCleaning up test file: {filepath}")
    os.remove(filepath)
    # Clean up the generated report as well
    if os.path.exists("Reports/Report_1.html"):
        os.remove("Reports/Report_1.html")
    if os.path.exists("Reports"):
        # Check if directory is empty before removing
        if not os.listdir("Reports"):
            os.rmdir("Reports")


# --- Test Functions ---
# Each function starting with 'test_' is a separate test case.

def test_analyze_function_runs_without_error(sample_test_data_path):
    """
    Tests if the main `decyphr.analyze` function runs to completion without
    raising an exception on a valid, simple dataset.
    """
    print(f"Running test_analyze_function_runs_without_error on {sample_test_data_path}...")
    try:
        decyphr.analyze(filepath=sample_test_data_path)
    except Exception as e:
        pytest.fail(f"decyphr.analyze() raised an unexpected exception: {e}")


def test_report_file_is_created(sample_test_data_path):
    """
    Tests if calling `decyphr.analyze` successfully creates an HTML report
    in the expected directory.
    """
    print(f"Running test_report_file_is_created on {sample_test_data_path}...")
    
    # Run the analysis
    report_path = decyphr.run_analysis_pipeline(filepath=sample_test_data_path)
    
    # Assert that the report path is not None and the file exists
    assert report_path is not None, "The analysis pipeline did not return a report path."
    assert os.path.exists(report_path), f"The report file was not created at the expected path: {report_path}"