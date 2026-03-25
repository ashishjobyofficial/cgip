"""
Sun & Cloud Animation
=====================
Computer Graphics Algorithms Used
----------------------------------
1. MIDPOINT CIRCLE ALGORITHM (Bresenham's Circle)
   - Used to rasterise every circle in the scene pixel-by-pixel using
     integer arithmetic and 8-way symmetry.
  
2. 2-D TRANSLATION
   - Every moving object (sun, clouds) is repositioned each frame by
     adding a displacement vector (tx, 0) to its centre coordinates:
         x' = x + tx
     This is the standard 2-D translation transformation.
   """

import tkinter as tk


class SunAnimation:
    def __init__(self, root):
        self.root = root
        self.root.title("Sun & Cloud Animation — Translation + Circle Algorithm")

        # Canvas (sky)
        self.canvas = tk.Canvas(root, width=800, height=400, bg="sky blue")
        self.canvas.pack()

        # Static ground — drawn once, never erased
        self.canvas.create_rectangle(0, 300, 800, 400, fill="green", outline="")

        # ── Sun state ──────────────────────────────────────────────────────────
        self.sun_x  = 50      # current centre-x (translated each frame)
        self.sun_y  = 110     # fixed centre-y
        self.sun_r  = 30      # radius
        self.sun_tx = 1.5     # translation step per frame (px)

        # ── Cloud state ────────────────────────────────────────────────────────
        # Each cloud is a list of circle specs relative to the cloud anchor.
        # Format per cloud dict:
        #   x, y    : anchor position (translated each frame)
        #   tx      : translation speed (px per frame)
        #   circles : list of (offset_x, offset_y, radius)
        self.clouds = [
            {
                "x": 200, "y": 65, "tx": 1.2,
                "circles": [(0, 0, 28), (-24, 8, 20), (24, 10, 18), (0, 16, 22)]
            },
            {
                "x": 460, "y": 80, "tx": 0.8,
                "circles": [(0, 0, 24), (-20, 8, 17), (20, 9, 15), (0, 14, 19)]
            },
            {
                "x": 650, "y": 55, "tx": 1.5,
                "circles": [(0, 0, 32), (-27, 9, 22), (26, 11, 20), (0, 18, 25)]
            },
            {
                "x": 110, "y": 145, "tx": 1.0,
                "circles": [(0, 0, 20), (-17, 6, 14), (17, 7, 13), (0, 11, 16)]
            },
            {
                "x": 570, "y": 135, "tx": 0.6,
                "circles": [(0, 0, 26), (-22, 8, 18), (22, 9, 16), (0, 15, 20)]
            },
        ]

        self.animate()

    # ── Midpoint Circle Algorithm ──────────────────────────────────────────────

    def _plot_8(self, h, k, x, y, color, tag):
        """
        Plot the 8 symmetric pixel positions from one octant computation.
        8-way symmetry: one (x,y) pair yields 8 boundary points.

        Reference: Foley et al., §3.3; Hearn & Baker, §3-9.
        """
        for px, py in [
            (h+x, k+y), (h-x, k+y), (h+x, k-y), (h-x, k-y),
            (h+y, k+x), (h-y, k+x), (h+y, k-x), (h-y, k-x),
        ]:
            self.canvas.create_rectangle(px, py, px+1, py+1,
                                         fill=color, outline="", tags=tag)

    def draw_circle(self, h, k, r, color, tag):
        """
        Midpoint Circle Algorithm (outline).
        Uses integer incremental arithmetic — no floating-point trig.

        Decision parameter:  p = 1 - r
          if p < 0  →  p += 2x + 3           (East step)
          else      →  p += 2(x - y) + 5     (South-East step, y--)

        Reference: Foley, van Dam, Feiner & Hughes,
        "Computer Graphics: Principles and Practice", 2nd ed., §3.3.
        """
        x, y = 0, r
        p = 1 - r
        self._plot_8(h, k, x, y, color, tag)
        while x < y:
            x += 1
            if p < 0:
                p += 2 * x + 1
            else:
                y -= 1
                p += 2 * (x - y) + 1
            self._plot_8(h, k, x, y, color, tag)

    def draw_filled_circle(self, h, k, r, color, tag):
        """
        Filled circle via scan-line spans derived from the Midpoint Circle
        Algorithm: horizontal lines are drawn between the left and right
        boundary points computed at each step, filling the disc.

        Reference: same as draw_circle() above.
        """
        x, y = 0, r
        p = 1 - r
        self.canvas.create_line(h-y, k, h+y, k, fill=color, tags=tag)
        while x < y:
            x += 1
            if p < 0:
                p += 2 * x + 1
            else:
                y -= 1
                p += 2 * (x - y) + 1
            self.canvas.create_line(h-x, k+y, h+x, k+y, fill=color, tags=tag)
            self.canvas.create_line(h-x, k-y, h+x, k-y, fill=color, tags=tag)
            self.canvas.create_line(h-y, k+x, h+y, k+x, fill=color, tags=tag)
            self.canvas.create_line(h-y, k-x, h+y, k-x, fill=color, tags=tag)

    # ── 2-D Translation ────────────────────────────────────────────────────────

    def translate(self, obj, tx):
        """
        Apply 2-D translation:  x' = x + tx

        In homogeneous matrix form:
            | 1  0  tx |   | x |   | x + tx |
            | 0  1   0 | × | y | = |   y    |
            | 0  0   1 |   | 1 |   |   1    |

       
        """
        obj["x"] += tx

    # ── Main animation loop ────────────────────────────────────────────────────

    def animate(self):
        # Clear all animated objects
        self.canvas.delete("sun")
        self.canvas.delete("cloud")

        # ── SUN: translate then draw with Midpoint Circle Algorithm ───────────
        self.sun_x += self.sun_tx          # 2-D Translation: x' = x + tx
        if self.sun_x > 860:
            self.sun_x = -60

        sx = int(self.sun_x)
        # Glow ring (outline circle)
        self.draw_circle(sx, self.sun_y, self.sun_r + 8, "orange", "sun")
        # Solid sun disc (filled circle)
        self.draw_filled_circle(sx, self.sun_y, self.sun_r, "yellow", "sun")
        # Bright inner highlight
        self.draw_filled_circle(sx, self.sun_y, self.sun_r // 3, "lightyellow", "sun")

        # ── CLOUDS: translate then draw each puff with Midpoint Circle Algo ───
        for cloud in self.clouds:
            self.translate(cloud, cloud["tx"])   # 2-D Translation
            if cloud["x"] > 900:
                cloud["x"] = -100

            cx, cy = int(cloud["x"]), cloud["y"]
            for (ox, oy, r) in cloud["circles"]:
                self.draw_filled_circle(cx+ox, cy+oy, r, "white", "cloud")
            for (ox, oy, r) in cloud["circles"]:
                self.draw_circle(cx+ox, cy+oy, r, "white", "cloud")

        # Loop at ~30 fps
        self.root.after(33, self.animate)


if __name__ == "__main__":
    root = tk.Tk()
    app = SunAnimation(root)
    root.mainloop()
