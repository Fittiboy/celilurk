from flask import Flask, request, abort
from os.path import realpath, basename
from waitress import serve
from twitchAPI.twitch import Twitch
import requests
import json
import re

app = Flask(__name__)

prefixes = {}

filepath = realpath(__file__)
filename = basename(filepath)
filedir = filepath[:-len(filename)]
tokenpath = filedir + "tokens.json"

with open(tokenpath) as tokens_file:
    tokens = json.load(tokens_file)

twitch = Twitch(tokens['key'], tokens['secret'])
token = twitch.get_app_token()


@app.route("/", methods=['GET'])
def root():
    streamer = request.args.get("streamer")
    if (prefix := prefixes.get(streamer, None)):
        return prefix
    else:
        b_id = twitch.get_users(logins=streamer)["data"][0]["id"]
        url = "https://api.twitch.tv/helix/chat/emotes"
        params = {
            "broadcaster_id": b_id
        }
        headers = {
            "Authorization": "Bearer " + token,
            "Client-Id": tokens['key']
        }
        response = requests.get(url,
                                params=params,
                                headers=headers).json()
        first_emote = response["data"][0]["name"]
        prefix = re.match("^[a-z0-9]+", first_emote).group(0)
        prefixes[streamer] = prefix
        return prefix


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=6942)
