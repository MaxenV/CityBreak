# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from . import GUSService
from . import wordManip as wp


class ActionCityPopulation(Action):

    def name(self) -> Text:
        return "action_city_population"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        gusService = GUSService.GUSService()
        city = tracker.get_slot("city")
        try:
            unitId = gusService.getUnitIdFromCity(city)
            population = gusService.getPopulationOfCity(unitId)

        except Exception as e:
            if len(e.args) > 1 and e.args[1] == "connectionError":
                dispatcher.utter_message(
                    text=f"Problem z połączeniem z serwerem GUS. Spróbuj ponownie później."
                )
                return []

            print(e)
            nomCity = wp.WordManip().to_nominative(city)
            dispatcher.utter_message(
                text=f"Nie udało się pobrać danych o populacji miasta: {nomCity}"
            )
            return []

        print("Find unitId: ", unitId)  # DEBUG

        dispatcher.utter_message(text=f"Populacja miasta: {city} wynosi: {population}")
        return []
