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
        unitId = gusService.getUnitIdFromCity(city)
        if unitId is None:
            dispatcher.utter_message(text=f"Nie znaleziono miasta: {city}")
            return []
        population = gusService.getPopulationOfCity(unitId)

        dispatcher.utter_message(text=f"Populacja miasta: {city} wynosi: {population}")
        return []
