from pycoingecko import CoinGeckoAPI
import discord
import os
import requests
import json
import random
from replit import db

cg = CoinGeckoAPI()
client = discord.Client()

favourites = ["bitcoin", "ethereum", "litecoin"]

if "active" not in db.keys():
  db["active"] = True

#Gets the current price of a crypto currency. Takes the name of the crypto and the name of the pair
def get_coin(ids, vs_currencies):
  current_price = cg.get_price(ids, vs_currencies)
  return current_price[ids][vs_currencies]


def get_favourites(favourites, pair):
  favourite_prices = []
  for coin in favourites:
      coin_price = get_coin(coin, pair)
      favourite_prices.append([coin, coin_price])
  return favourite_prices

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

  if message.author == client.user:
    return

  msg = message.content
  
  #get price

  # if msg.startswith("$")

  if msg.startswith("$vs"):
    value = msg.split("$vs ", 1)[1]
    [token, vs_currencies] = value.split()
    price = get_coin(token, vs_currencies)
    await message.channel.send("Current {} price is {} {}".format(token, price, vs_currencies))
  
  #Get favourites price
  if msg.startswith("$fav"):
    value = msg.split("$fav ", 1)[1]

    favourite_values = get_favourites(favourites, value)
    for favourite_value in favourite_values:
      await message.channel.send("Current {} price is {} {}".format(favourite_value[0], favourite_value[1], value))

  #Turn on or of
  if msg.startswith("$trady"):
    value = msg.split("$trady ", 1)[1]

    if value.lower() == "on":
      db["active"] = True
      await message.channel.send("Happy to see you!")
    else:
      db["active"] = False
      await message.channel.send("See you soon!")


client.run(os.getenv('TOKEN'))