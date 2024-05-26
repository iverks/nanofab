from pathlib import Path

# pip install ubermag
import discretisedfield as df
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

cur_dir = Path(__file__).parent


def main(filename="B=3mT"):
    read_field = df.Field.from_file(cur_dir / f"petal.out/{filename}.ovf")

    x0 = np.equal(read_field.sel("z").x, 0)
    y0 = np.equal(read_field.sel("z").y, 0)
    z0 = np.equal(read_field.sel("z").z, 0)
    ff: df.Field = np.logical_not(np.logical_and(x0, y0, z0))

    fig, ax = plt.subplots()
    ax: Axes = ax
    # # Plots arrows. Change number in resample to reduce
    read_field.sel("z").resample(n=(15, 15)).mpl.vector(
        ax=ax,
        multiplier=1e-6,
        color="k",
        use_color=False,
        colorbar=False,
        scale=15,
    )

    # Plots the z component as an image, kinda like an MFM image
    # read_field.sel("z").z.mpl.scalar(
    #     ax=ax,
    #     multiplier=1e-6,
    #     cmap="PuOr",
    #     symmetric_clim=True,
    #     filter_field=ff,
    # )

    # Plot directions as colors
    read_field.sel("z").mpl.lightness(
        ax=ax,
        multiplier=1e-6,
        filter_field=ff,
        colorwheel=None,
    )

    ax.axis("off")
    fig.savefig(
        cur_dir / f"pfigs/{filename}.png",
        bbox_inches="tight",
        pad_inches=0,
        dpi=300,
    )
    # plt.show()
    plt.close()


if __name__ == "__main__":
    for B in [-3, -1, 0, 1, 3, 5]:
        filename = f"B={B}mT"
        main(filename)
