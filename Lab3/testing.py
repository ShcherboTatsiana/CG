import time
import random
from math import sqrt
from algorithms import *

def test_algorithms(iterations=100):
    step_by_step_times = []
    dda_times = []
    bresenham_line_times = []
    bresenham_circle_times = []

    for _ in range(iterations):
        x1, y1 = random.randint(0, 100), random.randint(0, 100)
        x2, y2 = random.randint(0, 100), random.randint(0, 100)

        start_time = time.time()
        step_by_step_line(x1, y1, x2, y2)
        step_by_step_times.append(time.time() - start_time)

        start_time = time.time()
        dda_line(x1, y1, x2, y2)
        dda_times.append(time.time() - start_time)

        start_time = time.time()
        bresenham_line(x1, y1, x2, y2)
        bresenham_line_times.append(time.time() - start_time)

        start_time = time.time()
        r = sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))
        bresenham_circle(x1, y1, r)
        bresenham_circle_times.append(time.time() - start_time)

    print(f"Среднее время выполнения Пошагового алгоритма: {sum(step_by_step_times) / iterations:.6f} секунд")
    print(f"Среднее время выполнения алгоритма DDA: {sum(dda_times) / iterations:.6f} секунд")
    print(f"Среднее время выполнения алгоритма Брезенхема (линия): {sum(bresenham_line_times) / iterations:.6f} секунд")
    print(f"Среднее время выполнения алгоритма Брезенхема (окружность): {sum(bresenham_circle_times) / iterations:.6f} секунд")

test_algorithms()