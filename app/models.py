import requests
import datetime
import matplotlib.pyplot as plt

from config import WEATHER_API_KEY


def get_JSON(url: str):
    """
    Fetch JSON data from the provided URL and return it as a Python dictionary.

    Args:
        url (str): The URL to fetch JSON data from.

    Returns:
        dict: A Python dictionary containing the JSON data.
    """
    return requests.get(url).json()

def unix_to_datetime(unix: int):
    """
    Convert a Unix timestamp to a Python datetime object.

    Args:
        unix (int): The Unix timestamp to convert.

    Returns:
        datetime.datetime: A Python datetime object.
    """
    return datetime.datetime.fromtimestamp(unix)

def get_api_data(city_name):
    """
    Retrieve weather data from the OpenWeatherMap API for a specific city.

    Args:
        city_name (str): The name of the city for which to retrieve weather data.

    Returns:
        list: A list of weather data instances for the specified city.
    """
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={WEATHER_API_KEY}&units=metric'
    weather = get_JSON(url)
    return weather['list']

def get_icon_url(icon_id:str):
    return f'https://openweathermap.org/img/wn/{icon_id}@2x.png'

def get_current_weather(city_name: str):
    """
    Retrieve the current weather data for a specific city.

    Args:
        city_name (str): The name of the city for which to retrieve current weather data.

    Returns:
        tuple: A dictionary containing the current weather data for the spescified city, a string of the currrnt condition desctiption
         and a url of the icon for that weather condition.
    """
    weather_data = get_api_data(city_name)
    condition = weather_data[0]['weather'][0]['description']
    icon_id = weather_data[0]['weather'][0]['icon']
    return weather_data[0]['main'], condition, get_icon_url(icon_id), 

def times_and_temps(city_name: str):
    """
    Retrieve and process weather data for a specific city and return it as a zipped collection.

    Args:
        city_name (str): The name of the city for which to retrieve weather data.

    Returns:
        zip: A zipped collection of date and time, temperature, feels-like temperature, min temperature, max temperature, and weather description.
    """
    weather_data_list = get_api_data(city_name)
    dts = [unix_to_datetime(weather_data_instance['dt']) for weather_data_instance in weather_data_list]
    temps = [weather_data_instance['main']['temp'] for weather_data_instance in weather_data_list]
    feels_likes = [weather_data_instance['main']['feels_like'] for weather_data_instance in weather_data_list]
    temp_mins = [weather_data_instance['main']['temp_min'] for weather_data_instance in weather_data_list]
    temp_maxs = [weather_data_instance['main']['temp_max'] for weather_data_instance in weather_data_list]
    weathers = [weather_data_instance['weather'][0]['description'] for weather_data_instance in weather_data_list]

    return zip(dts, temps, feels_likes, temp_mins, temp_maxs, weathers)


def temp_graph(city_name: str):
    weather_data_list = get_api_data(city_name)
    dts = [unix_to_datetime(weather_data_instance['dt']) for weather_data_instance in weather_data_list]
    temps = [weather_data_instance['main']['temp'] for weather_data_instance in weather_data_list]

    # Create a line graph
    plt.figure(figsize=(10, 6))
    plt.plot(dts, temps, marker='o', linestyle='-', color='b')
    plt.title(f'Temperature Over Time for {city_name.capitalize()}')
    plt.xlabel('Date and Time')
    plt.ylabel('Temperature (°C)')
    plt.grid(True)

    # Customize the x-axis labels for readability
    # plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_formatter(plt.FixedFormatter([str(dt.strftime('%Y-%m-%d %H:%M')) for dt in dts]))

    # Save the graph as an image file (e.g., PNG)
    plt.savefig('app/static/img/temperature_graph.png')


def get_city_pictures(city_name: str):
    url = f'https://api.teleport.org/api/urban_areas/slug:{city_name.lower()}/images/'
    # print(requests.get(url))
    links = get_JSON(url)
    img_url = links['photos'][0]['image']['web']
    return img_url
