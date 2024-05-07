from flask import Flask
from flask import render_template

from datetime import datetime

# import request
import requests


api_url = "https://unicafe.fi/wp-json/swiss/v1/restaurants/?lang=fi"

# response from api_url
response = requests.get(api_url)

# get todays date in format 07.05
date = datetime.now().strftime("%d.%m")

app = Flask(__name__)
@app.route("/")
def index():
    
    onko_makkaraa = False
    message = []
    print(response.json())
    for entry in response.json():
        if entry["title"] == "Chemicum":
            for data in entry["menuData"]["menus"]:
                if date in data["date"]:
                    message.append(data)
                    if "Meksikolainen uunimakkara" in data:
                        onko_makkaraa = True
            break
    else:
        message = None
        
    
    return render_template("index.html", message=message, onko_makkaraa=onko_makkaraa, date=date)
