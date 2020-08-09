import math
import random
import sys
import numpy as np
from PIL import Image
from scipy.optimize import fsolve


def int_to_rgb(k, max_iter):
    a = k / max_iter
    # backcol = [255, 255, 221]
    # forecol = [247, 231, 180]
    forecol = [0, 0, 0]
    backcol = [255, 255, 255]
    r = backcol[0] - math.floor((backcol[0] - forecol[0]) * a)
    g = backcol[1] - math.floor((backcol[1] - forecol[1]) * a)
    b = backcol[2] - math.floor((backcol[2] - forecol[2]) * a)

    return (r, g, b)


def get_escape_radius(n, c):
    # R**n - R >= sqrt( cx**2 + cy**2)
    # R**n -R >= sqrt(2)
    # R**n - R = sqrt(2)
    f = lambda x: x ** n - x - math.sqrt(c.real ** 2 + c.imag ** 2)
    escape_radius = 2 * fsolve(f, 4)
    print(n, escape_radius)
    return escape_radius


def get_julia_value(z, c, n, max_iter, escape_radius):
    k = 1
    while (abs(z) < escape_radius) and (k < max_iter):
        z = z ** n + c
        k += 1
    if k == max_iter:
        return k
    return k - math.log(math.log(abs(z), n), n)


def make_julia(c, n, size):
    escape_radius = get_escape_radius(n, c)
    max_iter = 30
    img = np.zeros((size, size, 3), dtype=np.uint8)
    for i in range(size):
        for j in range(size):
            x = i - 0.5 * size
            y = j - 0.5 * size
            x = x / (0.25 * size)
            y = y / (0.25 * size)
            iters = get_julia_value(x + 1j * y, c, n, max_iter, escape_radius)
            img[i, j] = int_to_rgb(iters, max_iter)
    i = Image.fromarray(img, "RGB")
    return i


if __name__ == "__main__":
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
        cx = float(sys.argv[2])
        cy = float(sys.argv[3])
        size = int(sys.argv[4])
    else:
        import time

        seed = str(time.time())
        random.seed(seed)

        ints = [2, 3, 4, 5]
        n = random.choice(ints)

        alpha = 2 * math.pi * random.random()
        r = random.random()
        cx = r * math.cos(alpha)
        cy = r * math.sin(alpha)

        size = 1024

    c = cx + cy * 1j
    imag = make_julia(c, n, size)
    filename = str(n) + "_" + str(c) + ".png"
    imag.save(filename, "PNG")
