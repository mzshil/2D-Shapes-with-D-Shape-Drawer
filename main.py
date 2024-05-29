import tkinter as tk
import tkinter.ttk as ttk
import json
from tkinter import messagebox

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.display_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def display_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack(ipadx=1)

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("2D Shape Drawer - Michelle Arnado")
        self.root.geometry("800x600")
        
        # Canvas for drawing shapes
        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Frame for shape selection
        shape_frame = tk.Frame(self.root)
        shape_frame.pack(pady=5, padx=10, fill=tk.X)
        tk.Label(shape_frame, text="Select Shape:").pack(side=tk.LEFT)
        self.shape_var = tk.StringVar()
        self.shape_var.set("Point")  # Set default shape to "Point"
        self.shape_dropdown = ttk.OptionMenu(shape_frame, self.shape_var, "Point", "Point", "Line", "Circle", "Rectangle")
        self.shape_dropdown.pack(side=tk.LEFT)
        ToolTip(self.shape_dropdown, "Select a shape.")

        # Frame for color selection
        color_frame = tk.Frame(self.root)
        color_frame.pack(pady=5, padx=10, fill=tk.X)
        tk.Label(color_frame, text="Select Color:").pack(side=tk.LEFT)
        self.color_var = tk.StringVar()
        self.color_var.set("Black")  # Set default color to "Black"
        self.color_dropdown = ttk.OptionMenu(color_frame, self.color_var, "Black", "Black", "Red", "Green", "Blue")
        self.color_dropdown.pack(side=tk.LEFT)
        ToolTip(self.color_dropdown, "Select a color.")

        # Buttons for actions
        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(pady=5, padx=10, fill=tk.X)
        self.draw_button = tk.Button(buttons_frame, text="Draw", command=self.draw_shape)
        self.draw_button.pack(side=tk.RIGHT, padx=5)
        ToolTip(self.draw_button, "Draw the selected shape")

        self.clear_button = tk.Button(buttons_frame, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(side=tk.RIGHT, padx=5)
        ToolTip(self.clear_button, "Clear the canvas")

        # Binding mouse events
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)
        
        # Variables
        self.current_shape = None
        self.start_x = None
        self.start_y = None

    def start_draw(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def draw(self, event):
        if self.current_shape:
            self.canvas.delete(self.current_shape)
        
        shape = self.shape_var.get()
        color = self.color_var.get()
        
        if shape == "Line":
            self.current_shape = self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=color)
        elif shape == "Circle":
            self.current_shape = self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, outline=color)
        elif shape == "Rectangle":
            self.current_shape = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=color)
        elif shape == "Point":
            x, y = event.x, event.y
            point = self.canvas.create_oval(x-2, y-2, x+2, y+2, fill=color)

    def stop_draw(self, event):
        self.current_shape = None
    
    def clear_canvas(self):
        self.canvas.delete("all")

    def draw_shape(self):
        shape = self.shape_var.get()
        color = self.color_var.get()
        
        if shape == "Line":
            self.canvas.create_line(10, 10, 200, 200, fill=color)
        elif shape == "Circle":
            self.canvas.create_oval(100, 100, 300, 300, outline=color)
        elif shape == "Rectangle":
            self.canvas.create_rectangle(50, 50, 250, 150, outline=color)

    def save_shapes(self):
        shapes = []
        for item in self.canvas.find_all():
            shape_info = self.canvas.coords(item), self.canvas.itemcget(item, 'fill'), self.canvas.itemcget(item, 'outline'), self.canvas.type(item)
            shapes.append(shape_info)
        try:
            with open("saved_shapes.json", "w") as file:
                json.dump(shapes, file)
                messagebox.showinfo("Success", "Shapes saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving shapes: {str(e)}")

    def load_shapes(self):
        try:
            self.clear_canvas()
            with open("saved_shapes.json", "r") as file:
                shapes = json.load(file)
            for shape_info in shapes:
                if shape_info[3] == "line":
                    self.canvas.create_line(shape_info[0], fill=shape_info[1])
                elif shape_info[3] == "oval":
                    self.canvas.create_oval(shape_info[0], outline=shape_info[2])
                elif shape_info[3] == "rectangle":
                    self.canvas.create_rectangle(shape_info[0], outline=shape_info[2])
            messagebox.showinfo("Success", "Shapes loaded successfully!")
        except FileNotFoundError:
            messagebox.showerror("Error", "No saved shapes found!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading shapes: {str(e)}")

root = tk.Tk()
app = DrawingApp(root)

# Menubar
menubar = tk.Menu(root)
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Save", command=app.save_shapes)
file_menu.add_command(label="Load", command=app.load_shapes)
menubar.add_cascade(label="File", menu=file_menu)
root.config(menu=menubar)

root.mainloop()
