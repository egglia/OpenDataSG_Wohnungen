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
                               ("darkgoldenrod", "Überbelegt")]
FRONTSIZE: float = 8.


def add_quartier_to_plt(ax: Axes,
                        quartier: Quartier or None) -> Axes:
    """
    Adds a new axis for the miniplot and puts it on top of the background
    :param ax: existing matplotlib axes with the background
    :param quartier:
    :return:
    """
    # Load the data regarding occupation values
    if quartier is None:  # Load data for whole city
        occupacy_df: pd.DataFrame = Quartier.get_occupacy_all_districts()

        ax_mini = inset_axes(ax,
                             width="30%",
                             height="30%",
                             bbox_transform=ax.transAxes,
                             bbox_to_anchor=(0.07, 0, 1, 1),
                             loc='upper left')

        ax_mini.set_xticks([2011, 2015, 2019])
        ax_mini.set_yticks([0, .5, 1.], ["0%", "50%", "100%"])
        ax_mini.tick_params(axis='both', labelsize=FRONTSIZE)
        ax_mini.set_title("Total aller St.Galler Quartiere",
                          fontsize=FRONTSIZE, pad=6)

    else:  # Load data for only one single district
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

        # Remove x ticks
        ax_mini.set_xticks([])
        ax_mini.set_yticks([])
        ax_mini.set_title(quartier.get_name().replace("-", "-\n"),
                          fontsize=FRONTSIZE, pad=3)
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
    ax_mini.patch.set_alpha(0.)

    # Ax limits
    ax_mini.set_ylim([0, 1])
    ax_mini.set_xlim([years[0] - WIDTH/2, years[-1] + WIDTH/2])

    if quartier is None:
        # add a legend, but only for the whole city plot
        # Reverse the order of handles and labels
        handles, labels = ax_mini.get_legend_handles_labels()
        handles = handles[::-1]
        labels = labels[::-1]
        ax_mini.legend(handles, labels,
                       loc='upper center',
                       bbox_to_anchor=(0.5, -0.2),
                       fontsize=FRONTSIZE)

    return ax_mini


fig, ax = plt.subplots()
ax: Axes

# plot the distric borders as background
plot_districts(ax)

districts: list = list_districts()

# Add 'None' to districts list: Top left plot for the whole city
districts.append(None)

for quartier in districts:
    add_quartier_to_plt(ax, quartier)

# Polish plot
ax.set_xticks([])  # Remove x ticks
ax.set_yticks([])
ax.set_title("Belegung der Neuwohnungen in der Stadt St. Gallen",
             fontsize=FRONTSIZE+2, pad=15)
ax.set_frame_on(False)
plt.tight_layout()

plt.savefig("Belegung Wohnungen St.Gallen.png", dpi=450)
plt.savefig("Belegung Wohnungen St.Gallen.pdf")
plt.show()
