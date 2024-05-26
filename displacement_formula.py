import math


def calculate_suscepyt(b):
    # Formula involving natural logarithm and square root
    # Note: here 4pi = 12.56 is multiplied just to match the mumax simulation
    X = 12.56 / (2 * b * (math.log(8) - math.log(b) - 0.5))
    return X


def calculate_displacement(B, u, R, M, X):
    d = X * R * B / (u * M)
    return d


def slope_of_displacement(u, R, M, X):
    return X * R / (u * M)


u_value = 12.56e-7  # Thickness
M_value = 860000
t_value = 80e-9  # Thickness

for r in range(1, 3 + 1):
    R_value = 0.5e-6 * r
    b_value = t_value / R_value

    X = calculate_suscepyt(b_value * 0.55)
    # print(f"The susceptibility for r={R_value * 1e6}µm is: {X}")
    slope = slope_of_displacement(u_value, R_value, M_value, X)
    print(f"Slope of displacement is {slope * 1e3:f}")

    # for b in range(-5, 5 + 1):
    #     B_value = b * 1e-3

    #     result1 = calculate_displacement(B_value, u_value, R_value, M_value, X)
    #     print(f"displacement is :{result1*1.0e6}um")
    #     # change the value of R as well as the value of b in the first formula
