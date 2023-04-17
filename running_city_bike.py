import json
import pprint
from CityBikeImporter import CityBikeImporter


if __name__ == '__main__':
    station_data_class = CityBikeImporter('https://wegfinder.at/api/v1/stations')
    station_data_class.get_data()
    station_data_class.add_and_delete_attributes(['longitude', 'latitude', 'status', 'internal_id'])
    station_data_class.filter_bikes()
    station_data_class.sort_result()
    pprint.pprint(station_data_class.data, indent=4, sort_dicts=False)
    station_data_class.add_new_address('https://api.i-mobility.at/routing/api/v1/nearby_address', 1)
    print(f'Final list:\n')
    pprint.pp(pprint.pprint(station_data_class.data), indent=4, sort_dicts=False)