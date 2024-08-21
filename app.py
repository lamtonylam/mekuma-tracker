from flask import Flask
from flask import render_template
from flask_restful import Resource, Api

from datetime import datetime

# import request
import requests

import json

api_url = "https://unicafe.fi/wp-json/swiss/v1/restaurants/?lang=fi"

# response from api_url
response = requests.get(api_url)

app = Flask(__name__)
api = Api(app)

# get todays date in format 07.05
date = datetime.now().strftime("%d.%m")


def furtherst_date_data():
    dates = []
    for object in response.json():
        if object["title"] == "Chemicum":
            for menu in object["menuData"]["menus"]:
                dates.append(menu["date"])
    return dates[-1][3:]


def check_if_sausage_is_in_week(restaurant_name):
    # get the whole week
    menu_original = {}
    for object in response.json():
        if object["title"] == restaurant_name:
            for menu in object["menuData"]["menus"]:
                menu_original[menu["date"]] = []
                data = menu["data"]
                for item in data:
                    menu_original[menu["date"]].append(item["name"])

    # strip the menu
    menu_stripped_from_pastdates = {}
    for date_menu in menu_original:
        present = datetime.now().strftime("%d.%m.")
        # keep the date in the original format
        date_menu_original = date_menu
        # make date in format without weekday
        date_menu = date_menu[3:]
        if datetime.strptime(date_menu, "%d.%m.") < datetime.strptime(
            present, "%d.%m."
        ):
            pass
        else:
            menu_stripped_from_pastdates[date_menu_original] = [
                item.lower() for item in menu_original[date_menu_original]
            ]

    # dates that have sausage
    dates_that_have_sausage = []
    for day in menu_stripped_from_pastdates:
        if "meksikolainen uunimakkara" in menu_stripped_from_pastdates[day]:
            dates_that_have_sausage.append(day)

    return dates_that_have_sausage


def get_todays_menu(restaurant_name):
    restaurant_menu = []
    for object in response.json():
        if object["title"] == restaurant_name:
            for menu in object["menuData"]["menus"]:
                if date in menu["date"]:
                    data = menu["data"]
                    for item in data:
                        restaurant_menu.append(item["name"])
            break

    return restaurant_menu


def unicafe_global_sausagesearch():
    viikkiRestaurants = [
        "Tähkä",
        "Infokeskus alakerta",
        "Viikuna",
        "Infokeskus",
        "Biokeskus",
    ]

    keskustaRestaurants = [
        "Myöhä Café & Bar",
        "Kaivopiha",
        "Kaisa-talo",
        "Soc&Kom",
        "Rotunda",
        "Porthania",
        "Topelias",
        "Olivia",
        "Metsätalo",
        "Cafe Portaali",
    ]

    kumpulaRestaurants = ["Physicum", "Exactum", "Chemicum"]

    meilahtiRestaurants = ["Meilahti"]

    restaurants = (
        viikkiRestaurants
        + keskustaRestaurants
        + kumpulaRestaurants
        + meilahtiRestaurants
    )

    restaurant_sausage_dict = {}
    for restaurant in restaurants:
        sausage_dates = check_if_sausage_is_in_week(restaurant)
        if sausage_dates:
            restaurant_sausage_dict[restaurant] = sausage_dates

    # make a list of restaurants and dates as tuples
    sortedRestaurantsDate = list(restaurant_sausage_dict.items())

    # func to return the pure date of sausage availability of a restaurant
    def returndate(item):
        return item[1][0][3:8]

    # sort the items by date
    sortedRestaurantsDate.sort(key=returndate)
    sortedRestaurantsDate = dict(sortedRestaurantsDate)

    return sortedRestaurantsDate


@app.route("/")
def index():

    # Chemicum
    onko_makkaraa_chemicum = False
    chemicum_menu = get_todays_menu("Chemicum")
    if "Meksikolainen uunimakkara" in chemicum_menu:
        onko_makkaraa_chemicum = True

    chemicum_suljettu = False
    if len(chemicum_menu) == 0:
        chemicum_suljettu = True

    # Exactum
    onko_makkaraa_exactum = False
    exactum_menu = get_todays_menu("Exactum")
    if "Meksikolainen uunimakkara" in exactum_menu:
        onko_makkaraa_exactum = True

    exactum_suljettu = False
    if len(exactum_menu) == 0:
        exactum_suljettu = True

    return render_template(
        "index.html",
        chemicum_menu=chemicum_menu,
        chemicum_suljettu=chemicum_suljettu,
        exactum_menu=exactum_menu,
        exactum_suljettu=exactum_suljettu,
        onko_makkaraa_chemicum=onko_makkaraa_chemicum,
        onko_makkaraa_exactum=onko_makkaraa_exactum,
        date=date,
        global_sausage_search=unicafe_global_sausagesearch(),
        furtherst_date_data=furtherst_date_data(),
    )


# api
class UnicafeGlobalSausageSearch(Resource):
    def get(self):
        return unicafe_global_sausagesearch()


api.add_resource(UnicafeGlobalSausageSearch, "/api")
