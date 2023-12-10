import geopandas as gpd
import matplotlib.pyplot as plt
from os.path import abspath, isfile, join, dirname
from typing import List


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

    gdf.plot(ax=ax, color='none', edgecolor='black')

    # Set the extent based on the bounding box of the GeoJSON file
    extent = [gdf.bounds.minx.min(), gdf.bounds.maxx.max(),
              gdf.bounds.miny.min(), gdf.bounds.maxy.max()]
    ax.set_xlim(extent[0], extent[1])
    ax.set_ylim(extent[2], extent[3])


class Quartier():
    def __init__(self,
                 name: str,
                 lon: float,
                 lat: float):
        self._name: str = name
        self._lon: float = lon
        self._lat: float = lat

    def get_name(self):
        return self._name

    def get_coordinate_lon(self):
        return self._lon

    def get_coordinate_lat(self):
        return self._lat


def list_districts() -> List[Quartier]:
    # Returns a list of districts

    districts: list = list()
    geojson: gpd.geodataframe.GeoDataFrame = get_districts_geojson()

    for index, row in geojson.iterrows():
        name = row['statistisc']

        # Assuming 'geometry' is a Polygon or MultiPolygon
        if row['geometry'].geom_type == 'Polygon':
            centroid = row['geometry'].centroid
            lon, lat = centroid.x, centroid.y
        elif row['geometry'].geom_type == 'MultiPolygon':
            # Use the centroid of the first polygon in the MultiPolygon
            centroid = row['geometry'].geoms[0].centroid
            lon, lat = centroid.x, centroid.y
        else:
            # Handle other geometry types as needed
            lon, lat = None, None

        district = Quartier(name, lon, lat)
        districts.append(district)

    return districts


if __name__ == "__main__":
    # Plots the district boarders without any additional items
    gdf = get_districts_geojson()

    # List "kreis," "quartiergr," and "statistisc" for all entries
    for i, (index, row) in enumerate(gdf.iterrows()):
        print(
            f"Index: {i, index}, "
            f"Kreis: {row['kreis']}, "
            f"Statistisc: {row['statistisc']}")

    # Plot the geometries
    fig, ax = plt.subplots()
    plot_districts(ax)
    plt.show()