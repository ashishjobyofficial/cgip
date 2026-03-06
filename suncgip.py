import tkinter as tk
import math

class SunAnimation:
    def __init__(self, root):
        self.root = root
        self.root.title("Sun Animation with Ground Layer")
        
        # 1. Setup Canvas (Sky)
        self.canvas = tk.Canvas(root, width=800, height=400, bg="sky blue")
        self.canvas.pack()
        
        # 2. Draw the Static Ground (This stays at the bottom)
        # Coordinates: (x_start, y_start, x_end, y_end)
        self.canvas.create_rectangle(0, 300, 800, 400, fill="green", outline="")
        
        # 3. Initial State of Sun
        self.sun_x = 50
        self.sun_y = 100
        self.radius = 30
        self.dx = 5
        self.ray_length = 60
        
        # Start Animation
        self.animate()

    def draw_circle_midpoint(self, h, k, r):
        """Standard Midpoint Circle Algorithm"""
        x = 0
        y = r
        p = 1 - r
        self.plot_points(h, k, x, y)
        while x < y:
            x += 1
            if p < 0:
                p = p + 2 * x + 1
            else:
                y -= 1
                p = p + 2 * (x - y) + 1
            self.plot_points(h, k, x, y)

    def plot_points(self, h, k, x, y):
        """Plots the pixels for the sun core"""
        points = [
            (h+x, k+y), (h-x, k+y), (h+x, k-y), (h-x, k-y),
            (h+y, k+x), (h-y, k+x), (h+y, k-x), (h-y, k-x)
        ]
        for px, py in points:
            self.canvas.create_rectangle(px, py, px, py, outline="yellow", tags="sun")

    def draw_rays(self, h, k):
        """Draws yellow rays around the sun"""
        num_rays = 12
        for i in range(num_rays):
            angle = math.radians(i * (360 / num_rays))
            x_start = h + (self.radius + 5) * math.cos(angle)
            y_start = k + (self.radius + 5) * math.sin(angle)
            x_end = h + self.ray_length * math.cos(angle)
            y_end = k + self.ray_length * math.sin(angle)
            
            self.canvas.create_line(x_start, y_start, x_end, y_end, fill="yellow", width=2, tags="sun")

    def animate(self):
        # 1. Clear only the sun (tags="sun"), leaves the green ground alone
        self.canvas.delete("sun")
        
        # 2. Update Position
        self.sun_x += self.dx
        if self.sun_x > 850:
            self.sun_x = -50
            
        # 3. Draw the rays and the circle at new translated coordinates
        self.draw_rays(self.sun_x, self.sun_y)
        self.draw_circle_midpoint(self.sun_x, self.sun_y, self.radius)
        
        # 4. Loop
        self.root.after(33, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = SunAnimation(root)
    root.mainloop()
