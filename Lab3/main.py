import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import sqrt
from algorithms import *
from test import *

class RasterizationInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Алгоритмы растеризации")

        algorithm_frame = tk.Frame(root)
        algorithm_frame.pack(pady=10)

        self.label_method = tk.Label(algorithm_frame, text="Выберите метод:")
        self.label_method.pack(side=tk.LEFT)

        self.algorithm_combobox = ttk.Combobox(algorithm_frame, values=[
            'Пошаговый алгоритм',
            'Алгоритм ЦДА (DDA)',
            'Алгоритм Брезенхема (линия)',
            'Алгоритм Брезенхема (окружность)'
        ])
        self.algorithm_combobox.current(0)
        self.algorithm_combobox.pack(side=tk.LEFT)

        frame1 = tk.Frame(root)
        frame1.pack(pady=10)

        self.label_x1 = tk.Label(frame1, text="Введите x1:")
        self.label_x1.pack(side=tk.LEFT)
        self.entry_x1 = tk.Entry(frame1)
        self.entry_x1.pack(side=tk.LEFT)

        self.label_y1 = tk.Label(frame1, text="Введите y1:")
        self.label_y1.pack(side=tk.LEFT)
        self.entry_y1 = tk.Entry(frame1)
        self.entry_y1.pack(side=tk.LEFT)

        frame2 = tk.Frame(root)
        frame2.pack(pady=10)

        self.label_x2 = tk.Label(frame2, text="Введите x2:")
        self.label_x2.pack(side=tk.LEFT)
        self.entry_x2 = tk.Entry(frame2)
        self.entry_x2.pack(side=tk.LEFT)

        self.label_y2 = tk.Label(frame2, text="Введите y2:")
        self.label_y2.pack(side=tk.LEFT)
        self.entry_y2 = tk.Entry(frame2)
        self.entry_y2.pack(side=tk.LEFT)

        frame3 = tk.Frame(root)
        frame3.pack(pady=10)

        self.scale_label = tk.Label(frame3, text="Масштаб:")
        self.scale_label.pack(side=tk.LEFT)

        self.scale_slider = tk.Scale(frame3, from_=1, to=10, 
                                    orient=tk.HORIZONTAL, resolution=1)
        self.scale_slider.set(3)
        self.scale_slider.pack(side=tk.LEFT, padx = (0,20))

        self.plot_button = tk.Button(frame3, text="Изобразить", 
                                    command=self.plot)
        self.plot_button.pack(side=tk.RIGHT)

        self.figure = plt.Figure(figsize=(6, 5.8), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack()

    def plot(self):
        x1 = float(self.entry_x1.get())
        y1 = float(self.entry_y1.get())
        x2 = float(self.entry_x2.get())
        y2 = float(self.entry_y2.get())

        algorithm = self.algorithm_combobox.get()

        if algorithm == 'Пошаговый алгоритм':
            points = step_by_step_line(x1, y1, x2, y2)
        elif algorithm == 'Алгоритм ЦДА (DDA)':
            points = dda_line(x1, y1, x2, y2)
        elif algorithm == 'Алгоритм Брезенхема (линия)':
            points = bresenham_line(x1, y1, x2, y2)
        elif algorithm == 'Алгоритм Брезенхема (окружность)':
            r = sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))
            points = bresenham_circle(x1, y1, r)

        self.figure.clear()  
        ax = self.figure.add_subplot(111)

        scale = self.scale_slider.get()

        for (x, y) in points:
            ax.add_patch(plt.Rectangle((x, y), 1, 1,
                                        color='blue', alpha=0.5))

        ax.set_aspect('equal', adjustable='box')
        ax.set_xticks(range(-int(30/scale), int(30/scale), 1))
        ax.set_yticks(range(-int(30/scale), int(30/scale), 1))

        ax.axhline(0, color='black', linewidth=1.5)
        ax.axvline(0, color='black', linewidth=1.5)

        ax.grid(True)
        ax.set_xlabel('Ось X')
        ax.set_ylabel('Ось Y')

        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = RasterizationInterface(root)
    root.mainloop()
