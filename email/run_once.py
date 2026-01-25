
import logging
import sys
import os

# Ensure the current directory is in the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import job

if __name__ == "__main__":
    # Configure logging for the single run
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )
    
    logging.info("Starting single run execution...")
    try:
        job()
        logging.info("Single run execution completed successfully.")
    except Exception as e:
        logging.error(f"Single run execution failed: {e}")
        sys.exit(1)
