# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import DiningHall
import urllib.request  as urllib2 
import json
import requests
from flask_restful import Resource, reqparse
from twilio.rest import Client
import datetime
import time


app = Flask(__name__)

favorite_foods = ""#["Macaroni & Cheese", "Fried Butterfly Shrimp", "S'mores Bars", "French Fries", "Chocolate Chunk Cookie"]

dining_halls = {1: "Ikenberry Dining Hall", 2: "PAR Dining Hall", 5: "Lincoln/Allen Dining Hall", 27: "Blue 41"}  


def populate_favorites():
    global favorite_foods
    f = open("favorites.txt", "r")
    favorites_list = f.read()
    f.close()
    favorite_foods = favorites_list.split(",")

def get_favorite(hall, dateFrom, dateTo): 
    global dining_halls
      
    request_url = "https://web.housing.illinois.edu/MobileDining2/WebService/Search.aspx?k=7A828F94-620B-4EE3-A56F-328036CC3C04"
    request_url += "&id=" + str(hall) + "&from=" + dateFrom + "&to=" + dateTo + "&t=json"  
    try:
        request_data = requests.get(request_url)
        request_file = json.loads(request_data.text)
        menus = request_file["Menus"]["Item"]
        
        favoriteMessage = ""
        
        for food_item in menus:
            if food_item["FormalName"] in favorite_foods:
                if favoriteMessage == "":
                    favoriteMessage = food_item["FormalName"] + " is being served in " + dining_halls[int(hall)] + " during " + food_item["Meal"]
                else:
                    favoriteMessage += "\n" + food_item["FormalName"] + " is being served in " + dining_halls[int(hall)] + " during " + food_item["Meal"]
            
        if favoriteMessage == "":
            favoriteMessage = ""#"None of your favorite items will be served in " + dining_halls[int(hall)]
    except:
        favoriteMessage = ""
    return favoriteMessage 

def make_menu_file_test():
    global dining_halls
    text_to_add = ""
    
    
    for hall in dining_halls:
        request_url = "https://web.housing.illinois.edu/MobileDining2/WebService/Search.aspx?k=7A828F94-620B-4EE3-A56F-328036CC3C04"
        request_url += "&id=" + str(hall) + "&t=json"
        
        request_data = requests.get(request_url)
        request_file = json.loads(request_data.text)
        menus = request_file["Menus"]["Item"]    
                    
        f = open("menu_file.txt", "w")   
            
        text_to_add = ""
        for food in menus:
            text_to_add += food["Meal"] + ":" + food["FormalName"] + ", "   
        f.write(text_to_add)
        f.close()
        
def make_category_menu_file():
    global dining_halls
    text_to_add = ""
    
    
    for hall in dining_halls:
        request_url = "https://web.housing.illinois.edu/MobileDining2/WebService/Search.aspx?k=7A828F94-620B-4EE3-A56F-328036CC3C04"
        request_url += "&id=" + str(hall) + "&t=json"
        try:
            request_data = requests.get(request_url)
            request_file = json.loads(request_data.text)
            menus = request_file["Menus"]["Item"]    
                    
            
            meal_dictionary = ""
            
            with open("category_menu_file.txt") as file:
                meal_dictionary = file.read()
                file.close()
            f = open("category_menu_file.txt", "w")
            f.write("")
                #meal_dictionary = json.loads(meal_dictionary)
            text_to_add = ""
            for food in menus:
                text_to_add += food["Course"] + ": " + food["FormalName"] + ", "
            
            text_to_add = text_to_add[0:-1] + "}"
            f = open("category_menu_file.txt", "a")
            f.write(meal_dictionary[0:-1] + text_to_add)
            f.close()
        except:
            pass    

def make_menu_file():
    global dining_halls
    text_to_add = ""
    
    
    for hall in dining_halls:
        request_url = "https://web.housing.illinois.edu/MobileDining2/WebService/Search.aspx?k=7A828F94-620B-4EE3-A56F-328036CC3C04"
        request_url += "&id=" + str(hall) + "&t=json"
        try:
            request_data = requests.get(request_url)
            request_file = json.loads(request_data.text)
            menus = request_file["Menus"]["Item"]    
                    
            
            meal_dictionary = ""
            
            with open("menu_file.txt") as file:
                meal_dictionary = file.read()
                file.close()
            f = open("menu_file.txt", "w")
            f.write("")
                #meal_dictionary = json.loads(meal_dictionary)
            text_to_add = ""
            for food in menus:
                text_to_add += food["Meal"] + ": " + food["FormalName"] + ", "
            
            text_to_add = text_to_add[0:-1] + "}"
            f = open("menu_file.txt", "a")
            f.write(meal_dictionary[0:-1] + text_to_add)
            f.close()
        except:
            pass

def get(hall, dateFrom, dateTo):
    request_url = "https://web.housing.illinois.edu/MobileDining2/WebService/Search.aspx?k=7A828F94-620B-4EE3-A56F-328036CC3C04"
    request_url += "&id=" + hall + "&from=" + dateFrom + "&to=" + dateTo + "&t=json"
    
    request_data = requests.get(request_url)
    request_file = json.loads(request_data.text)
    menus = request_file["Menus"]["Item"]
    
    foods = ""
    for food in menus:
        foods = food["FormalName"]
    
    return str(foods)

@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
    """Respond to incoming messages with a friendly SMS."""
    # Start our response
    resp = MessagingResponse()

    # Add a message
    #r = DiningHall.Dining()
    #response = str(DiningHall.get("1", "10-26-2019", "10-27-2019"))
    #print(response)
    #response = "Hi"
    response = "" + get("1", "10-26-2019", "10-27-2019")
    resp.message(response)

    return str(resp)

def send_text(phone_number):
    account_sid = 'AC2b65ac20e63664cf0a6faafa1802061c'
    auth_token = '4dbe4cab0aae0d4c22cc2a7054b01a73'
    client = Client(account_sid, auth_token)
    
    message = client.messages \
                    .create(
                         body=get_favorite("2", "10-26-2019", "10-26-2019"),
                         from_='+12172902221',
                         to='+1' + str(phone_number)
                     )    

if __name__ == "__main__":
    #app.run(debug=True)
    #send_text(9199860150)
    #send_text(6508420875)
    #startTime = datetime.datetime(2019, 10, 26, 13, 32, 0)
    #print(datetime.datetime.now())
    #while datetime.datetime.now() < startTime:
        #time.sleep(1)
        
    #print("yay")
    populate_favorites()
    fav = ""
    for halls in dining_halls:
        if get_favorite(halls, "10-26-2019", "10-26-2019") != "":
            fav += get_favorite(halls, "10-26-2019", "10-26-2019") + "\n"
    print(fav)
    make_category_menu_file()