import itertools as it
from math import pi

import matplotlib.pyplot as plt
import phidl.geometry as pg
import phidl.path as pp
from phidl import Device, Path
from phidl import quickplot as qp  # Rename "quickplot()" to the easier "qp()"
from phidl import set_quickplot_options

rad_to_deg = 360 / (2 * pi)


def arc_petal(
    D: Device,
    n_petals: int,
    outer_radius: float,
    inner_radius: float,
    rotation: float = 0,
    center: tuple[float, float] = (0, 0),
):
    theta = pi / n_petals
    delta_r = outer_radius - inner_radius

    A = pg.arc(
        radius=inner_radius + (delta_r) / 2,
        width=delta_r,
        theta=theta * rad_to_deg,
        start_angle=-(theta * rad_to_deg) / 2,
    )
    A.rotate(rotation)
    A.movex(center[0])
    A.movey(center[1])
    D.add_ref(A)
    return D


def line_petal(
    D: Device,
    n_petals: int,
    outer_radius: float,
    inner_radius: float,
    rotation: float = 0,
    center: tuple[float, float] = (0, 0),
):
    theta = pi / n_petals
    delta_r = outer_radius - inner_radius

    P = Path()
    P.append(pp.straight(delta_r))
    P.movex(inner_radius)
    PP = P.extrude(width=[inner_radius * theta, outer_radius * theta])
    PP.rotate(rotation)
    PP.movex(center[0])
    PP.movey(center[1])
    D.add_ref(PP)
    return D


outer_width_compensation_factor = 0.60
outer_radius_compensation_factor = 1.05


def curved_petal_by_radius(
    D: Device,
    n_petals: int,
    outer_radius: float,
    inner_radius: float,
    arc_r: float,
    rotation: float = 0,
    center: tuple[float, float] = (0, 0),
):
    outer_radius *= outer_radius_compensation_factor

    theta = pi / n_petals
    delta_r = outer_radius - inner_radius

    P = Path()
    P.append(pp.arc(radius=arc_r, angle=delta_r / arc_r * rad_to_deg))
    P.movex(inner_radius)
    PP = P.extrude(
        width=[
            inner_radius * theta,
            outer_radius * theta * outer_width_compensation_factor,
        ]
    )
    PP.rotate(rotation)
    PP.movex(center[0])
    PP.movey(center[1])
    D.add_ref(PP)
    return D


def curved_petal_by_angle(
    D: Device,
    n_petals: int,
    outer_radius: float,
    inner_radius: float,
    petal_rotation: float = 90,
    rotation: float = 0,
    center: tuple[float, float] = (0, 0),
):
    outer_radius *= outer_radius_compensation_factor

    theta = pi / n_petals
    delta_r = outer_radius - inner_radius

    P = Path()
    # len = theta * r => r = theta/len
    angle = petal_rotation
    P.append(pp.arc(radius=delta_r / (angle / rad_to_deg), angle=angle))
    P.movex(inner_radius)
    PP = P.extrude(
        width=[
            inner_radius * theta,
            outer_radius * theta * outer_width_compensation_factor,
        ]
    )
    PP.rotate(rotation)
    PP.movex(center[0])
    PP.movey(center[1])
    D.add_ref(PP)
    return D


def intersect_petal(
    D: Device,
    n_petals: int,
    outer_radius: float,
    inner_radius: float,
    rotation: float = 0,
    center: tuple[float, float] = (0, 0),
):
    outer_radius = 5000
    inner_radius = 1000
    delta_r = outer_radius - inner_radius
    theta = pi / n_petals

    intersect_r = delta_r / 2 ** (1 / 2)
    R = pg.ring(radius=inner_radius + delta_r / 2, width=delta_r)
    C1 = pg.circle(radius=intersect_r)
    C1.movey(-intersect_r)
    C1.movex(inner_radius)
    AND = pg.boolean(A=R, B=C1, operation="and", precision=1e-6)
    C1.rotate(theta * rad_to_deg)
    NOT = pg.boolean(A=AND, B=C1, operation="not", precision=1e-6)
    NOT.rotate(rotation)
    NOT.movex(center[0])
    NOT.movey(center[1])
    D.add_ref(NOT)
    # D.add_ref(C1)
    # D.rotate(theta * rad_to_deg)
    # qp(D)
    # plt.show()
    return D


def flower_center(D: Device, radius: float, center: tuple[float, float]):
    C = pg.circle(radius=radius)
    C.movex(center[0])
    C.movey(center[1])
    D.add_ref(C)
    return D


def arc_flower(
    D: Device,
    n_petals: int = 4,
    outer_radius: float = 5000,
    inner_radius: float = 1000,
    center: tuple[float, float] = (0, 0),
):
    flower_center(D, inner_radius / 2, center)

    for i in range(n_petals):
        arc_petal(
            D=D,
            n_petals=n_petals,
            outer_radius=outer_radius,
            inner_radius=inner_radius,
            rotation=i * 360 / n_petals,
            center=center,
        )
    return D


def line_flower(
    D: Device,
    n_petals: int = 4,
    outer_radius: float = 5000,
    inner_radius: float = 1000,
    center: tuple[float, float] = (0, 0),
):
    flower_center(D, inner_radius / 2, center)

    for i in range(n_petals):
        line_petal(
            D=D,
            n_petals=n_petals,
            outer_radius=outer_radius,
            inner_radius=inner_radius,
            rotation=i * 360 / n_petals,
            center=center,
        )
    return D


def curved_flower_by_radius(
    D: Device,
    n_petals: int = 4,
    outer_radius: float = 5000,
    inner_radius: float = 1000,
    arc_r: float = 8000,
    center: tuple[float, float] = (0, 0),
):
    flower_center(D, inner_radius / 2, center)

    for i in range(n_petals):
        curved_petal_by_radius(
            D=D,
            n_petals=n_petals,
            outer_radius=outer_radius,
            inner_radius=inner_radius,
            rotation=i * 360 / n_petals,
            center=center,
            arc_r=arc_r,
        )
    return D


def curved_flower_by_angle(
    D: Device,
    n_petals: int = 4,
    outer_radius: float = 5000,
    inner_radius: float = 1000,
    petal_rotation: float = 90,
    center: tuple[float, float] = (0, 0),
):
    flower_center(D, inner_radius / 2, center)

    # n_petals = n_petals * 2
    for i in range(n_petals):
        curved_petal_by_angle(
            D=D,
            n_petals=n_petals,
            outer_radius=outer_radius,
            inner_radius=inner_radius,
            petal_rotation=petal_rotation,
            rotation=i * 360 / n_petals,
            center=center,
        )
    return D


def intersect_flower(
    D: Device,
    n_petals: int = 4,
    outer_radius: float = 5000,
    inner_radius: float = 1000,
    center: tuple[float, float] = (0, 0),
):
    flower_center(D, inner_radius / 2, center)

    # n_petals = n_petals * 2
    for i in range(n_petals):
        intersect_petal(
            D=D,
            n_petals=n_petals,
            outer_radius=outer_radius,
            inner_radius=inner_radius,
            rotation=i * 360 / n_petals,
            center=center,
        )
    return D


def test_drawind():
    # Unit is nm
    outer_radius = 5000
    inner_radius = 1000
    n_petals = 6
    arc_r = 8000

    spacing = 15_000

    D = Device("mydevice")

    for i in range(6):
        center = (spacing * i, 0)
        arc_flower(
            D=D,
            n_petals=2 * (i + 1),
            outer_radius=outer_radius,
            inner_radius=outer_radius / 5,
            center=center,
        )

    for i in range(6):
        center = (spacing * i, 0)
        curved_flower_by_angle(
            D=D,
            n_petals=2 * (i + 1),
            outer_radius=5000,
            inner_radius=1000,
            center=center,
        )

    for i in range(6):
        center = (spacing * i, spacing)
        intersect_flower(
            D=D,
            n_petals=2 * (i + 1),
            outer_radius=outer_radius,
            inner_radius=outer_radius / 5,
            center=center,
        )

    set_quickplot_options(show_ports=False, show_subports=False)
    qp(D)
    plt.show()


def create_our_flowers():
    # Unit is nm
    outer_radius = 15_000
    n_petals = 6

    spacing = 100_000

    D = Device("mydevice")

    for i in range(3):
        ri = i  # Get back the i that would be if we didn't multiply
        r = 15_000 - 5_000 * ri
        for j in range(6):
            for dx, dy in it.product([-1, 0, 1], [-1, 0, 1]):
                center = (
                    spacing * j + dx * spacing / 4,
                    -spacing * i + dy * spacing / 4,
                )
                flower_center(D=D, radius=r / 5 / 2, center=center)

    for i in range(3):
        r = 15_000 - 5_000 * i
        for j in range(6):
            center = (spacing * j, -spacing * (i + 3))
            arc_flower(
                D=D,
                n_petals=n_petals,
                outer_radius=r,
                inner_radius=r / 5,
                center=center,
            )

    for i in range(3):
        p = 4 + 2 * i
        for j in range(6):
            center = (spacing * j, -spacing * (i + 6))
            curved_flower_by_angle(
                D=D,
                n_petals=p,
                outer_radius=outer_radius,
                inner_radius=outer_radius / 5,
                center=center,
            )

    set_quickplot_options(show_ports=False, show_subports=False)
    qp(D)
    plt.show()

    D.write_gds(
        filename="flowers.gds",  # Output GDS file name
        unit=1e-9,  # Base unit
        precision=1e-9,  # Precision / resolution
        auto_rename=True,  # Automatically rename cells to avoid collisions
        max_cellname_length=28,  # Max length of cell names
        cellname="toplevel",  # Name of output top-level cell
    )


def create_big_flowers_for_emile():
    # Unit is nm
    outer_radius = 50_000
    spacing = 300_000

    D = Device("mydevice")

    for j in range(4):
        for dx, dy in it.product([-1, 0, 1], [-1, 0, 1]):
            center = (
                spacing * j + dx * spacing / 4,
                dy * spacing / 4,
            )
            flower_center(D=D, radius=outer_radius / 5 / 2, center=center)

    for i in range(1):
        p = 8
        for j in range(4):
            center = (spacing * j, -spacing * (i + 1))
            arc_flower(
                D=D,
                n_petals=p,
                outer_radius=outer_radius,
                inner_radius=outer_radius / 5,
                center=center,
            )

    for i in range(3):
        p = 4 + 2 * i
        for j in range(4):
            center = (spacing * j, -spacing * (i + 2))
            curved_flower_by_angle(
                D=D,
                n_petals=p,
                outer_radius=outer_radius,
                inner_radius=outer_radius / 5,
                center=center,
            )

    set_quickplot_options(show_ports=False, show_subports=False)
    qp(D)
    plt.show()

    D.write_gds(
        filename="big_flowers.gds",  # Output GDS file name
        unit=1e-9,  # Base unit
        precision=1e-9,  # Precision / resolution
        auto_rename=True,  # Automatically rename cells to avoid collisions
        max_cellname_length=28,  # Max length of cell names
        cellname="toplevel",  # Name of output top-level cell
    )


# Plan:

# 6 cols, all identical
# Regular flower of sizes R_o = 15, 10, 5 , R_i = 3, 2, 1 , R_d = 1.5, 1.0, 0.5
# Just the disks of same
# Arc flowers with Np = 4, 6, 8
# separation = 60

if __name__ == "__main__":
    # test_drawind()
    create_our_flowers()
    create_big_flowers_for_emile()
    # D = Device("testy")
    # intersect_petal(D=D, n_petals=6, outer_radius=5000, inner_radius=1000)
