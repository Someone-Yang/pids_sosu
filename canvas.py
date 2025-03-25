import tkinter as tk
import math

def draw_gradient_ball(targetCanvas:tk.Canvas ,x, y, radius, start_color, end_color, steps, tags = "normal"):
  for i in range(steps):
    ratio = i / steps
    r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
    g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
    b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
    color = f"#{r:02x}{g:02x}{b:02x}"
    current_radius = radius * (1 - ratio * 0.5)
    targetCanvas.create_oval(
        x - current_radius, y - current_radius,
        x + current_radius, y + current_radius,
        fill=color, outline=color, tags=tags
    )

def draw_arrow(targetCanvas:tk.Canvas, x, y, color, tags = "normal"):
    targetCanvas.create_polygon(
        (x,y),(x-8,y+16),(x+8,y+16),(x+16,y),(x+8,y-16),(x-8,y-16),
        fill=color, outline="#888888", width=2, tags=tags
)
    
