# Пошаговый алгоритм
def step_by_step_line(x1, y1, x2, y2):
    x = x1
    y = y1
    points = []

    if (abs(x2 - x1) >= abs(y2 - y1)):
        a = (y2 - y1) / (x2 - x1)
        while (x < x2):
            points.append((x, round(y)))
            x += 1
            y += a
    else:
        a = (x2 - x1) / (y2 - y1)
        while (y < y2):
            points.append((round(x), y))
            x += a
            y += 1

    return points

# Алгоритм ЦДА
def dda_line(x1, y1, x2, y2):
    Dx = x2 - x1
    Dy = y2 - y1
    steps = max(abs(Dx), abs(Dy))
    deltaX = Dx/steps
    deltaY = Dy/steps

    x = x1
    y = y1
    points = []
    for _ in range(int(steps)):
        points.append((round(x), round(y)))
        x += deltaX
        y += deltaY

    return points

# Алгоритм Брезенхема (линия)
def bresenham_line(x1, y1, x2, y2):
    points = []
    Dx = x2 - x1
    Dy = y2 - y1
    Sx = 1 if Dx > 0 else -1
    Sy = 1 if Dy > 0 else -1
    Dx = abs(Dx)
    Dy = abs(Dy)
    
    x = x1
    y = y1
    if Dx > Dy:
        err = Dx / 2.0
        while x != x2:
            points.append((x, y))
            err -= Dy
            if err < 0:
                y += Sy
                err += Dx
            x += Sx
    else:
        err = Dy / 2.0
        while y != y2:
            points.append((x, y))
            err -= Dx
            if err < 0:
                x += Sx
                err += Dy
            y += Sy
    
    return points

# Алгоритм Брезенхема (окружность)
def bresenham_circle(x_center, y_center, radius):
    points = []
    x = radius
    y = 0
    points.append((x_center + x, y_center + y))
    points.append((x_center - x, y_center + y))
    points.append((x_center + y, y_center - x))
    points.append((x_center - y, y_center - x))
    
    if radius > 0:
        points.append((x_center + x, y_center - y))
        points.append((x_center - x, y_center - y))
        points.append((x_center + y, y_center + x))
        points.append((x_center - y, y_center + x))
        
    p = 1 - radius
    
    while x > y:
        y += 1
        if p <= 0:
            p = p + 2 * y + 1
        else:
            x -= 1
            p = p + 2 * y - 2 * x + 1
        
        if x < y:
            break
        
        points.append((x_center + x, y_center + y))
        points.append((x_center - x, y_center + y))
        points.append((x_center + x, y_center - y))
        points.append((x_center - x, y_center - y))
        points.append((x_center + y, y_center + x))
        points.append((x_center - y, y_center + x))
        points.append((x_center + y, y_center - x))
        points.append((x_center - y, y_center - x))
    
    return points
