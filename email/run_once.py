import sys
import os
import logging

# Ensure we can import from the current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import job

if __name__ == "__main__":
    print("Executing single run of Twitter Monitor...")
    # Trigger the job manually
    job()
    print("Execution complete.")
