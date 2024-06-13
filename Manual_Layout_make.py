import tkinter as tk
from math import sin, cos, pi

SCALE_FACTOR = 0.5  # Adjust the scale factor as needed

class Pallet:
    def __init__(self, canvas, lbh):
        self.canvas = canvas
        self.lbh = [dim * SCALE_FACTOR for dim in lbh]
        self.id = self.canvas.create_rectangle(10, 10, self.lbh[0] + 10, self.lbh[1] + 10, fill='gray')

class Box:
    box_counter = 0  # Class variable to keep track of box numbers

    def __init__(self, canvas, lbh, angle=0):
        self.canvas = canvas
        self.lbh = [dim * SCALE_FACTOR for dim in lbh]
        self.angle = angle
        Box.box_counter += 1
        self.box_number = Box.box_counter
        self.id = self.canvas.create_rectangle(0, 0, self.lbh[0], self.lbh[1], fill='blue')
        self.label_id = self.canvas.create_text(self.lbh[0] / 2, self.lbh[1] / 2, text=str(self.box_number), fill='white')
        self.bind_events()

    def bind_events(self):
        self.canvas.tag_bind(self.id, '<ButtonPress-1>', self.on_click)
        self.canvas.tag_bind(self.id, '<Double-Button-1>', self.on_double_click)
        self.canvas.tag_bind(self.id, '<ButtonRelease-1>', self.on_release)
        self.canvas.tag_bind(self.id, '<B1-Motion>', self.on_drag)

    def on_click(self, event):
        self.x = event.x
        self.y = event.y

    def on_double_click(self, event):
        self.toggle_color()

    def on_release(self, event):
        self.update_label_position()
        self.update_center_coordinates()

    def on_drag(self, event):
        dx = event.x - self.x
        dy = event.y - self.y
        self.canvas.move(self.id, dx, dy)
        self.canvas.move(self.label_id, dx, dy)
        self.x = event.x
        self.y = event.y

    def toggle_color(self):
        current_color = self.canvas.itemcget(self.id, 'fill')
        new_color = 'red' if current_color == 'blue' else 'blue'
        self.canvas.itemconfig(self.id, fill=new_color)

    def rotate(self, angle):
        if self.is_red_color():
            self.angle = angle
            coords = self.canvas.coords(self.id)
            if len(coords) == 4:  # Initial rectangle coordinates
                x1, y1, x2, y2 = coords
                w, h = self.lbh[0], self.lbh[1]
                cx = (x1 + x2) / 2
                cy = (y1 + y2) / 2
                self.canvas.delete(self.id)
                self.id = self.canvas.create_polygon(self.get_points(cx, cy, w, h, angle), fill='red')
            else:
                cx = sum(coords[::2]) / 4
                cy = sum(coords[1::2]) / 4
                self.canvas.coords(self.id, *self.get_points(cx, cy, self.lbh[0], self.lbh[1], angle))

            self.update_label_position()
            self.bind_events()  # Re-bind the events to the new polygon

    def is_red_color(self):
        return self.canvas.itemcget(self.id, 'fill') == 'red'

    def get_points(self, cx, cy, w, h, angle):
        points = []
        for x, y in [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)]:
            x_rot = cx + (x - cx) * cos(angle) - (y - cy) * sin(angle)
            y_rot = cy + (x - cx) * sin(angle) + (y - cy) * cos(angle)
            points.append(x_rot)
            points.append(y_rot)
        return points

    def update_label_position(self):
        coords = self.canvas.coords(self.id)
        if len(coords) == 4:
            x1, y1, x2, y2 = coords
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2
        else:
            cx = sum(coords[::2]) / 4
            cy = sum(coords[1::2]) / 4
        self.canvas.coords(self.label_id, cx, cy)

    def update_center_coordinates(self):
        coords = self.canvas.coords(self.id)
        if len(coords) == 4:
            x1, y1, x2, y2 = coords
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2
        else:
            cx = sum(coords[::2]) / 4
            cy = sum(coords[1::2]) / 4
        # Convert cx, cy to coordinates relative to the bottom left corner of the pallet
        cx -= 10
        cy = self.canvas.winfo_height() - cy - 10
        return self.box_number, cx, cy

class Application:
    def __init__(self, master):
        self.master = master
        self.master.title("Pallet and Box GUI")

        # Frames for organizing input fields
        self.pallet_frame = tk.Frame(self.master)
        self.pallet_frame.pack(pady=10)

        self.box_frame = tk.Frame(self.master)
        self.box_frame.pack(pady=10)

        self.rotation_frame = tk.Frame(self.master)
        self.rotation_frame.pack(pady=10)

        self.coordinates_frame = tk.Frame(self.master)
        self.coordinates_frame.pack(pady=10)

        # Canvas for drawing
        self.canvas = tk.Canvas(self.master, width=800, height=600)
        self.canvas.pack()

        # Input fields for pallet dimensions
        tk.Label(self.pallet_frame, text="Pallet Dimensions:").grid(row=0, column=0, padx=10, pady=5)
        self.pallet_length_entry = tk.Entry(self.pallet_frame, width=10)
        self.pallet_length_entry.grid(row=0, column=1, padx=10, pady=5)
        self.pallet_breadth_entry = tk.Entry(self.pallet_frame, width=10)
        self.pallet_breadth_entry.grid(row=0, column=2, padx=10, pady=5)
        self.pallet_height_entry = tk.Entry(self.pallet_frame, width=10)
        self.pallet_height_entry.grid(row=0, column=3, padx=10, pady=5)
        self.create_pallet_button = tk.Button(self.pallet_frame, text="Create Pallet", command=self.create_pallet)
        self.create_pallet_button.grid(row=0, column=4, padx=10, pady=5)

        # Input fields for box dimensions
        tk.Label(self.box_frame, text="Box Dimensions:").grid(row=0, column=0, padx=10, pady=5)
        self.box_length_entry = tk.Entry(self.box_frame, width=10)
        self.box_length_entry.grid(row=0, column=1, padx=10, pady=5)
        self.box_breadth_entry = tk.Entry(self.box_frame, width=10)
        self.box_breadth_entry.grid(row=0, column=2, padx=10, pady=5)
        self.box_height_entry = tk.Entry(self.box_frame, width=10)
        self.box_height_entry.grid(row=0, column=3, padx=10, pady=5)
        self.create_box_button = tk.Button(self.box_frame, text="Create Box", command=self.create_box)
        self.create_box_button.grid(row=0, column=4, padx=10, pady=5)

        # Rotation controls with buttons
        tk.Label(self.rotation_frame, text="Rotation Controls:").grid(row=0, column=0, padx=10, pady=5)
        self.button_0_deg = tk.Button(self.rotation_frame, text="0°", command=lambda: self.rotate_boxes(0))
        self.button_0_deg.grid(row=0, column=1, padx=10, pady=5)
        self.button_90_deg = tk.Button(self.rotation_frame, text="90°", command=lambda: self.rotate_boxes(90))
        self.button_90_deg.grid(row=0, column=2, padx=10, pady=5)
        self.button_180_deg = tk.Button(self.rotation_frame, text="180°", command=lambda: self.rotate_boxes(180))
        self.button_180_deg.grid(row=0, column=3, padx=10, pady=5)
        self.button_270_deg = tk.Button(self.rotation_frame, text="270°", command=lambda: self.rotate_boxes(270))
        self.button_270_deg.grid(row=0, column=4, padx=10, pady=5)
        self.button_360_deg = tk.Button(self.rotation_frame, text="360°", command=lambda: self.rotate_boxes(360))
        self.button_360_deg.grid(row=0, column=5, padx=10, pady=5)

        # Coordinates display
        self.coordinates_label = tk.Label(self.coordinates_frame, text="Box Center Coordinates:")
        self.coordinates_label.pack()
        self.coordinates_text = tk.Text(self.coordinates_frame, width=50, height=10)
        self.coordinates_text.pack()
        self.get_coordinates_button = tk.Button(self.coordinates_frame, text="GET COORDINATES", command=self.display_coordinates)
        self.get_coordinates_button.pack(pady=10)

        self.pallet = None
        self.boxes = []

    def create_pallet(self):
        try:
            pallet_length = int(self.pallet_length_entry.get())
            pallet_breadth = int(self.pallet_breadth_entry.get())
            pallet_height = int(self.pallet_height_entry.get())
            self.pallet = Pallet(self.canvas, [pallet_length, pallet_breadth, pallet_height])
        except ValueError:
            print("Invalid pallet dimensions")

    def create_box(self):
        try:
            box_length = int(self.box_length_entry.get())
            box_breadth = int(self.box_breadth_entry.get())
            box_height = int(self.box_height_entry.get())
            box = Box(self.canvas, [box_length, box_breadth, box_height])
            self.boxes.append(box)
        except ValueError:
            print("Invalid box dimensions")

    def rotate_boxes(self, angle):
        for box in self.boxes:
            box.rotate(angle * pi / 180)
            box.update_center_coordinates()

    def display_coordinates(self):
        self.coordinates_text.delete(1.0, tk.END)  # Clear previous coordinates
        for box in self.boxes:
            box_number, cx, cy = box.update_center_coordinates()
            self.coordinates_text.insert(tk.END, f"Box {box_number}: ({cx}, {cy})\n")
        self.coordinates_text.see(tk.END)  # Scroll to the end

    def update(self):
        self.master.after(100, self.update)

root = tk.Tk()
app = Application(root)
app.update()
root.mainloop()

