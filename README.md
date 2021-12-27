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

PS: After creating your application you need to add it to at least one channel in a Slack workspace.

### Python3.7+

1. Make sure you have at least Python 3.7.0 installed on your machine.

## Setting up

1. Create and activate your virtualenv.

2. Install application requirements using pip
```bash
> pip install -r requirements.txt
```

3. Run the app

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

