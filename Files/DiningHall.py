import urllib.request  as urllib2 
import json
import requests
from flask_restful import Resource, reqparse

class Dining(Resource):
    def get(self, hall, dateFrom, dateTo):
        request_url = "https://web.housing.illinois.edu/MobileDining2/WebService/Search.aspx?k=7A828F94-620B-4EE3-A56F-328036CC3C04"
        request_url += "&id=" + hall + "&from=" + dateFrom + "&to=" + dateTo + "&t=json"
        
        request_data = requests.get(request_url)
        request_file = json.loads(request_data.text)
        menus = request_file["Menus"]["Item"]
        
        for food in menus:
            print(food["FormalName"])

r = Dining()
print(r.get("1", "10-26-2019", "10-27-2019"))