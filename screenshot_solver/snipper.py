import tkinter as tk
import sys

class Snipper:
    def __init__(self):
        self.root = tk.Tk()
        # Remove fullscreen to avoid creating a new Space (which looks black)
        # self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        
        # Use overrideredirect to remove title bar and keep it on current desktop
        self.root.overrideredirect(True)
        
        # Manually set geometry to cover the whole screen
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+0+0")
        
        # Transparent background for macOS
        # 'systemTransparent' makes the window background fully transparent
        # so the user sees their desktop clearly without dimming.
        self.root.wm_attributes("-transparent", True)
        self.root.config(bg='systemTransparent')

        # Canvas for drawing selection
        # bg='systemTransparent' ensures the canvas doesn't block the view
        self.canvas = tk.Canvas(self.root, bg='systemTransparent', highlightthickness=0, cursor="crosshair")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.start_x = None
        self.start_y = None
        self.rect_id = None

        # Bind events
        self.canvas.bind('<Button-1>', self.on_mouse_down)
        self.canvas.bind('<B1-Motion>', self.on_mouse_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_up)
        
        # Escape to cancel
        self.root.bind('<Escape>', self.exit_app)

    def on_mouse_down(self, event):
        self.start_x = event.x
        self.start_y = event.y
        # Draw a rectangle. 
        # Thinnest line (width=1), Light Gray to simulate 90% transparency, Dashed
        self.rect_id = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y, 
            outline='#d9d9d9', width=1, dash=(3, 3)
        )

    def on_mouse_drag(self, event):
        if self.rect_id:
            self.canvas.coords(self.rect_id, self.start_x, self.start_y, event.x, event.y)

    def on_mouse_up(self, event):
        if self.start_x is None:
            self.exit_app()
            return
            
        x1 = min(self.start_x, event.x)
        y1 = min(self.start_y, event.y)
        x2 = max(self.start_x, event.x)
        y2 = max(self.start_y, event.y)
        
        width = x2 - x1
        height = y2 - y1
        
        # Only print if valid area
        if width > 5 and height > 5:
            # Print coordinates for the caller to capture
            # Format: x,y,w,h
            print(f"{x1},{y1},{width},{height}")
            
        self.root.destroy()

    def exit_app(self, event=None):
        self.root.destroy()
        sys.exit(1) # Exit with error code to indicate cancellation

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    Snipper().run()
