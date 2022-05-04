#v2 rewritten for scratchconnect in order to use list encryption

import requests
import scratchconnect
from dotenv import load_dotenv
import os
import time
import random

load_dotenv()

API_KEY = os.environ['API_KEY']
username = os.environ['USERNAME']
password = os.environ['PASSWORD']

user = scratchconnect.ScratchConnect(username, password)
project = user.connect_project(596980037)  # Connect the project

def getWeather(city):
    api = "https://api.openweathermap.org/data/2.5/weather?q="+city+"&units=imperial&appid="+API_KEY
    r = requests.get(api)
    if r.status_code == 200:
        data = r.json()

        # at a quick glance
        location = data['name']
        condition = data['weather'][0]['main']
        description = data['weather'][0]['description']

        # right now
        temperature = data['main']['temp'] #temperature in fahrenheit
        feels_like_temperature = data['main']['feels_like']

        #today
        max_temperature = data['main']['temp_max']
        min_temperature = data['main']['temp_min']
        humidity = data['main']['humidity'] # should be a percent
        cloud_coverage = data['clouds']['all'] # should be a percent

        return location, condition, description, temperature, feels_like_temperature, max_temperature, min_temperature, humidity, cloud_coverage
    elif r.status_code == 404:
        print("Requested location not found!")

        return "Location Not Found"

RandomLocations = ['Toledo', 'Detriot', 'Columbus', 'Cleveland', 'Miami', 'Olympia', 'Washington DC', 'Boston', 'Kansas City', 'Orlando']
while True:
    variables = project.connect_cloud_variables()
    request = variables.get_cloud_variable_value(variable_name='request')[0]
    #print(request)
    if request != '1':
        if request == '2':
            print('No new requests.')
        elif request == '3':
            print("New request intetified; Random Location.")
            weather = getWeather(random.choice(RandomLocations))
            print(weather)
            if weather == "Location Not Found":
                variables.set_cloud_variable(variable_name='request', value='2')
                print("Response submited: Location not Found; Code 2")
            else:
                encoded = variables.encode_list(list(weather))
                variables.set_cloud_variable(variable_name='response', value=encoded)

                variables.set_cloud_variable(variable_name='request', value='1')
                print("Response Submited: Date sent; Code 1")
        else:    
            print("New request intetified.")
            location = variables.decode(request)
            #print(location)
            #location, condition, description, temperature, feels_like_temperature, max_temperature, min_temperature, humidity, cloud_coverage = getWeather(decoded_request)
            weather = getWeather(location)
            print(weather)
            if weather == "Location Not Found":
                variables.set_cloud_variable(variable_name='request', value='2')
                print("Response submited: Location not Found; Code 2")
            else:
                encoded = variables.encode_list(list(weather))
                variables.set_cloud_variable(variable_name='response', value=encoded)

                variables.set_cloud_variable(variable_name='request', value='1')
                print("Response Submited: Date sent; Code 1")

    else:
        print('No new requests.')
    time.sleep(10) 
