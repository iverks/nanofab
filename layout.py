from math import pi

import matplotlib.pyplot as plt
import phidl.geometry as pg
import phidl.path as pp
from phidl import Device, Path
from phidl import quickplot as qp  # Rename "quickplot()" to the easier "qp()"

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


def curved_petal_by_radius(
    D: Device,
    n_petals: int,
    outer_radius: float,
    inner_radius: float,
    arc_r: float,
    rotation: float = 0,
    center: tuple[float, float] = (0, 0),
):
    theta = pi / n_petals
    delta_r = outer_radius - inner_radius

    P = Path()
    P.append(pp.arc(radius=arc_r, angle=delta_r / arc_r * rad_to_deg))
    P.movex(inner_radius)
    PP = P.extrude(width=[inner_radius * theta, outer_radius * theta])
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
    theta = pi / n_petals
    delta_r = outer_radius - inner_radius

    P = Path()
    # len = theta * r => r = theta/len
    angle = petal_rotation
    P.append(pp.arc(radius=delta_r / (angle / rad_to_deg), angle=angle))
    P.movex(inner_radius)
    PP = P.extrude(width=[inner_radius * theta, outer_radius * theta])
    PP.rotate(rotation)
    PP.movex(center[0])
    PP.movey(center[1])
    D.add_ref(PP)
    return D


def arc_flower(
    D: Device,
    n_petals: int = 4,
    outer_radius: float = 5000,
    inner_radius: float = 1000,
    center: tuple[float, float] = (0, 0),
):
    C = pg.circle(radius=inner_radius / 2)
    C.movex(center[0])
    C.movey(center[1])
    D.add_ref(C)

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
    C = pg.circle(radius=inner_radius / 2)
    C.movex(center[0])
    C.movey(center[1])
    D.add_ref(C)

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
    C = pg.circle(radius=inner_radius / 2)
    C.movex(center[0])
    C.movey(center[1])
    D.add_ref(C)

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
    C = pg.circle(radius=inner_radius / 2)
    C.movex(center[0])
    C.movey(center[1])
    D.add_ref(C)

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


# Unit is nm
outer_radius = 5000
inner_radius = 1000
n_petals = 6
arc_r = 8000

spacing = 20_000

D = Device("mydevice")

for i in range(6):
    center = (spacing * i, 0)
    outer_radius = 5000 + 1000 * i
    arc_flower(
        D=D,
        n_petals=n_petals,
        outer_radius=outer_radius,
        inner_radius=outer_radius / 5,
        center=center,
    )

for i in range(6):
    center = (spacing * i, spacing)
    outer_radius = 5000 + 1000 * i
    line_flower(
        D=D,
        n_petals=n_petals,
        outer_radius=outer_radius,
        inner_radius=outer_radius / 5,
        center=center,
    )

for i in range(6):
    center = (spacing * i, 2 * spacing)
    curved_flower_by_radius(
        D=D,
        n_petals=n_petals,
        outer_radius=5000,
        inner_radius=1000,
        arc_r=8000 - 1000 * i,
        center=center,
    )

for i in range(6):
    center = (spacing * i, 3 * spacing)
    curved_flower_by_radius(
        D=D,
        n_petals=10,
        outer_radius=5000,
        inner_radius=1000,
        arc_r=8000 - 1000 * i,
        center=center,
    )

for i in range(6):
    center = (spacing * i, 4 * spacing)
    curved_flower_by_angle(
        D=D,
        n_petals=2 * (i + 1),
        outer_radius=5000,
        inner_radius=1000,
        center=center,
    )


qp(D)
plt.show()

# D.write_gds(
#     filename="flowers.gds",  # Output GDS file name
#     unit=1e-9,  # Base unit
#     precision=1e-9,  # Precision / resolution
#     auto_rename=True,  # Automatically rename cells to avoid collisions
#     max_cellname_length=28,  # Max length of cell names
#     cellname="toplevel",  # Name of output top-level cell
# )
