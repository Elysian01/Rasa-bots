# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import EventType
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet

from datetime import date
import mysql.connector


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="chatbot_agent_handoff"
)

today = date.today()
mycursor = db.cursor()


def get_customer_id(name, password):
    name = name.title()
    sql = "SELECT id FROM customers WHERE name = '" + \
        name + "' and password = '" + password + "'"
    mycursor.execute(sql)
    row = mycursor.fetchone()
    # print("Customer ID :" + str(row[0]))
    return row[0]


def get_email(id):
    sql = "SELECT email FROM customers WHERE id = '" + str(id) + "'"
    mycursor.execute(sql)
    row = mycursor.fetchone()
    # print("User Location :" + str(row[0]))
    return row[0]


def sign_in(name, password):
    name = name.title()
    sql = "SELECT * FROM customers WHERE name = '" + \
        name + "' and password = '" + password + "'"
    mycursor.execute(sql)
    row = mycursor.fetchone()
    try:
        if len(row) != 0:
            print(f"{name} just logged in ")
            customer_id = get_customer_id(name, password)
            return customer_id, "Success"
    except TypeError:
        return -1, "Failed"


def sign_up(name, email, password):
    name = name.title()
    sql = "INSERT INTO customers (name,email,password) VALUES (%s,%s,%s)"
    val = (name, email, password)
    mycursor.execute(sql, val)
    db.commit()
    print(f"New User registered with name : {name} and email : {email}")

    customer_id = get_customer_id(name, password)
    return customer_id


class ActionSignIn(Action):

    def name(self) -> Text:
        return "action_sign_in"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot('name')
        password = tracker.get_slot('password')

        customer_id, status = sign_in(name, password)

        if status == "Failed":
            dispatcher.utter_message(
                text="Please provide valid information or Sign up")
            dispatcher.utter_message(template="utter_sign_in_or_sign_up")
            return [SlotSet("name", None), SlotSet("password", None)]
        else:
            email = get_email(customer_id)
            dispatcher.utter_message(
                text=f"Logged in successfully as {name} and email : " + email)
        return [SlotSet("customer_id", str(customer_id)), SlotSet("email", email)]


class ActionSignUp(Action):

    def name(self) -> Text:
        return "action_sign_up"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot('name')
        email = tracker.get_slot('email')
        password = tracker.get_slot('password')

        customer_id = sign_up(name, email, password)

        dispatcher.utter_message(
            text=f"Registered successfully with {name} and email : {email}")

        return [SlotSet("customer_id", str(customer_id))]


# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
