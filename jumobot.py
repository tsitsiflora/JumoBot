import os
import requests
import time
from pathlib import Path
from dotenv import load_dotenv
import json
from jumobot_config import BOT_NAME, SLACK_BOT_TOKEN, WEATHER_API_TOKEN 
from slackclient import SlackClient

env_path = Path('.')/'env'
load_dotenv(dotenv_path=env_path)

# instantiating the slack client
slack_client = SlackClient(token=os.environ['SLACK_BOT-TOKEN'])
# we also need the user ID: 
jumobot_id = None

# defining constants
# adding a 1 second delay between reading from RTM
RTM_READ_DELAY = 1
COMMAND = "/jumo_weather"


def parse_slack_output(slack_rtm_output):
    """Parses output data from Slack message stream"""

    # read data from slack channels
    output_list = slack_rtm_output

    if output_list and len(output_list) > 0:
        for output in output_list:

            if output and 'text' in output:
                text = output['text']

                # if bot name is mentioned, take text to the right of the mention as the command
                if COMMAND in text.lower():
                    city = text.lower().strip()
                    return city, output['channel']

    return None, None


def get_weather(city):
    '''Makes a get request to the Open Weater API, gets the location of the
    requested city.'''

    api_key = WEATHER_API_TOKEN
    route = f'api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    api_request = requests.get(route)
    data = json.loads(api_request.text)
    weather_response = f'It feels like {data} degrees'
    return weather_response


def bot_response(channel, weather_response): 
    '''Takes the response from the get_weather function and posts it in the channel'''

    #default response for when the weather API does not understand the request
    default_response = 'City not found, please try again.'

    #sending the response back to the channel
    slack_client.api_call(
        'çhat.postMessage', channel=channel, text=weather_response or default_response
    )


if __name__ == "__main__":
    if slack_client.rtm_connect():
        print(f"{BOT_NAME} connected and running!")

        while True:
            text_input, channel = parse_slack_output(slack_client.rtm_read())
            if text_input and channel:
                bot_response(text_input, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID")



