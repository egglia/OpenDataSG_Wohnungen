from typing import List
import pandas as pd
import geopandas as gpd

from plot_lib.backgroundmap import get_districts_geojson
from occupancy.analyse import get_district_data


class Quartier():
    def __init__(self,
                 name: str,
                 lon: float,
                 lat: float):
        self._name: str = name
        self._lon: float = lon
        self._lat: float = lat

        self._occupancy = get_district_data(self._name)

    def get_name(self):
        return self._name

    def get_coordinate_lon(self):
        return self._lon

    def get_coordinate_lat(self):
        return self._lat

    def get_occupacy(self) -> pd.DataFrame:
        """
        :return: Dataframe with occupacy figures for all years. Includes relative percentages
        """
        return self._occupancy


def list_districts() -> List[Quartier]:
    # Returns a list of districts

    districts: list = list()
    geojson: gpd.geodataframe.GeoDataFrame = get_districts_geojson()

    for index, row in geojson.iterrows():
        name = index

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
