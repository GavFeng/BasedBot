import os

import discord
from dotenv import load_dotenv

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
    await message.channel.send('Based!')


token = os.getenv('TOKEN')
if token is None:
  print(
      "Error: Discord bot token not found. Please set the 'TOKEN' environment variable."
  )
else:
  client.run(token)
