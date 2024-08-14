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
  if message.content.startswith('$poll'):
    # Extract the poll question and options
    poll_parts = message.content.split(' ', 1)
    if len(poll_parts) > 1:
      question = poll_parts[1].strip()
      poll_question = question.split('\n')[0]
      options = question.split('\n')[1:]
      options = [option for option in options if option.strip()]
      if len(options) > 1:
        # Create the poll message
        poll_message = f"**{poll_question}**\n\n"
        for i, option in enumerate(options):
          poll_message += f"{chr(ord('🇦') + i)}: {option}\n"
        # Send the poll message with reactions
        poll = await message.channel.send(poll_message)
        for i in range(len(options)):
          await poll.add_reaction(chr(ord('🇦') + i))

        await message.delete()
      else:
        await message.channel.send(
            "Please provide at least two options for the poll.")
    else:
      await message.channel.send("Please provide a poll question.")

  if message.content.startswith('$based'):
    tenor_gifs = [
        'https://media.tenor.com/cXMEiCWQJ-EAAAAC/wonder-egg-priority-ai-ohto.gif',
        'https://media.tenor.com/pZVhtVrNefQAAAAd/spy-x-family-yor-forger.gif',
        'https://media.tenor.com/FWCuG9k-2kQAAAAd/uh-hello-department.gif'
    ]
    random_gif_url = random.choice(tenor_gifs)

    filename = 'based.gif'

    # Download the file
    def download_file(url, filename):
      response = requests.get(url, stream=True)
      with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
          if chunk:
            f.write(chunk)

    download_file(random_gif_url, filename)

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
