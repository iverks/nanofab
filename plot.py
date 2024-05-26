import discretisedfield as df
import matplotlib.font_manager as fm
import matplotlib.patheffects as patheffects
import matplotlib.pyplot as plt
import micromagneticmodel as mm
import numpy as np
import oommfc as oc
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar

filename = "center_B=1mT_mag"
read_field = df.Field.from_file(f"data/{filename}.ovf")


fig, ax = plt.subplots()
# Plots arrows. Change number in resample to reduce
read_field.sel("z").resample(n=(50, 50)).mpl.vector(
    ax=ax,
    multiplier=1e-6,
    color="w",
    use_color=False,
    colorbar=False,
    scale=50,
)

# Plots the z component as an image, kinda like an MFM image
read_field.sel("z").z.mpl.scalar(ax=ax, multiplier=1e-6, symmetric_clim=True)
ax.axis("off")
plt.savefig(f"plots/{filename}.png")
plt.show()
