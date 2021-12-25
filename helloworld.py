import slack
from jumo_config import SLACK_BOT_TOKEN, WEATHER_API_TOKEN, BOT_NAME
#from slackclient import SlackClient

slack_client = slack.WebClient(SLACK_BOT_TOKEN)

slack_client.chat_postMessage(channel='#test', text="Hello world!")