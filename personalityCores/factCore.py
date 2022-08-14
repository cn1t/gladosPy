import pywhatkit
import randfacts
import requests
from googletrans import Translator
from GoogleNews import GoogleNews

googlenews = GoogleNews()
translator = Translator()

googlenews.set_encode("utf-8")
googlenews.set_lang("de")
googlenews.set_period("1d")

def randomFact():
    """
    Description:
        Gets a random fact about anything

    Returns:
        - fact.text: The fact
    """
    en_fact = randfacts.get_fact()
    fact = translator.translate(en_fact, src="en", dest="de")

    print("[INFO-factCore/randomFact] Random fact has been generated.")

    return(fact.text)

def weatherFrog(city_name: str):
    """
    Parameters:
        - city_name: The name of the city

    Description:
        Gets the weather data for a specific city.

    Returns:
        - current_temperature: Temperature
        - current_humidity: Humidity
        - weather_desc.text: Description

        These infos are returned as a tuple.

        Usage:
            list_weather = weatherFrog()
            print(list_weather[0])

            - Replace 0 with the index of the item (0, 1, 2)
    """

    api_key = "8ef61edcf1c576d65d836254e11ea420"
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperatureone = y["temp"]
        current_humidiy = str(y["humidity"]) + "%"
        z = x["weather"]
        current_temperature = str(round(current_temperatureone - 273.15, 2)) + " Grad Celsius"
        en_weather_description = z[0]["description"]
        weather_desc = translator.translate(en_weather_description, src="en", dest="de")

        print(f"[INFO-factCore/weatherfrog] '{city_name}' has been checked and returned weather-information")

        return current_temperature, current_humidiy, weather_desc.text

def wikiSearch(to_search):
    """
    Parameters:
        - to_search: The subject

    Description:
        Searches wikipedia for the given subject.

    Returns:
        - wiki.text: The first two lines on the wikipedia article

        Usage:
            print(wikiSearches("dogs"))
    """
    en_wiki = pywhatkit.info(to_search, lines=2, return_value=True)
    wiki = translator.translate(en_wiki, src="en", dest="de")

    print(f"[INFO-factCore/wikiSearch] Subject '{to_search}' has researched and returned information")

    return(wiki.text)