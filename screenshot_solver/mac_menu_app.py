import os
import sys
import threading
import subprocess
import tempfile
from main import ScreenshotSolver

# PyObjC Imports
try:
    from Foundation import NSObject
    from AppKit import NSApplication, NSStatusBar, NSMenu, NSMenuItem, NSVariableStatusItemLength, NSEvent
except ImportError:
    print("Error: PyObjC is not installed correctly.")
    print("Please run: pip install pyobjc")
    sys.exit(1)

# Initialize Solver
solver = ScreenshotSolver()

class ScreenshotApp(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        # Create the Status Item
        self.statusItem = NSStatusBar.systemStatusBar().statusItemWithLength_(NSVariableStatusItemLength)
        
        # Set the Icon (Text for now, or load image if available)
        # Using the magnifying glass emoji/text as requested
        self.statusItem.button().setTitle_("🔍")
        
        # Set the Action
        # We point it to our handler method
        self.statusItem.button().setAction_("handleIconClick:")
        self.statusItem.button().setTarget_(self)
        
        # CRITICAL: Allow Right Click to trigger the action
        # By default, NSButton only triggers on Left Mouse Up.
        # We need it to trigger on Right Mouse Up as well to show the menu.
        # sendActionOn: accepts a mask.
        # NSEventMaskLeftMouseUp (1 << 1) = 2
        # NSEventMaskRightMouseUp (1 << 3) = 8
        # Total = 10
        self.statusItem.button().sendActionOn_(10)
        
        # Pre-create the Quit menu
        self.quitMenu = NSMenu.alloc().init()
        # "terminate:" is the standard selector to quit the app
        quitItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Quit", "terminate:", "q")
        self.quitMenu.addItem_(quitItem)

    def handleIconClick_(self, sender):
        event = NSApplication.sharedApplication().currentEvent()
        # NSEventTypeRightMouseUp = 4
        # Control Key Mask = 262144 (for Ctrl+LeftClick = RightClick)
        
        is_right = (event.type() == 4) or ((event.modifierFlags() & 262144) != 0)
        
        if is_right:
            # Show the Quit Menu
            self.statusItem.popUpStatusItemMenu_(self.quitMenu)
        else:
            # Left Click -> Trigger Screenshot
            threading.Thread(target=self.process_screenshot).start()

    def process_screenshot(self):
        """
        Trigger the custom snipper tool and solve the question.
        """
        # Create a temporary file for the screenshot
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tf:
            screenshot_path = tf.name

        print(f"Temporary screenshot path: {screenshot_path}")

        # Use custom snipper to get coordinates
        snipper_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "snipper.py")
        try:
            result = subprocess.run(
                [sys.executable, snipper_script], 
                capture_output=True, 
                text=True
            )
            
            if result.returncode != 0:
                print("Snipping cancelled or failed.")
                return

            coords = result.stdout.strip()
            if not coords:
                print("No coordinates received.")
                return
                
            print(f"Coordinates received: {coords}")
            
            # Take screenshot of the selected area using system tool
            # -R x,y,w,h: capture rect
            # -x: silent
            # -r: no shadow (irrelevant for rect but good practice)
            # coords format from snipper is x,y,w,h
            ret = os.system(f"screencapture -R {coords} -x {screenshot_path}")
            
            if ret != 0 or not os.path.exists(screenshot_path):
                print("Screenshot capture failed.")
                return
                
        except Exception as e:
            print(f"Error during snipping: {e}")
            return

        print("Screenshot taken. Analyzing...")
        
        # Call solver to get the answer
        answer = solver.solve(screenshot_path)
        
        # Save answer to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix=".txt", delete=False, encoding='utf-8') as ans_file:
            ans_file.write(answer)
            ans_path = ans_file.name
            
        # Show result in the floating window
        display_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "display_result.py")
        subprocess.Popen([sys.executable, display_script, ans_path])
        
        # Clean up
        try:
            os.remove(screenshot_path)
        except:
            pass

if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    delegate = ScreenshotApp.alloc().init()
    app.setDelegate_(delegate)
    app.run()
