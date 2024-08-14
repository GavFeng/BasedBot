import os

import discord
from dotenv import load_dotenv
import random

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
    tenor_gifs = [
        'https://tenor.com/view/wonder-egg-priority-ai-ohto-egg-wonder-priority-gif-8174882731399849953',
    ]

    random_gif = random.choice(tenor_gifs)
    await message.channel.send(file=discord.File(url=random_gif))


token = os.getenv('TOKEN')
if token is None:
  print(
      "Error: Discord bot token not found. Please set the 'TOKEN' environment variable."
  )
else:
  client.run(token)
