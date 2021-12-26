import json
import slack
import requests
import urllib.parse
from requests.models import Response
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

def get_data():
    '''
    Helper method for getting the data sent by Slack to our webhook
    '''
    
    data = request.form

    return (data.get('channel_id'), data.get('text'))    

@app.route('/jumo_weather', methods=['POST'])
def weather_request():
    '''Makes a get request to the Open Weather API, gets the weather of the
    requested city.'''

    # Get the data sent through the post request
    channel, city = get_data()

    # URL encode user input
    city = urllib.parse.quote_plus(city)

    # Build up the URL for the OWM API, passing in the city name and our API token
    route = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={WEATHER_API_TOKEN}'

    response = ''

    try:
        # Send a request to the API
        api_request = requests.get(route)

        # Parse JSON data
        data = json.loads(api_request.text)

        # If the API returns malformed data, it's an indicator that the city might not exist, send the message to the user
        if data['cod'] is not 200:
            response = data['message'] or 'An error occured while proccessing your request'
        
        else:
            # Build response string
            response = 'The temperature is {} and it feels like {} degrees in {}.'.format( 
                data['main']['temp'], data['main']['feels_like'], data['name'] 
            )
        
    except Exception as e:
        print(str(e))
        response = 'Something went wrong, please try again.'


    '''Takes the response from the weather and posts it in the channel'''

    #sending the response back to the channel
    slack_client.chat_postMessage(channel=channel, text=response.capitalize())
     
    return Response(), 200

if __name__=="__main__":
    app.run(debug=True, port=8000)



# todo: fix the issue with ngrok
