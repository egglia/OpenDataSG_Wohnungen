import pandas as pd

from data.read_data import get_apartment_statistics_xlsx

STATISTICS: pd.DataFrame = get_apartment_statistics_xlsx()
YEARS: list = sorted(STATISTICS['Belegungsjahr'].unique().tolist())


def get_district_data(district_name: str or None):
    """
    Extract the relevant data from the excel in the .data folder.
    :param district_name: Name of district (or 'None' for ALL districts in the city)
    :return:
    """

    data: pd.DataFrame = pd.DataFrame(index=YEARS)
    for year in data.index:
        # Extract the relevant year
        filtered_data = STATISTICS[STATISTICS['Belegungsjahr'] == year]

        # If requested, further filtering for just one district
        if district_name is not None:
            assert district_name in STATISTICS["Quartiersgruppe Name"].unique().tolist()
            filtered_data = filtered_data[filtered_data['Quartiersgruppe Name'] == district_name]

        count_normaloccup: int = 0  # Normalbelegung
        count_overoccup: int = 0  # Anzahl Wohnungen mit Überbelegung
        count_underoccup: int = 0  # Unterbelegung

        for _, row in filtered_data.iterrows():
            # each row correponds to one appartement
            count_rooms: int = row['Wohnungsgroesse']  # number of rooms in that appartement
            count_inhabitants: int = row['Anz_Kinder'] + row['Anz_Erwachsene']
            if count_inhabitants + 1 == count_rooms:  # Normalbel.: Anz. Zi = Anz. Bewohner + 1
                count_normaloccup += 1
            elif count_inhabitants + 1 > count_rooms:  # Überbelegung
                count_overoccup += 1
            elif count_inhabitants + 1 < count_rooms:  # Unterbelegung
                count_underoccup += 1

        # Store relative numbers in dataframe
        count_all: int = count_normaloccup + count_overoccup + count_underoccup
        data.loc[year, "Anz. Whnh"] = count_all
        if count_all <= 50:
            # Overwrite percentages if number of appartements is very small
            count_normaloccup = count_overoccup = count_underoccup = 0
            count_all = max(count_all, 1)  # to avoid division by zero if absolutely no data
        data.loc[year, "Normalbelegt"] = float(count_normaloccup) / count_all
        data.loc[year, "Überbelegt"] = float(count_overoccup) / count_all
        data.loc[year, "Unterbelegt"] = float(count_underoccup) / count_all

    return data


if __name__ == "__main__":
    print(get_district_data("Lachen"))
