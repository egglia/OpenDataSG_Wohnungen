import unittest
from data.read_data import get_apartment_statistics_xlsx
from occupancy.quartier import list_districts


class TestQuartierNames(unittest.TestCase):
    """
    Test if the district names in the geojson match the xlsx names
    """

    def test_quartier_names_match(self):
        # Load statistics from Excel file
        statistics = get_apartment_statistics_xlsx()

        # Get unique quartier names from Excel
        xlsx_quartnames = statistics["Quartiersgruppe Name"].unique().tolist()

        # Get quartier names from GeoJSON
        districts = list_districts()
        geojson_name = [district.get_name() for district in districts]

        # Assert that quartier names match
        self.assertSetEqual(set(xlsx_quartnames), set(geojson_name))


if __name__ == '__main__':
    unittest.main()
