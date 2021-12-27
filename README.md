# JumoBot
A Slack bot for weather updates


# Running the application locally

## Pre-requisites

### Ngrok

1. Download ngrok and register for a free account here: https://ngrok.com/
2. Run your application and obtain the forwarding url.

### A slack application: 

1. Head over to https://api.slack.com/apps to create a new application.
2. Create a slash command for the application under the Slash Commands Section. 
3. Define te scope (i.e allow chat write) and event subscriptions for your app.
4. Enter the forwarding url from ngrok under your request url for slash commands and events.
5. Once you install your application to your workspace, you will obtain a slack token.

PS: After creating your application you need to add it to at least one channel in a Slack workspace.

### Open Weather Map Token

1. Register for the free plan on https://openweathermap.org/api to get current weather data and obtain the API token.

### Python3.7+

1. Make sure you have at least Python 3.7.0 installed on your machine.

## Setting up

1. Create and activate your virtualenv.

2. Install application requirements using pip
```bash
> pip3 install -r requirements.txt
```

3. Create a configuration file named jumo_config.py and enter your slack token, and open weather map token in there. 

4. Import the configuration file to your main application and edit where necessary.

5. Run the app

```bash
> python3 jumobot.py
```

## Testing

In your slack channel enter:

```
> /jumo_weather New York
```
Expected response:
```
The temperature is 1.66 and it feels like 0.39 degrees in New York.
```

