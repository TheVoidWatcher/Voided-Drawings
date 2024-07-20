import tkinter as tk
from tkinter import colorchooser, simpledialog, filedialog, messagebox

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Drawing App")

        self.pen_color = "black"
        self.pen_width = 2
        self.tool = "pen"  # "pen", "eraser", "line", "rectangle", "circle"
        self.start_x = None
        self.start_y = None
        self.selected_shape = None
        self.shapes = []  # to store created shapes for undo/redo

        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Create buttons
        self.pen_btn = tk.Button(root, text="Pen", command=lambda: self.set_tool("pen"))
        self.pen_btn.pack(side=tk.LEFT, padx=5, pady=10)

        self.eraser_btn = tk.Button(root, text="Eraser", command=lambda: self.set_tool("eraser"))
        self.eraser_btn.pack(side=tk.LEFT, padx=5, pady=10)

        self.line_btn = tk.Button(root, text="Line", command=lambda: self.set_tool("line"))
        self.line_btn.pack(side=tk.LEFT, padx=5, pady=10)

        self.rectangle_btn = tk.Button(root, text="Rectangle", command=lambda: self.set_tool("rectangle"))
        self.rectangle_btn.pack(side=tk.LEFT, padx=5, pady=10)

        self.circle_btn = tk.Button(root, text="Circle", command=lambda: self.set_tool("circle"))
        self.circle_btn.pack(side=tk.LEFT, padx=5, pady=10)

        self.color_btn = tk.Button(root, text="Color", command=self.choose_color)
        self.color_btn.pack(side=tk.LEFT, padx=5, pady=10)

        self.thickness_btn = tk.Button(root, text="Thickness", command=self.choose_thickness)
        self.thickness_btn.pack(side=tk.LEFT, padx=5, pady=10)

        self.save_btn = tk.Button(root, text="Save", command=self.save_drawing)
        self.save_btn.pack(side=tk.LEFT, padx=5, pady=10)

        self.load_btn = tk.Button(root, text="Load", command=self.load_drawing)
        self.load_btn.pack(side=tk.LEFT, padx=5, pady=10)

        self.clear_btn = tk.Button(root, text="Clear", command=self.clear_canvas)
        self.clear_btn.pack(side=tk.LEFT, padx=5, pady=10)

        self.undo_btn = tk.Button(root, text="Undo", command=self.undo)
        self.undo_btn.pack(side=tk.LEFT, padx=5, pady=10)

        self.redo_btn = tk.Button(root, text="Redo", command=self.redo)
        self.redo_btn.pack(side=tk.LEFT, padx=5, pady=10)

        # Bindings
        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)
        self.canvas.bind("<ButtonPress-3>", self.select_shape)

    def set_tool(self, tool):
        self.tool = tool

    def start_draw(self, event):
        self.start_x = event.x
        self.start_y = event.y

        if self.tool == "line":
            self.selected_shape = self.canvas.create_line(self.start_x, self.start_y, self.start_x, self.start_y,
                                                          fill=self.pen_color, width=self.pen_width)
        elif self.tool == "rectangle":
            self.selected_shape = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y,
                                                               outline=self.pen_color, width=self.pen_width)
        elif self.tool == "circle":
            self.selected_shape = self.canvas.create_oval(self.start_x, self.start_y, self.start_x, self.start_y,
                                                          outline=self.pen_color, width=self.pen_width)

    def draw(self, event):
        if self.tool in ["pen", "eraser"]:
            if self.tool == "pen":
                self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.pen_color, width=self.pen_width)
            elif self.tool == "eraser":
                self.canvas.create_rectangle(event.x - self.pen_width, event.y - self.pen_width,
                                             event.x + self.pen_width, event.y + self.pen_width,
                                             fill="white", outline="white")

            self.start_x = event.x
            self.start_y = event.y

        elif self.tool in ["line", "rectangle", "circle"] and self.selected_shape:
            if self.tool == "line":
                self.canvas.coords(self.selected_shape, self.start_x, self.start_y, event.x, event.y)
            elif self.tool == "rectangle":
                self.canvas.coords(self.selected_shape, self.start_x, self.start_y, event.x, event.y)
            elif self.tool == "circle":
                self.canvas.coords(self.selected_shape, self.start_x, self.start_y, event.x, event.y)

    def end_draw(self, event):
        if self.selected_shape:
            self.shapes.append((self.tool, self.selected_shape))
            self.selected_shape = None

    def select_shape(self, event):
        if not self.shapes:
            return

        x, y = event.x, event.y
        item = self.canvas.find_closest(x, y)[0]

        if item in [shape[1] for shape in self.shapes]:
            self.selected_shape = item
            self.canvas.itemconfig(self.selected_shape, outline="red")

    def choose_color(self):
        self.pen_color = colorchooser.askcolor()[1]

    def choose_thickness(self):
        self.pen_width = simpledialog.askinteger("Pen Thickness", "Enter pen thickness (1-10):", minvalue=1, maxvalue=10)

    def save_drawing(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, "w") as f:
                    for tool, shape in self.shapes:
                        if tool == "pen":
                            f.write(f"pen {self.canvas.coords(shape)} {self.canvas.itemcget(shape, 'fill')} {self.canvas.itemcget(shape, 'width')}\n")
                        elif tool == "eraser":
                            f.write(f"eraser {self.canvas.coords(shape)}\n")
                        elif tool == "line":
                            f.write(f"line {self.canvas.coords(shape)} {self.canvas.itemcget(shape, 'fill')} {self.canvas.itemcget(shape, 'width')}\n")
                        elif tool == "rectangle":
                            f.write(f"rectangle {self.canvas.coords(shape)} {self.canvas.itemcget(shape, 'outline')} {self.canvas.itemcget(shape, 'width')}\n")
                        elif tool == "circle":
                            f.write(f"circle {self.canvas.coords(shape)} {self.canvas.itemcget(shape, 'outline')} {self.canvas.itemcget(shape, 'width')}\n")
                messagebox.showinfo("Save", "Drawing saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {e}")

    def load_drawing(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                self.clear_canvas()
                with open(file_path, "r") as f:
                    for line in f:
                        parts = line.split()
                        tool = parts[0]
                        coords = list(map(float, parts[1:5]))
                        if tool == "pen":
                            pen_color = parts[5]
                            pen_width = int(parts[6])
                            shape_id = self.canvas.create_line(coords, fill=pen_color, width=pen_width)
                            self.shapes.append(("pen", shape_id))
                        elif tool == "eraser":
                            shape_id = self.canvas.create_rectangle(coords, fill="white", outline="white")
                            self.shapes.append(("eraser", shape_id))
                        elif tool == "line":
                            line_color = parts[5]
                            line_width = int(parts[6])
                            shape_id = self.canvas.create_line(coords, fill=line_color, width=line_width)
                            self.shapes.append(("line", shape_id))
                        elif tool == "rectangle":
                            rect_outline = parts[5]
                            rect_width = int(parts[6])
                            shape_id = self.canvas.create_rectangle(coords, outline=rect_outline, width=rect_width)
                            self.shapes.append(("rectangle", shape_id))
                        elif tool == "circle":
                            circle_outline = parts[5]
                            circle_width = int(parts[6])
                            shape_id = self.canvas.create_oval(coords, outline=circle_outline, width=circle_width)
                            self.shapes.append(("circle", shape_id))
                messagebox.showinfo("Load", "Drawing loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load: {e}")

    def clear_canvas(self):
        self.canvas.delete("all")
        self.shapes = []

    def undo(self):
        if self.shapes:
            tool, shape_id = self.shapes.pop()
            self.canvas.delete(shape_id)

    def redo(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
