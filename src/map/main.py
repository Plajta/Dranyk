# imports
from os.path import join
from pathlib import Path

# relative imports
from data_utils import GeoJSONreader

ABS_PATH = str(Path(__file__).parents[2])
DATA_PATH = join(ABS_PATH, "data")

if __name__ == "__main__":
    gjson_reader = GeoJSONreader(DATA_PATH)
    data = gjson_reader.read_data()
    # Like bols