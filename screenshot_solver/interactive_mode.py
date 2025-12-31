import os
import sys
import platform
import subprocess
from main import ScreenshotSolver

def take_screenshot_interactive(save_path: str):
    """
    Takes an interactive screenshot.
    On macOS: Uses 'screencapture -i' to let user select a region.
    On others: Takes full screenshot (fallback).
    """
    system = platform.system()
    
    if system == "Darwin":
        print("Please select the region on your screen to capture...")
        # -i: interactive, -x: no sound
        ret = os.system(f"screencapture -i -x {save_path}")
        if ret != 0:
            print("Screenshot cancelled or failed.")
            return False
        return True
    else:
        # Fallback for Windows/Linux (Full screen or requires other tools)
        try:
            import pyautogui
            print("Taking full screen screenshot in 3 seconds...")
            import time
            time.sleep(3)
            screenshot = pyautogui.screenshot()
            screenshot.save(save_path)
            return True
        except ImportError:
            print("pyautogui not installed. Cannot take screenshot.")
            return False

def main():
    temp_path = "temp_screenshot.png"
    
    # Clean up previous
    if os.path.exists(temp_path):
        os.remove(temp_path)
        
    if take_screenshot_interactive(temp_path):
        if os.path.exists(temp_path):
            solver = ScreenshotSolver()
            solver.run_from_file(temp_path)
            
            # Optional: Clean up
            # os.remove(temp_path)
        else:
            print("Screenshot file was not created.")

if __name__ == "__main__":
    main()
