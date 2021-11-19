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

  #Get status of the cg API
  if msg.startswith("$status"):
    result = cg.ping()
    if "To the Moon!" in result["gecko_says"]:
      await message.channel.send("The server is up **to the moon** :rocket:")
    else:
      await message.channel.send("There's something going on :sweat_smile: Please try again later")

  #get pair price
  if msg.startswith("$vs"):
    try: #Check if the message has more than one word
      value = msg.split("$vs ", 1)[1]
      [token, vs_currencies] = value.split()
      try:
        price = get_coin(ids=token, vs_currencies=vs_currencies)
        print(price)
        await message.channel.send("Current {} price is {} {}".format(token, price, vs_currencies))
      except:
        await message.channel.send("There was a problem getting the pair price :face_with_spiral_eyes: Verify the availability and spelling of the coin id you used.\nTo see a coin id reffer to coingecko.com and look for the coin or use **$get_id + token_contract**")

    except:
      await message.channel.send("Remember to write the coin id you want to get the price off and the pair! Eg: \n$vs bitcoin usd :thumbsup:\n$vs bitcoin :x:")
     
  #Get favourites price
  if msg.startswith("$fav"):
    try:
      value = msg.split("$fav ", 1)[1]
      try:
        favourite_values = get_favourites(favourites, value)
        for favourite_value in favourite_values:
          await message.channel.send("Current {} price is {} {}".format(favourite_value[0], favourite_value[1], value))
      except:
        await message.channel.send("There has been a problem fetching the servers favourites :skull: Try: \n-Check your internet conection :white_check_mark:  \n-Use **$status** to check the coingecko API status :white_check_mark: \n-Try again")   
    except:
      await message.channel.send("Make sure to include the currency pair :sweat_smile: Eg: \n\n$fav usd :+1:\n \n$fav :x:")
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