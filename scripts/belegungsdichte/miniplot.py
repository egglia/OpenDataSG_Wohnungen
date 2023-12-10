"""
This script plots some "miniplots" on top of the district boarders
"""

from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from plot_lib.backgroundmap import plot_districts, Quartier, list_districts


def add_quartier_to_plt(ax: Axes,
                        quartier: Quartier) -> Axes:
    """
    Adds a new axis for the miniplot and puts it on top of the background
    :param ax: existing matplotlib axes with the background
    :param quartier:
    :return:
    """
    ax_mini = inset_axes(ax,
                         width=.5,
                         height=.5,
                         bbox_transform=ax.transData,
                         bbox_to_anchor=(quartier.get_coordinate_lon(),
                                         quartier.get_coordinate_lat()),
                         loc='center')
    ax_mini: Axes

    # Miniplot background transparency
    ax_mini.patch.set_alpha(.6)

    # Remove x ticks
    ax_mini.set_xticks([])
    ax_mini.set_yticks([])

    # Add some dummy data for now
    ax_mini.bar([2020, 2021], [10, 20], width=.7, label="UB", bottom=[0, 0])

    return ax_mini


fig, ax = plt.subplots()
ax: Axes

# plot the distric borders as background
plot_districts(ax)

districts: list = list_districts()

for quartier in districts:
    add_quartier_to_plt(ax, quartier)

plt.savefig("Belegung Wohnungen St.Gallen.png")
plt.savefig("Belegung Wohnungen St.Gallen.pdf")
plt.show()
