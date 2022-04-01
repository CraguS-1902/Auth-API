import discord
import asyncio
from quart import Quart

app = Quart(__name__)
client = discord.Client()


@app.route("/test")
def test():
    import requests
    import json
    r = requests.post(f'https://discord.com/api/v9/guilds/959116879740416040/channels',

        headers={'Authorization': "Bot OTU4MzUzNzI2MjYxODU0MzI4.YkMGdQ.6eRIPXyTKJsUqwoxN9zqhWt4bT4"})

    channelID = "935244618809876490" # enable dev mode on discord, right-click on the channel, copy ID
    botToken = "OTU4MzUzNzI2MjYxODU0MzI4.YkMGdQ.6eRIPXyTKJsUqwoxN9zqhWt4bT4"    # get from the bot page. must be a bot, not a discord app

    baseURL = "https://discord.com/api/v9/channels/935244618809876490/messages"
    headers = { "Authorization":"Bot {}".format(botToken),
                "User-Agent":"myBotThing (http://some.url, v0.1)",
                "Content-Type":"application/json", }

    data = {
        "content" : "123"
    }
    data["embeds"] = [
        {
            "description" : "text in embed",
            "title" : "embed title"
        }
    ]
    #r = requests.post(baseURL, headers = headers, json = data)
    return r.json()

@app.route("/send", methods=["GET"])
async def send_message():
    # wait_until_ready and check for valid connection is missing here
    channel = client.get_channel("959116879740416043")
    user = client.get_user("935244618809876490")
    await user.send('XYZ')
    return 'OK', 200


app.run()