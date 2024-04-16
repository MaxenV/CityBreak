import requests
import re
from . import wordManip as wp


class GUSService:
    def __init__(self, apiKey=""):
        self.word_manip = wp.WordManip()

        if apiKey:
            self.apiKey = apiKey
            print("API Key is set")

    def getUnitIdFromCity(self, cityName):
        url = f"https://bdl.stat.gov.pl/api/v1/units/search"
        nomCity = self.word_manip.to_nominative(cityName).lower()
        params = {
            "name": nomCity,
            "format": "json",
            "unit-level": "6",
            "page-size": "40",
        }
        response = requests.get(url, params=params)
        regex = "m.st.*warszawa.*od|(miasto$)"

        dataUnit = self.__checkResponse(response)

        if len(dataUnit["results"]) == 0:
            raise Exception(f"Nie znaleziono miasta {cityName}")
        else:
            res = self.__firstCityId(dataUnit["results"], regex)
            return res

    def getPopulationOfCity(self, unitId):
        url = "https://bdl.stat.gov.pl/api/v1/data/by-variable/72305"
        params = {
            "unit-level": "6",
            "unit-parent-id": unitId,
            "format": "json",
        }

        response = requests.get(url, params=params)
        dataPopulation = self.__checkResponse(response)

        if len(dataPopulation["results"]) == 0:
            raise Exception(f"Nie znaleziono miasta o id: {unitId}")
        else:
            return self.__firstCityPopulation(dataPopulation["results"], unitId)

    def __firstCityId(self, data, regex):
        for item in data:
            if item["id"][-2] != "0" and item["id"][-1] != "0":
                if len(item["name"].split(" ")) > 3 and re.search(
                    regex, item["name"].lower()
                ):
                    return item["id"]
                elif len(item["name"].split(" ")) <= 3:
                    return item["id"]
        return None

    def __firstCityPopulation(self, data, unitId):
        for item in data:
            if unitId == item["id"]:
                result = item["values"]
                result.reverse()
                return result[0]["val"]
        return None

    def __checkResponse(self, response):
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Błąd żądania: {response.status_code}")
