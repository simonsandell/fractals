from multiprocessing import Pool
import julia
import numpy as np
import cmath


def generate_image(c, k):
    if k // 100 == 0:
        if k // 10 == 0:
            str_k = "00" + str(k)
        else:
            str_k = "0" + str(k)
    else:
        str_k = str(k)

    i = julia.make_julia(c, 2, 1024)
    i.save("./gif_stage_1000/" + str_k + ".png", "PNG")


def half_circle_contour_path(num_points):
    args = []
    k = 0
    num_points_line = int(num_points / 2)
    num_points_circle = num_points - num_points_line

    # line segment
    start_c = -0.9653942497733798 - (1j * 0.2607948283699144)
    end_c = -start_c

    X = np.linspace(start_c.real, end_c.real, num_points_line)
    Y = np.linspace(start_c.imag, end_c.imag, num_points_line)

    for x, y in zip(X, Y):
        if k not in already_done:
            args.append((x + 1j * y, k))
        k = k + 1

    # circle segment
    r, phi_start = cmath.polar(end_c)
    phi_end = phi_start + cmath.pi
    PHI = np.linspace(phi_start, phi_end, num_points_circle)

    for phi in PHI:
        if k not in already_done:
            args.append((r * cmath.exp(1j * phi), k))
        k = k + 1


def spiral_path(num_points):
    args = []
    k = 0

    num_rotations = 5
    num_oscillations = 2

    z_fun = lambda x, y: cmath.sin(x) * cmath.exp(1j * y)

    X = np.linspace(0, num_oscillations * cmath.pi, num_points)
    Y = np.linspace(0, num_rotations * 2 * cmath.pi, num_points)

    for x, y in zip(X, Y):
        args.append((z_fun(x, y), k))
        k = k + 1
    return args


args = spiral_path(1000)
print(args)
p = Pool(6)
p.starmap(generate_image, args)
# for arg in args:
#    generate_image(*arg)
p.close()
p.join()
p.terminate()
