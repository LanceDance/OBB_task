import time
import requests
import json


def mark_methods(cls):
    """
    decorator takes the class and "decorate" all methods with error handling function error_handler
    :param cls:
    :return: cls
    """
    method_list = [func for func in dir(cls) if callable(getattr(cls, func)) and not func.startswith("__")]
    for method_name in method_list:
        method = getattr(cls, method_name)
        setattr(cls, method_name, error_handler(method))
    return cls


def error_handler(method):
    """
    working funtion in main decorator checking for bugs... super handy if you need to write logs somewhere and
    you don't need to create catcher for every method
    :param method:
    :return:
    """
    def wrapped_method(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except Exception as e:
            print(f"Error in {method.__name__}: {e}")
            raise

    return wrapped_method


@mark_methods
class CityBikeImporter:
    def __init__(self, url):
        self.url = url
        self.data = self.get_data().json()

    def get_data(self) -> json:
        """
        :return: response with working data
        """
        try:
            response = requests.get(self.url, headers={'Accept': 'application/json'})
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return response

    def add_and_delete_attributes(self, list_of_atrribute_to_delete: list) -> list:
        """
        because one of the task was to change the structure of the response I did in and I re
        :param list_of_atrribute_to_delete:
        :return: modified results
        """
        for i in self.data:
            i.update({"coordinate": [i['longitude'], i['latitude']]})
            i.update({'free_ratio': i['free_boxes'] // i['boxes']})
            i.update({'active': True}) if i['status'] == 'aktiv' else None
            for attribute_to_delete in list_of_atrribute_to_delete:
                del i[attribute_to_delete]
        return self.data

    def filter_bikes(self) -> list:
        """
        remove data if they had no free bikes
        :return: modified results
        """
        self.data = [self.data[i] for i, j in enumerate(self.data) if j['free_bikes'] != 0]
        return self.data

    def sort_result(self) -> list:
        """
        just sort the data free bikes descending, if two stations have  the same number of bikes, sort by name ascending.
        :return: modified results
        """
        self.data = sorted(self.data, key=lambda d: (-d['free_bikes'],
                                                     d['name'].casefold().translate(str.maketrans("", "", "äöü"))))
        return self.data

    def add_new_address(self, address_endpoint: str, time_for_sleep_if_429=5) -> list:
        """
        :param address_endpoint:
        :param time_for_sleep_if_429: sometimes happens that server disconnect call because of 429, so if that happens
        then wait a while and then run last element again
        :return: modified results
        """
        time_for_sleep_if_429 = 5 if time_for_sleep_if_429 < 5 else None
        for i in self.data:
            try:
                address = requests.get(f'{address_endpoint}?latitude={i["coordinate"][1]}&longitude={i["coordinate"][0]}',
                                   headers={'Accept': 'application/json'})
                i.update({'address': address.json()['data']['name']})
            except requests.exceptions.JSONDecodeError:
                    time.sleep(time_for_sleep_if_429)
                    address = requests.get(
                        f'{address_endpoint}?latitude={i["coordinate"][1]}&longitude={i["coordinate"][0]}',
                        headers={'Accept': 'application/json'})
                    i.update({'address': address.json()['data']['name']})

                    continue
            except requests.exceptions.RequestException as e:
                    raise SystemExit(e)

        return self.data

