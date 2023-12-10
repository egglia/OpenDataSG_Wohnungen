from os.path import abspath, dirname, join, isfile
import pandas as pd


def _get_data_dir() -> str:
    return abspath(dirname(__file__))


def get_apartment_statistics_xlsx() -> pd.DataFrame:
    xlsx: str = abspath(join(_get_data_dir(),
                             "belegung-neu-erstellter-wohnungen-2011-2019.xlsx"))
    assert isfile(xlsx)

    df: pd.DataFrame = pd.read_excel(xlsx)
    # Replace the "Quartiergruppe " prefix from column "F"
    df['Quartiersgruppe Name'] = df['Quartiersgruppe Name'].str.replace('Quartiergruppe ', '')
    df['Quartiersgruppe Name'] = df['Quartiersgruppe Name'].str.replace('Linsebühl', 'Linsenbühl')
    df['Quartiersgruppe Name'] = df['Quartiersgruppe Name'].str.replace(' - ', '-')
    return df
