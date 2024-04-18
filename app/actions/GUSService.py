import requests
import re


class GUSService:
    def __init__(self, apiKey=""):

        if apiKey:
            self.apiKey = apiKey
            print("API Key is set")

    def getUnitIdFromCity(self, nomCity):
        url = f"https://bdl.stat.gov.pl/api/v1/units/search"
        nomCity = nomCity.lower()
        params = {
            "name": nomCity,
            "format": "json",
            "unit-level": "6",
            "page-size": "99",
        }

        dataUnit = self.__getDataResponse(url, params)

        if len(dataUnit["results"]) == 0:
            raise Exception(f"No results")
        else:
            res = self.__readCityId(dataUnit["results"], nomCity)
            if res is None:
                raise Exception(f"The search was not matched")

            return res

    def getProvinceFromUnitId(self, unitId):
        provinceId = unitId[:4] + ("0" * len(unitId[4:]))

        url = f"https://bdl.stat.gov.pl/api/v1/units/{provinceId}"
        dataUnit = self.__getDataResponse(
            url,
            {
                "format": "json",
            },
        )

        print("Type DataUnit: ", type(dataUnit))  # DEBUG
        if "errors" in dataUnit:
            raise Exception(f"Province not found.")
        else:
            return self.__normalizeProvinceName(dataUnit["name"])

    def getPopulationOfCity(self, unitId):
        print("UnitId: ", unitId)  # DEBUG
        url = "https://bdl.stat.gov.pl/api/v1/data/by-variable/72305"
        params = {
            "unit-level": "6",
            "unit-parent-id": unitId,
            "format": "json",
            "page-size": "99",
        }

        dataPopulation = self.__getDataResponse(url, params)

        if len(dataPopulation["results"]) == 0:
            raise Exception(f"City not found.")
        else:
            return self.__readCityPopulation(dataPopulation["results"], unitId)

    def __readCityId(self, data, cityName):
        for item in data:
            lowerName = item["name"].lower()
            if not re.search(f"(^| |.){cityName}($| )", lowerName):
                print("No city: ", item["name"])  # DEBUG
                continue
            if item["level"] == 6:
                if len(data) == 1:
                    return item["id"]
                elif item["kind"] in ["1", "4"]:
                    if not re.search(" do ", lowerName):
                        return item["id"]
            else:
                continue

        return None

    def __readCityPopulation(self, data, unitId):
        result = None
        for item in data:
            if len(data) == 1:
                print("One item: ", item["values"])  # DEBUG
                result = item["values"]
                break
            elif not unitId[-1] == "0":
                print("UnitId: ", unitId)  # DEBUG
                if unitId == item["id"]:
                    result = item["values"]
                    break
            else:
                print("Item: ", item)  # DEBUG

                if item["id"][-1] == "1":
                    result = item["values"]
                    break
                if re.search("miasto$", item["name"].lower()):
                    result = item["values"]
                    break
                else:
                    result = item["values"]

        print("Correct: ", result)  # DEBUG
        if result:
            result.reverse()
            return result[0]["val"]
        return None

    def __getDataResponse(self, url, params):
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(
                    f"Response error: {response.status_code}", "connectionError"
                )

        except requests.exceptions.RequestException as e:
            print("Connection Error: ", e)
            raise Exception(f"Response error", "connectionError")

    def __normalizeProvinceName(self, name):
        return name.lower().replace("województwo ", "")[:-1] + "m"
