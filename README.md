[https://makkara.fly.dev](https://makkara.fly.dev)

# Introduction
The project aims to inform where and when mexican oven sausage is available at Unicafe's restaurants.  
It also acts as an api to fetch restaurant menus for specific queries.

# Local development
Preferably create a Python virtual env first.  
```
python3 -m venv venv
```
Then run
```
pip install -r requirements.txt
```
To start run
```
flask run
```
You should see now the website running at http://127.0.0.1:5000


### API Endpoints

#### Returns Sausage Dates

https://makkara.fly.dev/api

#### Returns Chemicum/Exactum Menu for Today

https://makkara.fly.dev/api/chemicum/exactum

#### Returns Menu for Restaurant for Specific Date
Date is in format 2024-10-30
https://makkara.fly.dev/api/datesearch/<string:restaurant_name>/<string:date>
