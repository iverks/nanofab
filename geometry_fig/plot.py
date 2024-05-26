from math import pi
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.patches import Arc, FancyArrowPatch
from PIL import Image


def main():
    straight = Image.open("straight_device.png")
    curved = Image.open("curved_device.png")
    s_ar = straight.width / straight.height
    c_ar = curved.width / curved.height
    fig, axs = plt.subplot_mosaic([["a", "b"]], width_ratios=[s_ar, c_ar])
    axs: dict[str, Axes] = axs
    sax = axs["a"]
    cax = axs["b"]
    sax.imshow(straight)
    cax.imshow(curved)

    for label, ax in axs.items():
        ax.autoscale(False)
        ax.axis("off")
        ax.text(
            50,
            50,
            label,
            fontsize=16,
            ha="left",
            va="top",
            backgroundcolor="black",
            color="white",
        )

    # Straight
    center = (1095, 1169)
    cx, cy = center
    R_o = 1169 - 54
    R_i = R_o / 5
    R_d = R_i / 2

    color = "yellow"
    fontsize = 16
    head_width = 1.5

    # R_o
    sax.plot([cx, cx + R_o], [cy, cy], "--", color=color)
    sax.plot([cx, cx + R_o], [cy - R_o, cy - R_o], "--", color=color)
    fa = FancyArrowPatch(
        (cx + R_o - 50, cy),
        (cx + R_o - 50, cy - (R_o + 10)),
        color=color,
    )
    fa.set_arrowstyle("<|-|>", head_width=head_width, head_length=head_width * 2)
    sax.add_patch(fa)
    sax.annotate(
        "$R_o$", (cx + R_o - 330, cy - R_o / 2 + 100), color=color, fontsize=fontsize
    )

    # R_i
    sax.plot([cx, cx + R_i * 3], [cy - R_i, cy - R_i], "--", color=color)
    fa = FancyArrowPatch(
        (cx + R_i * 3 - 20, cy - 5),
        (cx + R_i * 3 - 20, cy - (R_i + 10)),
        color=color,
    )
    fa.set_arrowstyle("<|-|>", head_width=head_width, head_length=head_width * 2)
    sax.add_patch(fa)
    sax.annotate(
        "$R_i$",
        (cx + R_i * 3 + 50, cy - (R_i / 3 + 10)),
        color=color,
        fontsize=fontsize,
    )

    # R_c
    sax.plot([cx, cx + R_d * 3], [cy + R_d, cy + R_d], "--", color=color)
    arrow_len = 150
    fa = FancyArrowPatch(  # over
        (cx + R_d * 3 - 20, cy + 10),
        (cx + R_d * 3 - 20, cy - arrow_len),
        color=color,
    )
    fa.set_arrowstyle("<|-", head_width=head_width, head_length=head_width * 2)
    sax.add_patch(fa)
    fa = FancyArrowPatch(  # under
        (cx + R_d * 3 - 20, cy + R_d - 10),
        (cx + R_d * 3 - 20, cy + R_d - 10 + arrow_len),
        color=color,
    )
    fa.set_arrowstyle("<|-", head_width=head_width, head_length=head_width * 2)
    sax.add_patch(fa)
    sax.annotate(
        "$R_d$",
        (cx + R_d * 3 + 50, cy + (R_d + 150)),
        color=color,
        fontsize=fontsize,
    )

    c = Arc(center, R_o * 1.5, R_o * 1.5, angle=-88, theta1=-15, theta2=15, color=color)
    sax.add_patch(c)
    sax.annotate(
        r"$\theta$", (cx - 60, cy - R_o * 1.5 / 2 - 50), color=color, fontsize=fontsize
    )
    c = Arc(center, R_o, R_o, angle=-117, theta1=-15, theta2=15, color=color)
    sax.add_patch(c)
    ann_r = R_o / 2 + 50
    sax.annotate(
        r"$\theta$",
        (cx - 60 - ann_r * np.sin(pi / 6), cy - ann_r * np.cos(pi / 6)),
        color=color,
        fontsize=fontsize,
    )

    # Curved
    shift = 65
    center = (1355 - shift, 1157)
    cx, cy = center
    R_d = 1472 - 1355
    R_i = R_d * 2
    R_o = R_i * 5

    color = "yellow"
    fontsize = 16
    head_width = 1.5

    # R_o
    cax.plot([cx, cx], [cy, cy - R_o], "--", color=color)
    cax.plot([cx + R_o, cx + R_o], [cy, cy - R_o], "--", color=color)
    fa = FancyArrowPatch(
        (cx, cy - (R_o - 50)),
        (cx + (R_o + 10), cy - (R_o - 50)),
        color=color,
    )
    fa.set_arrowstyle("<|-|>", head_width=head_width, head_length=head_width * 2)
    cax.add_patch(fa)
    cax.annotate(
        "$R_o$", (cx + R_o / 2 - 100, cy - R_o + 250), color=color, fontsize=fontsize
    )

    # R_i
    cax.plot([cx + R_i, cx + R_i], [cy, cy - R_i * 3], "--", color=color)
    fa = FancyArrowPatch(
        (cx, cy - (R_i * 3 - 20)),
        (cx + R_i, cy - (R_i * 3 - 20)),
        color=color,
    )
    fa.set_arrowstyle("<|-|>", head_width=head_width, head_length=head_width * 2)
    cax.add_patch(fa)
    cax.annotate(
        "$R_i$",
        (cx + R_i / 3 - 20, cy - (R_i * 3) - 80),
        color=color,
        fontsize=fontsize,
    )

    # R_c
    cax.plot([cx - R_d, cx - R_d], [cy, cy - R_d * 3], "--", color=color)
    arrow_len = 150
    fa = FancyArrowPatch(  # right
        (cx, cy - (R_d * 3 - 40)),
        (cx + arrow_len, cy - (R_d * 3 - 40)),
        color=color,
    )
    fa.set_arrowstyle("<|-", head_width=head_width, head_length=head_width * 2)
    cax.add_patch(fa)
    fa = FancyArrowPatch(  # left
        (cx - (R_d - 10), cy - (R_d * 3 - 40)),
        (cx - (R_d - 10 + arrow_len), cy - (R_d * 3 - 40)),
        color=color,
    )
    fa.set_arrowstyle("<|-", head_width=head_width, head_length=head_width * 2)
    cax.add_patch(fa)
    cax.annotate(
        "$R_d$",
        (cx - (R_d + 150), cy - (R_d * 3 + 50)),
        color=color,
        fontsize=fontsize,
    )

    # Two theta annotation
    # c = Arc(center, R_o * 1.2, R_o * 1.2, angle=185, theta1=0, theta2=60, color=color)
    # cax.add_patch(c)
    # ann_r = R_o / 2 + 50
    # cax.annotate(
    #     r"$2\theta$",
    #     (
    #         cx + ann_r * np.sin((90 + 185 + 30) * pi / 180) - 350,
    #         cy - ann_r * np.cos((90 + 185 + 30) * pi / 180) - 50,
    #     ),
    #     color=color,
    #     fontsize=fontsize,
    # )

    # All this to get the stupid phi
    p1 = np.array([135 - shift, 1124])
    p2 = np.array([458 - shift, 1342])
    l1 = p2 - p1
    l1 = l1 / np.linalg.norm(l1)
    # cax.axline(p1, p2)

    p3 = np.array([1188 - shift, 977])
    p4 = np.array([1123 - shift, 1084])
    l2 = p4 - p3
    l2 = l2 / np.linalg.norm(l2)
    # cax.axline(p3, p4)

    center_2 = (820 - shift, 1586)

    cax.plot(*zip(p1, center_2, p3), color=color)
    square_size = 100
    p5 = center_2 - square_size * l1
    p6 = center_2 - square_size * l1 - square_size * l2
    p7 = center_2 - square_size * l2
    cax.plot(*zip(p5, p6, p7), color=color)

    cax.annotate(
        r"$\phi$",
        (700 - shift, 1360),
        color=color,
        fontsize=fontsize,
    )

    fig.tight_layout()
    plt.savefig("both_devices.png", dpi=300, bbox_inches="tight", pad_inches=0)
    plt.show()
    plt.close()


if __name__ == "__main__":
    main()
