import os
import requests
import time
import json

from requests.models import Response
import slack
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
from jumo_config import SLACK_BOT_TOKEN, WEATHER_API_TOKEN, BOT_NAME, SIGNING_SECRET

app = Flask(__name__)

# instantiating the slack client
slack_client = slack.WebClient(SLACK_BOT_TOKEN)
slack_event_adapter = SlackEventAdapter(SIGNING_SECRET,'/slack/events', app)

# defining constants
# adding a 1 second delay between reading from RTM
BOT_ID = slack_client.api_call("auth.test")['user_id']
RTM_READ_DELAY = 1

@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    if BOT_ID != user_id:
        slack_client.chat_postMessage(channel=channel_id, text="That sounds awesome!")


@app.route('/jumo_weather', methods=['POST'])
def weather_request():

    '''Makes a get request to the Open Weather API, gets the weather of the
    requested city.'''

    data = request.form
    city = data.get('text')
    print(city)
    
    api_key = WEATHER_API_TOKEN
    route = f'://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    api_request = requests.get('https' + route)
    data = json.loads(api_request.text)
    weather_response = f'It feels like {data} degrees'
    print(weather_response)

    return weather_response, 200
    
'''
def bot_response(weather_response): 
    Takes the response from the get_weather function and posts it in the channel

    #default response for when the weather API does not understand the request
    default_response = 'City not found, please try again.'

    #sending the response back to the channel
    slack_client.chat_postMessage(text=weather_response or default_response)
'''

if __name__=="__main__":
    app.run(debug=True, port=8000)



