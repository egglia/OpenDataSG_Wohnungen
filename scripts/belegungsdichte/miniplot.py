"""
This script plots some "miniplots" on top of the district boarders
"""
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np
from warnings import warn

from occupancy.quartier import Quartier, list_districts
from plot_lib.backgroundmap import plot_districts

LEGEND_COLOR_CATEGORY: list = [("blue", "Unterbelegt"),
                               ("lightgray", "Normalbelegt"),
                               ("red", "Überbelegt")]


def add_quartier_to_plt(ax: Axes,
                        quartier: Quartier) -> Axes:
    """
    Adds a new axis for the miniplot and puts it on top of the background
    :param ax: existing matplotlib axes with the background
    :param quartier:
    :return:
    """
    # Load the data regarding occupation values
    occupacy_df: pd.DataFrame = quartier.get_occupacy()

    # Check if there even exists data for that district
    if (occupacy_df["Normalbelegt"] == 0).all():
        warn(f"No data for {quartier.get_name()}. No miniplot generated")
        return None

    ax_mini = inset_axes(ax,
                         width=.5,
                         height=.5,
                         bbox_transform=ax.transData,
                         bbox_to_anchor=(quartier.get_coordinate_lon(),
                                         quartier.get_coordinate_lat()),
                         loc='center')
    ax_mini: Axes

    # plot the relative percentages
    years: np.ndarray = np.array(occupacy_df.index.tolist())
    bottom: list = np.zeros(len(years))
    WIDTH: float = 1.
    for color, category in LEGEND_COLOR_CATEGORY:
        normalbel: np.ndarray = np.array(occupacy_df[category].tolist())
        ax_mini.bar(years, normalbel, color=color, width=WIDTH, label=category, bottom=bottom)
        bottom += normalbel

    # Miniplot background transparency
    ax_mini.patch.set_alpha(.6)

    # Remove x ticks
    ax_mini.set_xticks([])
    ax_mini.set_yticks([])

    # Ax limits
    ax_mini.set_ylim([0, 1])
    ax_mini.set_xlim([years[0] - WIDTH/2, years[-1] + WIDTH/2])

    return ax_mini


fig, ax = plt.subplots()
ax: Axes

# plot the distric borders as background
plot_districts(ax)

districts: list = list_districts()

for quartier in districts:
    add_quartier_to_plt(ax, quartier)

# Polish plot
for color, label in reversed(LEGEND_COLOR_CATEGORY):
    ax.plot([0, 0], [0, 0], color=color, label=label)
ax.legend(loc="upper left")

ax.set_xticks([])  # Remove x ticks
ax.set_yticks([])
ax.set_frame_on(False)
plt.tight_layout()

plt.savefig("Belegung Wohnungen St.Gallen.png")
plt.savefig("Belegung Wohnungen St.Gallen.pdf")
plt.show()
