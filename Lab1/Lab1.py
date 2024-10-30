import tkinter as tk
from tkinter import colorchooser
import colorsys as cs

# Functions
def rgb_to_hls(r, g, b):
    r /= 255.0
    g /= 255.0
    b /= 255.0

    c_max = max(r, g, b)
    c_min = min(r, g, b)
    delta = c_max - c_min
    l = (c_max + c_min) / 2

    if delta == 0: 
        s = 0
        h = 0  
    else:
        if l < 0.5:
            s = delta / (c_max + c_min)
        else:
            s = delta / (2 - (c_max + c_min))

    if c_max == r:
        h = (g - b) / delta + (6 if g < b else 0)
    elif c_max == g:
        h = (b - r) / delta + 2
    else:
        h = (r - g) / delta + 4

    h *= 60
    if h < 0:
        h += 360

    l *= 100
    s *= 100

    return round(h), round(l), round(s)

def hls_to_rgb(h, l, s):
    l /= 100.0
    s /= 100.0

    c = (1 - abs(2 * l - 1)) * s    
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2

    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = c, x, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    elif 300 <= h < 360:
        r, g, b = c, 0, x

    r = int((r + m) * 255)
    g = int((g + m) * 255)
    b = int((b + m) * 255)

    return r, g, b


def rgb_to_cmyk(r, g, b):
    r /= 255.0
    g /= 255.0
    b /= 255.0

    c = 1 - r
    m = 1 - g
    y = 1 - b
    k = min(c, m, y)

    if k < 1:
        c = (c - k) / (1 - k)
        m = (m - k) / (1 - k)
        y = (y - k) / (1 - k)
    else:
        c = m = y = 0

    c = round(c * 100)
    m = round(m * 100)
    y = round(y * 100)
    k = round(k * 100)

    return c, m, y, k

def cmyk_to_rgb(c, m, y, k):
    c /= 100.0
    m /= 100.0
    y /= 100.0
    k /= 100.0

    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)

    return round(r), round(g), round(b)

def update_cmyk(c, m, y, k):
    
    c_slider.set(c)
    m_slider.set(m)
    y_slider.set(y)
    k_slider.set(k)

    c_spinbox.delete(0, "end")
    c_spinbox.insert(0, str(c))
    m_spinbox.delete(0, "end")
    m_spinbox.insert(0, str(m))
    y_spinbox.delete(0, "end")
    y_spinbox.insert(0, str(y))
    k_spinbox.delete(0, "end")
    k_spinbox.insert(0, str(k))

def update_rgb(r, g, b):
    r_slider.set(r)
    g_slider.set(g)
    b_slider.set(b)

    r_spinbox.delete(0, "end")
    r_spinbox.insert(0, str(r))
    g_spinbox.delete(0, "end")
    g_spinbox.insert(0, str(g))
    b_spinbox.delete(0, "end")
    b_spinbox.insert(0, str(b))

def update_hls(h, l, s):
    h_slider.set(h)
    l_slider.set(l)
    s_slider.set(s)

    h_spinbox.delete(0, "end")
    h_spinbox.insert(0, str(h))
    l_spinbox.delete(0, "end")
    l_spinbox.insert(0, str(l))
    s_spinbox.delete(0, "end")
    s_spinbox.insert(0, str(s))


def update_models_color(c, m, y, k, r, g, b, h, l, s):
    update_cmyk(c, m, y, k)
    update_hls(h, l, s)
    update_rgb(r, g, b)
    color_box.config(bg=f'#{r:02x}{g:02x}{b:02x}')

    
def on_cmyk_slider_change(var):
    c = int(c_slider.get())
    m = int(m_slider.get())
    y = int(y_slider.get())
    k = int(k_slider.get())

    r, g, b = cmyk_to_rgb(c, m, y, k)
    h, l, s = rgb_to_hls(r, g, b)

    update_models_color(c, m, y, k, r, g, b, h, l, s)

def on_rgb_slider_change(event):
    r = int(r_slider.get())
    g = int(g_slider.get())
    b = int(b_slider.get())

    h, l, s = rgb_to_hls(r, g, b)
    c, m, y, k = rgb_to_cmyk(r, g, b)

    update_models_color(c, m, y, k, r, g, b, h, l, s)

def on_hls_slider_change(event):
    h = int(h_slider.get())
    s = int(s_slider.get())
    l = int(l_slider.get())

    r, g, b = hls_to_rgb(h, l, s)
    c, m, y, k = rgb_to_cmyk(r, g, b)

    update_models_color(c, m, y, k, r, g, b, h, l, s)


def on_cmyk_spinbox_change():
    c = int(c_spinbox.get())
    m = int(m_spinbox.get())
    y = int(y_spinbox.get())
    k = int(k_spinbox.get())

    r, g, b = cmyk_to_rgb(c, m, y, k)
    h, l, s = rgb_to_hls(r, g, b)

    update_models_color(c, m, y, k, r, g, b, h, l, s)

def on_cmyk_spinbox_change_for_bind(event):
    on_cmyk_spinbox_change()

def on_rgb_spinbox_change():
    r = int(r_spinbox.get())
    g = int(g_spinbox.get())
    b = int(b_spinbox.get())

    h, l, s = rgb_to_hls(r, g, b)
    c, m, y, k = rgb_to_cmyk(r, g, b)

    update_models_color(c, m, y, k, r, g, b, h, l, s)

def on_rgb_spinbox_change_for_bind(event):
    on_rgb_spinbox_change()

def on_hls_spinbox_change():
    h = int(h_spinbox.get())
    s = int(s_spinbox.get())
    l = int(l_spinbox.get())

    r, g, b = hls_to_rgb(h, l, s)
    c, m, y, k = rgb_to_cmyk(r, g, b)

    update_models_color(c, m, y, k, r, g, b, h, l, s)

def on_hls_spinbox_change_for_bind(event):
    on_hls_spinbox_change()

def choose_color():
    color_code = colorchooser.askcolor(title="Choose color")
    if color_code:
        rgb = color_code[0]
        r, g, b = int(rgb[0]), int(rgb[1]), int(rgb[2])

        h, l, s = rgb_to_hls(r, g, b)
        c, m, y, k = rgb_to_cmyk(r, g, b)

        update_models_color(c, m, y, k, r, g, b, h, l, s)

# Interface
root = tk.Tk()
root.title("Color Chooser")

top_frame = tk.Frame(root)
top_frame.pack()

color_box = tk.Label(top_frame, width=50, height=8, bg=f'#000000')
color_box.pack(pady=10)

choose_color_button = tk.Button(top_frame, text="Choose Color", command=choose_color)
choose_color_button.pack(pady=10)

bottom_frame = tk.Frame(root)
bottom_frame.pack()

# CMYK
cmyk_frame = tk.Frame(bottom_frame)
cmyk_frame.pack(side=tk.LEFT, padx = 30)

tk.Label(cmyk_frame, text="C:  0-100").grid(row=0, column=0, padx = 10)
c_slider = tk.Scale(cmyk_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                     command=on_cmyk_slider_change)
c_slider.grid(row=0, column=1)
c_spinbox = tk.Spinbox(cmyk_frame, from_=0, to=100, increment=1, width=3, 
                    command=on_cmyk_spinbox_change) 
c_spinbox.grid(row=0, column=2, padx = 10)

tk.Label(cmyk_frame, text="M:  0-100").grid(row=1, column=0, padx = 10)
m_slider = tk.Scale(cmyk_frame, from_=0, to=100, orient=tk.HORIZONTAL, 
                    command=on_cmyk_slider_change) 
m_slider.grid(row=1, column=1)
m_spinbox = tk.Spinbox(cmyk_frame, from_=0, to=100, increment=1, width=3, 
                    command=on_cmyk_spinbox_change) 
m_spinbox.grid(row=1, column=2, padx = 10)

tk.Label(cmyk_frame, text="Y:  0-100").grid(row=2, column=0, padx = 10)
y_slider = tk.Scale(cmyk_frame, from_=0, to=100, orient=tk.HORIZONTAL, 
                    command=on_cmyk_slider_change)
y_slider.grid(row=2, column=1)
y_spinbox = tk.Spinbox(cmyk_frame, from_=0, to=100, increment=1, width=3,
                    command=on_cmyk_spinbox_change) 
y_spinbox.grid(row=2, column=2, padx = 10)

tk.Label(cmyk_frame, text="K:  0-100").grid(row=3, column=0, padx = 10)
k_slider = tk.Scale(cmyk_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                    command=on_cmyk_slider_change) 
k_slider.grid(row=3, column=1)
k_spinbox = tk.Spinbox(cmyk_frame, from_=0, to=100, increment=1, width=3, 
                       command=on_cmyk_spinbox_change) 
k_spinbox.grid(row=3, column=2, padx = 10)

c_spinbox.bind("<KeyRelease>", on_cmyk_spinbox_change_for_bind)
m_spinbox.bind("<KeyRelease>", on_cmyk_spinbox_change_for_bind)
y_spinbox.bind("<KeyRelease>", on_cmyk_spinbox_change_for_bind)
k_spinbox.bind("<KeyRelease>", on_cmyk_spinbox_change_for_bind)

# RGB
rgb_frame = tk.Frame(bottom_frame)
rgb_frame.pack(side=tk.LEFT, padx = 30)

tk.Label(rgb_frame, text="R:  0-255").grid(row=0, column=0, padx = 10)
r_slider = tk.Scale(rgb_frame, from_=0, to=255, orient=tk.HORIZONTAL, 
                    command=on_rgb_slider_change) 
r_slider.grid(row=0, column=1)
r_spinbox = tk.Spinbox(rgb_frame, from_=0, to=255, increment=1, width=3,
                    command=on_rgb_spinbox_change) 
r_spinbox.grid(row=0, column=2, padx=10)

tk.Label(rgb_frame, text="G:  0-255").grid(row=1, column=0, padx = 10)
g_slider = tk.Scale(rgb_frame, from_=0, to=255, orient=tk.HORIZONTAL,
                    command=on_rgb_slider_change) 
g_slider.grid(row=1, column=1)
g_spinbox = tk.Spinbox(rgb_frame, from_=0, to=255, increment=1, width=3,
                    command=on_rgb_spinbox_change) 
g_spinbox.grid(row=1, column=2, padx=10)

tk.Label(rgb_frame, text="B:  0-255").grid(row=2, column=0, padx = 10)
b_slider = tk.Scale(rgb_frame, from_=0, to=255, orient=tk.HORIZONTAL,
                    command=on_rgb_slider_change) 
b_slider.grid(row=2, column=1)
b_spinbox = tk.Spinbox(rgb_frame, from_=0, to=255, increment=1, width=3,
                    command=on_rgb_spinbox_change)
b_spinbox.grid(row=2, column=2, padx=10)

r_spinbox.bind("<KeyRelease>", on_rgb_spinbox_change_for_bind)  
g_spinbox.bind("<KeyRelease>", on_rgb_spinbox_change_for_bind)  
b_spinbox.bind("<KeyRelease>", on_rgb_spinbox_change_for_bind)  

# HLS
hls_frame = tk.Frame(bottom_frame)
hls_frame.pack(side=tk.LEFT, padx = 30)

tk.Label(hls_frame, text="H:  0-360。").grid(row=0, column=0, padx = 20)
h_slider = tk.Scale(hls_frame, from_=0, to=360, orient=tk.HORIZONTAL,
                    command=on_hls_slider_change)
h_slider.grid(row=0, column=1)
h_spinbox = tk.Spinbox(hls_frame, from_=0, to=360, increment=1, width=3,
                    command=on_hls_spinbox_change)
h_spinbox.grid(row=0, column=2, padx=10)

tk.Label(hls_frame, text="L:  0-100%").grid(row=1, column=0, padx = 20)
l_slider = tk.Scale(hls_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                    command=on_hls_slider_change)
l_slider.grid(row=1, column=1)
l_spinbox = tk.Spinbox(hls_frame, from_=0, to=100, increment=1, width=3,
                    command=on_hls_spinbox_change) 
l_spinbox.grid(row=1, column=2, padx=10)

tk.Label(hls_frame, text="S:  0-100%").grid(row=2, column=0, padx = 20)
s_slider = tk.Scale(hls_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                    command=on_hls_slider_change)
s_slider.grid(row=2, column=1)
s_spinbox = tk.Spinbox(hls_frame, from_=0, to=100, increment=1, width=3,
                    command=on_hls_spinbox_change) 
s_spinbox.grid(row=2, column=2, padx=10)

h_spinbox.bind("<KeyRelease>", on_hls_spinbox_change_for_bind)
l_spinbox.bind("<KeyRelease>", on_hls_spinbox_change_for_bind)
s_spinbox.bind("<KeyRelease>", on_hls_spinbox_change_for_bind)

root.mainloop()