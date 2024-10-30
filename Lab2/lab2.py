import cv2
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk

def display_images(original, processed):
    orig_image = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    processed_image = cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)

    height, width, _ = original.shape

    max_width = int(root.winfo_screenwidth() / 2) 
    max_height = root.winfo_screenheight() - 275  

    aspect_ratio = width / height
    space_aspect_ratio = max_width / max_height

    if aspect_ratio > space_aspect_ratio:
        scale = max_width / width
    else:
        scale = max_height / height

    new_width = int(width * scale)
    new_height = int(height * scale)

    orig_image = Image.fromarray(orig_image).resize((new_width, new_height))
    processed_image = Image.fromarray(processed_image).resize((new_width, new_height))

    orig_photo = ImageTk.PhotoImage(orig_image)
    processed_photo = ImageTk.PhotoImage(processed_image)

    orig_label.config(image=orig_photo)
    orig_label.image = orig_photo

    processed_label.config(image=processed_photo)
    processed_label.image = processed_photo

def linear_contrast(image):
    return cv2.convertScaleAbs(image, alpha=1.5, beta=0)

def plot_histogram(image):
    channels = cv2.split(image)
    colors = ('b', 'g', 'r')  
    plt.figure()
    for i, color in enumerate(colors):
        hist = cv2.calcHist([channels[i]], [0], None, [256], [0, 256])
        plt.plot(hist, color=color)
        plt.xlim([0, 256])
    plt.title('Гистограмма изображения')
    plt.xlabel('Интенсивность')
    plt.ylabel('Количество пикселей')
    plt.show()

def histogram_equalization_rgb(image):
    channels = cv2.split(image)
    equalized_channels = [cv2.equalizeHist(c) for c in channels]
    return cv2.merge(equalized_channels)

def histogram_equalization_hsv(image):
    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    channels = cv2.split(img_hsv)
    cv2.equalizeHist(channels[2], channels[2])  # Эквализация V
    return cv2.cvtColor(cv2.merge(channels), cv2.COLOR_HSV2BGR)

def sharpen_image(image, alpha):
    kernel = np.array([[0, -1, 0],
                       [-1, 4 + alpha, -1],
                       [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)

def load_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        global image, orig_image
        orig_image = cv2.imread(file_path)
        image = orig_image.copy()
        if image is None:
            messagebox.showerror("Ошибка", "Не удалось загрузить изображение.")
        else:
            messagebox.showinfo("Успех", "Изображение загружено.")
            display_images(image, image)
            plot_histogram(image) 

def process_image():
    if image is None:
        messagebox.showerror("Ошибка", "Сначала загрузите изображение.")
        return

    process_type = method_combobox.get()
    
    if process_type == 'Линейное контрастирование':
        result = linear_contrast(image)

    elif process_type == 'Эквализация гистограммы (RGB)':
        result = histogram_equalization_rgb(image)

    elif process_type == 'Эквализация гистограммы (HSV)':
        result = histogram_equalization_hsv(image)

    elif process_type == 'Оригинальное изображение':
        result = orig_image

    else:
        return

    display_images(orig_image, result)

def apply_sharpening():
    if image is None:
        messagebox.showerror("Ошибка", "Сначала загрузите изображение.")
        return

    alpha = sharpness_scale.get()
    result = sharpen_image(image, alpha)
    display_images(orig_image, result)

# Интерфейс
root = tk.Tk()
root.title("Обработка изображений")
root.attributes("-fullscreen", True)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

load_button = tk.Button(button_frame, text="Загрузить изображение", command=load_image)
load_button.pack(side=tk.TOP, padx=5)

method_combobox = ttk.Combobox(button_frame, values=[
    'Оригинальное изображение',
    'Линейное контрастирование',
    'Эквализация гистограммы (RGB)',
    'Эквализация гистограммы (HSV)'
])
method_combobox.set("Выберите метод")
method_combobox.pack(side=tk.TOP, padx=5)
method_combobox['state'] = 'readonly'

process_button = tk.Button(button_frame, text="Обработать изображение", command=process_image)
process_button.pack(side=tk.TOP, padx=5)

sharpness_label = tk.Label(button_frame, text="Уровень резкости")
sharpness_label.pack(side=tk.TOP, padx=5)

sharpness_scale = tk.Scale(button_frame, from_=-1, to=5, resolution=0.1, orient=tk.HORIZONTAL, length=300)
sharpness_scale.set(1)
sharpness_scale.pack(side=tk.TOP, padx=5)

sharpen_button = tk.Button(button_frame, text="Применить увеличение резкости", command=apply_sharpening)
sharpen_button.pack(side=tk.LEFT, padx=(5, 2), pady=10)

image_frame = tk.Frame(root)
image_frame.pack()

orig_label = tk.Label(image_frame)
orig_label.pack(side=tk.LEFT, padx=5, pady=5)

processed_label = tk.Label(image_frame)
processed_label.pack(side=tk.LEFT, padx=5, pady=5)

orig_image = None
image = None

def exit_fullscreen(event):
    root.attributes("-fullscreen", False)

root.bind("<Escape>", exit_fullscreen)
root.mainloop()