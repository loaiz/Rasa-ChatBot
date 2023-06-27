# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import json
from typing import  Text, List, Any, Dict 
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from actions.action_utils import list_to_nl
#from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.types import DomainDict



class ActionRequestProductCategories(Action):

    def __init__(self) -> None:
        super().__init__()
        with open('data/product_categories.json') as f:
            file_contents = json.load(f)
            self.categories = file_contents["categories"]
    
    def name(self) -> Text:
        return "action_provide_product_categories"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        categories = list_to_nl([c["name"] for c in self.categories])
        if categories:
            dispatcher.utter_message(text=f"Sure! We have {categories}")
        else:
            dispatcher.utter_message(text="I am sorry, we don't have any products at the moment")
        return []
    
    
    

def clean_name(name):
    return "".join([c for c in name if c.isalpha()])

class ValidateNameForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_name_form"

    def validate_first_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `first_name` value."""

        # If the name is super short, it might be wrong.
        name = clean_name(slot_value)
        if len(name) == 0:
            dispatcher.utter_message(text="That must've been a typo.")
            return {"first_name": None}
        return {"first_name": name}

    def validate_last_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `last_name` value."""

        # If the name is super short, it might be wrong.
        name = clean_name(slot_value)
        if len(name) == 0:
            dispatcher.utter_message(text="That must've been a typo.")
            return {"last_name": None}
        
        first_name = tracker.get_slot("first_name")
        if len(first_name) + len(name) < 3:
            dispatcher.utter_message(text="That's a very short name. We fear a typo. Restarting!")
            return {"first_name": None, "last_name": None}
        return {"last_name": name}

