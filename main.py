import os

import discord
from dotenv import load_dotenv
import random
import requests

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$based'):
    gif_url = 'https://media.tenor.com/cXMEiCWQJ-EAAAAC/wonder-egg-priority-ai-ohto.gif'
    filename = 'based.gif'

    # Download the file
    def download_file(url, filename):
      response = requests.get(url, stream=True)
      with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
          if chunk:
            f.write(chunk)

    download_file(gif_url, filename)

    # Create discord.File from the downloaded file
    with open(filename, 'rb') as f:
      based_gif = discord.File(f)
      await message.channel.send(file=based_gif)


token = os.getenv('TOKEN')
if token is None:
  print(
      "Error: Discord bot token not found. Please set the 'TOKEN' environment variable."
  )
else:
  client.run(token)
