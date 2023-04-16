import unittest
from CityBikeImporter import CityBikeImporter


class TestGetRequests(unittest.TestCase):
    URL = 'https://wegfinder.at/api/v1/stations'
    ADDRESS_MOBILITY = 'https://api.i-mobility.at/routing/api/v1/nearby_address'
    testing_class = CityBikeImporter(URL)

    def test_get_data(self):
        response = self.testing_class.get_data()
        self.assertEqual(response.status_code, 200)

    def test_delete_attribute(self):
        method = self.testing_class.add_and_delete_attributes(['internal_id'])[0]
        self.assertNotIn('internal_id', method)

    def test_add_attribute(self):
        method = self.testing_class.add_and_delete_attributes([])[0]
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