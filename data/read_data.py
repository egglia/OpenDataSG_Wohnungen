from os.path import abspath, dirname


def _get_data_dir() -> str:
    return abspath(dirname(__file__))
