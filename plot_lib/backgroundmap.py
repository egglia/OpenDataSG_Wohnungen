import geopandas as gpd
import matplotlib.pyplot as plt
from os.path import abspath, isfile, join, dirname


def get_districts_geojson() -> gpd.geodataframe.GeoDataFrame:
    """
    Loads the geojson file content.
    Since the original file contains about 30 polygons (reflecting sub-districts),
    the information is aggregated to 14 "master" districts.
    This then also matches the districts from https://stada2.sg.ch/
    :return: GeoDataFrame with 14 districts
    """
    data_dir = abspath(dirname(__file__))
    fname = "wohnviertel_stadt-stgallen.geojson"
    geojson_file = abspath(join(data_dir, fname))
    assert isfile(geojson_file)
    geojson_file = gpd.read_file(geojson_file)
    # Perform a spatial dissolve based on the "Quartiergr" column
    dissolved_gdf = geojson_file.dissolve(by="quartiergr", aggfunc="first")
    return dissolved_gdf


def plot_districts(ax):
    # Add the district border to an existing matplotlib axis

    gdf = get_districts_geojson()  # Contains one polygon per district

    gdf.plot(ax=ax, color='none', edgecolor='darkgray', alpha=1)

    # Set the extent based on the bounding box of the GeoJSON file
    extent = [gdf.bounds.minx.min(), gdf.bounds.maxx.max(),
              gdf.bounds.miny.min(), gdf.bounds.maxy.max()]
    ax.set_xlim(extent[0], extent[1])
    ax.set_ylim(extent[2], extent[3])


if __name__ == "__main__":
    # Plots the district boarders without any additional items
    gdf = get_districts_geojson()

    # List "kreis," "quartiergr," and "statistisc" for all entries
    for i, (index, row) in enumerate(gdf.iterrows()):
        print(
            f"Index: {i, index}, "
            f"Nummer: {row['nummer']}, "
            f"Kreis: {row['kreis']}, "
            f"Statistisc: {row['statistisc']}")

    # Plot the geometries
    fig, ax = plt.subplots()
    plot_districts(ax)
    plt.show()
