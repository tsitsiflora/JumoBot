import sys
import requests
import time
import re
import json
from jumobot_config import BOT_NAME, SLACK_BOT_TOKEN, WEATHER_API_TOKEN 
from slackclient import SlackClient

# instantiating the slack client
slack_client = SlackClient(SLACK_BOT_TOKEN)
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
                if BOT_NAME in text.lower():
                    return text.lower().split(BOT_NAME)[1].strip().lower(), output['channel']

    return None, None


def get_weather(text):
    api_key = WEATHER_API_TOKEN
    route = f'api.openweathermap.org/data/2.5/weather?q={text}&appid={api_key}'
    api_request = requests.get(route)
    data = json.loads(api_request.text)
    response = f'It feels like {data['main']['temp']} degrees'
    return response


def handle_command():
    return(something)


if __name__ == "__main__":
    if slack_client.rtm_connect():
        print(f"{BOT_NAME} connected and running!")

        while True:
            text_input, channel = parse_slack_output(slack_client.rtm_read())
            if text_input and channel:
                handle_command(text_input, channel)
            RTM_READ_DELAY
    else:
        print("Connection failed. Invalid Slack token or bot ID")



