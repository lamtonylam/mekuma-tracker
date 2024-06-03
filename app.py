from flask import Flask
from flask import render_template

from datetime import datetime

# import request
import requests

import json

api_url = "https://unicafe.fi/wp-json/swiss/v1/restaurants/?lang=fi"

# response from api_url
response = requests.get(api_url)


# get todays date in format 07.05
date = datetime.now().strftime("%d.%m")

app = Flask(__name__)


@app.route("/")
def index():
    onko_makkaraa_chemicum = False
    chemicum_menu = []
    for object in response.json():
        if object["title"] == "Chemicum":
            for menu in object["menuData"]["menus"]:
                if date in menu["date"]:
                    data = menu["data"]
                    for item in data:
                        chemicum_menu.append(item["name"])
                    if "Meksikolainen uunimakkara" in chemicum_menu:
                        onko_makkaraa_chemicum = True
            break

    print(chemicum_menu)
    
    onko_makkaraa_exactum = False
    exactum_menu = []
    for object in response.json():
        if object["title"] == "Exactum":
            for menu in object["menuData"]["menus"]:
                if date in menu["date"]:
                    data = menu["data"]
                    for item in data:
                        exactum_menu.append(item["name"])
                    if "Meksikolainen uunimakkara" in exactum_menu:
                        onko_makkaraa_exactum = True
            break
    
    print(exactum_menu)

    return render_template(
        "index.html",
        chemicum_menu=chemicum_menu,
        exactum_menu=exactum_menu,
        onko_makkaraa_chemicum=onko_makkaraa_chemicum,
        onko_makkaraa_exactum=onko_makkaraa_exactum,
        date=date,
    )
