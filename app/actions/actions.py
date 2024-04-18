# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import FollowupAction

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

        if city is None:
            dispatcher.utter_message(text="Jakie miasto Cię interesuje?")
            return []

        nomCity = wp.WordManip().to_nominative(city)
        try:
            unitId = gusService.getUnitIdFromCity(nomCity)
            population = gusService.getPopulationOfCity(unitId)

        except Exception as e:
            if len(e.args) > 1 and e.args[1] == "connectionError":
                dispatcher.utter_message(
                    text=f"Problem z połączeniem z serwerem GUS. Spróbuj ponownie później."
                )
                return []

            print(e)

            dispatcher.utter_message(
                text=f"Nie udało się pobrać danych o populacji miasta: {nomCity}"
            )
            return []

        print("Find unitId: ", unitId)  # DEBUG

        dispatcher.utter_message(
            text=f"Populacja miasta {nomCity} wynosi: {population}"
        )
        return [FollowupAction("action_listen")]


class ActionCityLocation(Action):

    def name(self) -> Text:
        return "action_city_location"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        city = tracker.get_slot("city")
        gusService = GUSService.GUSService()

        if city is None:
            dispatcher.utter_message(text="Jakie miasto Cię interesuje?")
            return []

        nomCity = wp.WordManip().to_nominative(city)
        try:
            unitId = gusService.getUnitIdFromCity(nomCity)
            print("UnitId: ", unitId)  # DEBUG
            province = gusService.getProvinceFromUnitId(unitId)
            print("Province: ", province)  # DEBUG

        except Exception as e:
            if len(e.args) > 1 and e.args[1] == "connectionError":
                dispatcher.utter_message(
                    text=f"Problem z połączeniem z serwerem GUS. Spróbuj ponownie później."
                )
                return []

            print(e)
            dispatcher.utter_message(
                text=f"Nie udało się pobrać danych o lokalizacji miasta: {nomCity}"
            )
            return []

        dispatcher.utter_message(
            text=f"Miasto: {nomCity} znajduje się w województwie {province}"
        )
        return [FollowupAction("action_listen")]


class ActionAnswerContext(Action):

    def name(self) -> Text:
        return "action_answer_context"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        available_operations = ["context_population", "context_location"]
        lastly_operation = tracker.get_slot("lastly_operation")

        if lastly_operation is None:
            dispatcher.utter_message(text="Nie mam informacji do wyświetlenia.")
            return []
        elif lastly_operation not in available_operations:
            dispatcher.utter_message(text="Nie mam informacji do wyświetlenia.")
            return []
        else:
            if lastly_operation == "context_population":
                return [FollowupAction("action_city_population")]
            elif lastly_operation == "context_location":
                return [FollowupAction("action_city_location")]
