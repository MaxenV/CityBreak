# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import FollowupAction, SlotSet

from . import gusService
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

        # gusService = GUSService.GUSService()
        city = tracker.get_slot("city")

        if city is None:
            dispatcher.utter_message(text="Jakie miasto Cię interesuje?")
            return []

        nomCity = wp.to_nominative(city)
        try:
            unitId = gusService.getUnitIdFromCity(nomCity)
            population = gusService.getPopulationOfCity(unitId)

            dispatcher.utter_message(
                text=f"Populacja miasta {nomCity} wynosi: {population}"
            )
            return []

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
        finally:
            print("=" * 10 + " END of ActionCityPopulation " + "=" * 10, end="\n\n")


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
        # gusService = GUSService.GUSService()

        if city is None:
            dispatcher.utter_message(text="Jakie miasto Cię interesuje?")
            return []

        nomCity = wp.to_nominative(city)
        try:
            unitId = gusService.getUnitIdFromCity(nomCity)
            province = gusService.getProvinceFromUnitId(unitId)
            dispatcher.utter_message(
                text=f"Miasto: {nomCity} znajduje się w województwie {province}"
            )
            return []

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
        finally:
            print("=" * 10 + " END of ActionCityLocation " + "=" * 10, end="\n\n")


class ActionAnswerContext(Action):

    def name(self) -> Text:
        return "action_answer_context"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        available_operations = [
            "context_population",
            "context_location",
            "compare_population",
        ]
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
            elif lastly_operation == "compare_population":
                return [FollowupAction("action_compare_population")]
            else:
                dispatcher.utter_message(text="Nie mam informacji do wyświetlenia.")
                return []


class ActionComparePopulation(Action):

    def name(self) -> Text:
        return "action_compare_population"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # gusService = GUSService.GUSService()
        city1 = tracker.get_slot("prev_city")
        city2 = tracker.get_slot("city")

        if city1 is None or city2 is None:
            dispatcher.utter_message(text="Podaj miasta do porównania.")
            return []

        nomCity1 = wp.to_nominative(city1)
        nomCity2 = wp.to_nominative(city2)

        try:
            unitId1 = gusService.getUnitIdFromCity(nomCity1)
            unitId2 = gusService.getUnitIdFromCity(nomCity2)
            population1 = gusService.getPopulationOfCity(unitId1)
            population2 = gusService.getPopulationOfCity(unitId2)

            if population1 > population2:
                dispatcher.utter_message(
                    text=f"Populacja miasta {nomCity1} jest większa niż populacja miasta {nomCity2} o {population1 - population2} osób."
                )
            elif population1 < population2:
                dispatcher.utter_message(
                    text=f"Populacja miasta {nomCity2} jest większa niż populacja miasta {nomCity1} o {population2 - population1} osób."
                )
            else:
                dispatcher.utter_message(
                    text=f"Populacja miasta {nomCity1} i {nomCity2} jest taka sama i wynosi {population1} osób."
                )
            return []
        except Exception as e:
            if len(e.args) > 1 and e.args[1] == "connectionError":
                dispatcher.utter_message(
                    text=f"Problem z połączeniem z serwerem GUS. Spróbuj ponownie później."
                )
                return []

            print(e)
            dispatcher.utter_message(
                text=f"Nie udało się pobrać danych o populacji miast: {nomCity1} i {nomCity2}"
            )
            return []
        finally:
            print("=" * 10 + " END of ActionComparePopulation " + "=" * 10, end="\n\n")


class ActionSetPrevCity(Action):

    def name(self) -> Text:
        return "action_set_prev_city"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        city = tracker.get_slot("city")
        return [SlotSet("prev_city", city)]
