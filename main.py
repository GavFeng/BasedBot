import os

import discord
from dotenv import load_dotenv
import random
import requests
import json
from replit import db

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

based_words = ["based", "Based", "BASED"]
pog_words = ["pog", "poggers", "Pog", "Poggers", "POG", "POGGERS"]
jonkler_words = ["jonkler", "Jonkler", "JONKLER"]

starter_boardgames = ["Chess", "Catan"]


def get_airing_anime():
  response = requests.get("https://api.jikan.moe/v4/top/anime?filter=airing")
  json_data = response.json()
  anime_list = json_data.get('data', [])

  if anime_list:
    # Extract titles from the list of anime
    titles = [anime['title'] for anime in anime_list]
    return titles
  else:
    return "No airing anime found."


def get_popular_anime():
  response = requests.get(
      "https://api.jikan.moe/v4/top/anime?filter=bypopularity")
  json_data = response.json()
  anime_list = json_data.get('data', [])

  if anime_list:
    # Extract titles from the list of anime
    titles = [anime['title'] for anime in anime_list]
    return titles
  else:
    return "Error Finding Anime."


def get_upcoming_anime():
  response = requests.get("https://api.jikan.moe/v4/top/anime?filter=upcoming")
  json_data = response.json()
  anime_list = json_data.get('data', [])

  if anime_list:
    # Extract titles from the list of anime
    titles = [anime['title'] for anime in anime_list]
    return titles
  else:
    return "No upcoming anime found."


async def send_based_gif(channel):
  tenor_gifs = [
      'https://media.tenor.com/cXMEiCWQJ-EAAAAC/wonder-egg-priority-ai-ohto.gif',
      'https://media.tenor.com/pZVhtVrNefQAAAAd/spy-x-family-yor-forger.gif',
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
    await channel.send(file=based_gif)


async def send_pog_gif(channel):
  tenor_gifs = [
      'https://media.tenor.com/ivazNwHRNXEAAAAd/pog-poggers.gif',
      'https://media.tenor.com/_x4YWJaC624AAAAC/x3.gif',
  ]
  random_gif_url = random.choice(tenor_gifs)

  filename = 'pog.gif'

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
    pog_gif = discord.File(f)
    await channel.send(file=pog_gif)


async def send_jonkler_gif(channel):
  tenor_gifs = [
      'https://media.tenor.com/ZmfAblJRirMAAAAd/bunny-girl.gif',
      'https://media.tenor.com/FWCuG9k-2kQAAAAd/uh-hello-department.gif',
  ]
  random_gif_url = random.choice(tenor_gifs)

  filename = 'jonkler.gif'

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
    jonkler_gif = discord.File(f)
    await channel.send(file=jonkler_gif)


def update_boardgame_list(boardgame):
  if "boardgames" in db.keys():
    boardgames = db["boardgames"]
    boardgames.append(boardgame)
    db["boardgames"] = boardgames
  else:
    db["boardgames"] = [boardgame]


def delete_boardgame(index):
  boardgames = db["boardgames"]
  if len(boardgames) > index:
    del boardgames[index]
    db["boardgames"] = boardgames


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
    await send_based_gif(message.channel)

  if any(word in message.content for word in based_words):
    await send_based_gif(message.channel)

  if any(word in message.content for word in pog_words):
    await send_pog_gif(message.channel)

  if any(word in message.content for word in jonkler_words):
    await send_jonkler_gif(message.channel)

  options = starter_boardgames
  if "bordgames" in db.keys():
    options = options + db["boardgames"]

  if message.content.startswith('$add'):
    boardgame = message.content.split('$add ', 1)[1]
    update_boardgame_list(boardgame)
    await message.channel.send(boardgame + " added.")

  if message.content.startswith('$del'):
    boardgames = db.get("boardgames", [])
    if boardgames:
      try:
        # Adjust for one-based indexing by subtracting 1
        index = int(message.content.split('$del', 1)[1].strip()) - 1
        if 0 <= index < len(boardgames):
          delete_boardgame(index)
          boardgames = db["boardgames"]
          if boardgames:
            # Format each board game with a number
            formatted_list = "**Updated Board Game List:**\n" + "\n".join(
                f"**{i + 1}**. {game}" for i, game in enumerate(boardgames))
            await message.channel.send(formatted_list)
          else:
            await message.channel.send("All boardgames have been deleted.")
        else:
          await message.channel.send("Error: Index is out of range.")
      except ValueError:
        await message.channel.send(
            "Error: Please provide a valid integer index after `$del`.")

  if message.content.startswith("$list"):
    boardgames = db.get("boardgames", [])
    if boardgames:
      formatted_list = "**Board Game List:**\n" + "\n".join(
          f"**{i + 1}**. {game}" for i, game in enumerate(boardgames))
      await message.channel.send(formatted_list)
    else:
      await message.channel.send("No boardgames found.")

  if message.content.startswith('$airing'):
    airing_anime = get_airing_anime()
    formatted_list = "**Airing Anime List:**\n" + "\n".join(
        f"**{i + 1}**. {anime}" for i, anime in enumerate(airing_anime))
    await message.channel.send(formatted_list)

  if message.content.startswith('$popular'):
    popular_anime = get_popular_anime()
    formatted_list = "**Popular Anime List:**\n" + "\n".join(
        f"**{i + 1}**. {anime}" for i, anime in enumerate(popular_anime))
    await message.channel.send(formatted_list)

  if message.content.startswith('$upcoming'):
    upcoming_anime = get_upcoming_anime()
    formatted_list = "**Upcoming Anime List:**\n" + "\n".join(
        f"**{i + 1}**. {anime}" for i, anime in enumerate(upcoming_anime))
    await message.channel.send(formatted_list)


token = os.environ.get('TOKEN')
if token is None:
  print(
      "Error: Discord bot token not found. Please set the 'TOKEN' environment variable."
  )
else:
  client.run(token)
