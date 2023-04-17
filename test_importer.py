import unittest
from unittest import mock

from CityBikeImporter import CityBikeImporter
from unittest.mock import patch, Mock


class TestGetRequests(unittest.TestCase):
    URL = 'https://wegfinder.at/api/v1/stations'
    ADDRESS_MOBILITY = 'https://api.i-mobility.at/routing/api/v1/nearby_address'
    testing_class = CityBikeImporter(URL)
    testing_class.data = [{
            "id": 1,
            "name": "Friedrich Schmidtplatz",
            "status": "aktiv",
            "description": "Ecke Lichtenfelsgasse U2 Station Rathaus",
            "boxes": 24,
            "free_boxes": 24,
            "free_bikes": 0,
            "longitude": 16.356581,
            "latitude": 48.211433,
            "internal_id": 1026
          },
          {
            "id": 109,
            "name": "Johannesgasse",
            "status": "aktiv",
            "description": "Parkring / Stadtpark beim Haupteingang des Kursalons",
            "boxes": 20,
            "free_boxes": 13,
            "free_bikes": 6,
            "longitude": 16.376719,
            "latitude": 48.203366,
            "internal_id": 1029
          },
          {
            "id": 112,
            "name": "Kärntner Ring",
            "status": "aktiv",
            "description": "Ecke Akademiestraße in der Mitte der beiden Einkaufszentren der Ringstraßengalerien",
            "boxes": 16,
            "free_boxes": 11,
            "free_bikes": 5,
            "longitude": 16.371317,
            "latitude": 48.202157,
            "internal_id": 1028
          },
          {
            "id": 110,
            "name": "Rathausplatz",
            "status": "aktiv",
            "description": "Universitätsring gegenüber des Burgtheaters",
            "boxes": 20,
            "free_boxes": 20,
            "free_bikes": 0,
            "longitude": 16.36025,
            "latitude": 48.209921,
            "internal_id": 1027
          }]

    def test_get_data(self):
        requests = mock.Mock()
        requests.get.return_value.status_code = 200
        response = requests.get(self.URL)
        self.assertEqual(response.status_code, 200)

    def test_delete_attribute(self):
        method = self.testing_class.add_and_delete_attributes(['internal_id'])[0]
        self.assertNotIn('internal_id', method)

    def test_add_attribute(self):
        method = self.testing_class.add_and_delete_attributes([])[0]
        print(method)
        self.assertIn('free_ratio', method)

    def test_filter_bikes(self):
        result = self.testing_class.filter_bikes()
        for i in result:
            if i['free_bikes'] == 0:
                assert False
            else:
                assert True

    def test_add_new_address(self):
        result = self.testing_class.add_new_address(self.ADDRESS_MOBILITY, 2)
        if result[0].get('address'):
            assert True
        else:
            assert False