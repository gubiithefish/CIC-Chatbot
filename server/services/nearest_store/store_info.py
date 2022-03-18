# import required modules
from math import sin, cos, sqrt, asin, radians
from decouple import config
from pathlib import Path
import requests
import unittest
import json

# Configuration variables
weather_api_key = config('OPENWEATHERAPIKEY')


def _json_file_to_list(file_string: str) -> list:
    """Local method to retrieve content of JSON files in the directory of this method"""
    directory = Path(__file__).parent
    json_path = directory.joinpath(file_string)

    # Using the "with open()" method as closing the file is done
    # internally when leaving the "with" statement.
    with open(json_path, encoding='utf-8') as json_file:
        return json.load(json_file)


def _url_get_json_response(url: str) -> dict:
    """Local method that attempts to return the GET response as a dict,
    if the response is a list, it will take the first element of that list"""
    response = requests.get(url).json()

    if isinstance(response, list) and len(response) == 1:
        if isinstance(response[0], dict):
            return response[0]

    elif isinstance(response, dict):
        return response

    else:
        raise TypeError("The GET response is neither a dictionary nor a list with a single dictionary element")


def get_closest_store(lat_customer: float, lon_customer: float, api_response: bool = False) -> dict:
    """Determine which store location is closest to the customer"""
    locations = _json_file_to_list("store_locations.json")
    shop_dist = {"name": None, "dist": float}

    for location in locations:
        info = list(location.values())[0]
        calc = calculate_distance(lat_customer, lon_customer, info['lat'], info['lon'])

        if shop_dist['name'] is None:
            shop_dist.update({'name': info["name"], 'dist': calc})

        elif calc < shop_dist['dist']:
            shop_dist.update({'name': info["name"], 'dist': calc})

    if api_response is False:
        return shop_dist
    else:
        return {"msg": f"Den nærmeste butik fra din by ligger i {shop_dist['name']} " +
                       f"med {shop_dist['dist']} kilometers afstand i fuglelinje",
                "data": shop_dist}


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculating the great-circle distance between two points (specified
    in decimal degrees) on a sphere using the Haversine formula"""
    # longitudes and latitudes conversion to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Apply the haversine formula
    a = sin((lat2 - lat1) / 2) ** 2
    b = cos(lat1) * cos(lat2)
    c = sin((lon2 - lon1) / 2) ** 2
    R = 6371.0
    distance = 2 * R * asin(sqrt(a + b * c))

    return round(distance, 1)


def get_weather_forecast(city: str, api_response=False) -> dict:
    lat, lon = get_coordinates(city)
    url_base = f"https://api.openweathermap.org/data/2.5/onecall"
    url_args = f"?lat={lat}&lon={lon}&exclude=minutely,hourly&units=metric&appid={weather_api_key}"
    url_full = url_base + url_args
    response = _url_get_json_response(url_full)

    # Select specific key:value pairs from json response
    weather_now = response['current']
    weather_day = response['daily'][0]
    forecast = {
        "currently": {
            "temp": weather_now['temp'],
            "feels_like": weather_now['feels_like'],
            "humidity": weather_now['humidity'],
            "wind_speed": weather_now['wind_speed'],
            "weather_desc": weather_now['weather'][0]['description'],
            "weather_icon": f"https://openweathermap.org/img/wn/{weather_now['weather'][0]['icon']}@2x.png",
        },
        "today": {
            "min_temp": weather_day['temp']['min'],
            "max_temp": weather_day['temp']['max'],
            "avg_wind": weather_day['wind_speed'],
            "max_wind": weather_day['wind_gust'],
        }
    }

    if api_response is False:
        return forecast
    else:
        return {"msg": f"Temperaturen for {city} vil i dag svinge mellem {forecast['today']['min_temp']} og " +
                       f"{forecast['today']['max_temp']} grader 🌡, med en gennemsnitlig blæst på " +
                       f"{forecast['today']['avg_wind']} km/t og vindstød op til {forecast['today']['max_wind']} " +
                       f"km/t 💨. Til gengæld er der lige nu {forecast['currently']['temp']} grader, en " +
                       f"gennemsnitlig blæst på {forecast['currently']['wind_speed']} km/t og en fugtighed på " +
                       f"{forecast['currently']['humidity']}% 🌈",
                "data": forecast}


def get_coordinates(city: str) -> list:
    """Get coordinates for one given city located in Denmark"""
    url_base = f"http://api.openweathermap.org/geo/1.0/direct"
    url_args = f"?q={city},Denmark&limit=1&appid={weather_api_key}"
    url_full = url_base + url_args
    response = _url_get_json_response(url_full)
    return [response['lat'], response['lon']]


#
#
#
#


class TestDataCollection(unittest.TestCase):
    # _url_get_json_response
    def setUp(self):
        self.get_argument1 = "http://ip.jsontest.com/"
        self.get_argument2 = "htt:/d.c"
        self.get_argument3 = "https://jsonplaceholder.typicode.com/comments?postId=1"

    def test_assert_is_instance(self):
        self.assertIsInstance(_url_get_json_response(self.get_argument1), dict)

    @unittest.expectedFailure
    def test_expected_failure_wrong_url(self):
        self.assertIsInstance(_url_get_json_response(self.get_argument2), dict)

    @unittest.expectedFailure
    def test_expected_failure_dicts_in_list(self):
        self.assertIsInstance(_url_get_json_response(self.get_argument3), dict)

    # _json_file_to_list
    def test_url_get_json_response(self):
        self.assertIsInstance(_json_file_to_list("store_locations.json"), list)


class TestAPIMethods(unittest.TestCase):
    def test_location_is_instance(self):
        self.assertIsInstance(get_weather_forecast("Aarhus"), dict)

    def test_weather_is_instance(self):
        self.assertIsInstance(get_coordinates("Aarhus"), list)

    @unittest.expectedFailure
    def test_weather_forecast_city_outside_denmark(self):
        self.assertIsInstance(get_weather_forecast("New York"), dict)

    @unittest.expectedFailure
    def test_weather_forecast_coordinates_outside_denmark(self):
        self.assertIsInstance(get_coordinates("New York"), list)


class TestCalculationMethods(unittest.TestCase):
    @staticmethod
    def determine(lat, lon):
        return get_closest_store(lat, lon)

    @staticmethod
    def calc_dist(lat1, lon1, lat2, lon2):
        return calculate_distance(lat1, lon1, lat2, lon2)

    def setUp(self):
        self.store_AAL = [56.6352382, 9.1404871]
        self.store_AAH = [56.1836560, 10.097648]
        self.store_CPH = [55.8280745, 8.7169946]

    def test_calculate_is_equal(self):
        self.assertEqual(self.calc_dist(50, 10, -50, 10), 11119.5)

    def test_closest_store_is_equal(self):
        self.assertEqual(self.determine(56.6352382, 9.1404871)['name'], 'Bauhaus Aalborg')


if __name__ == '__main__':
    unittest.main()
    # print(get_coordinates("Copenhagen"))
    # x,y = get_coordinates("Copenhagen")
    # print(get_closest_store(x,y))
