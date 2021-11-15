from pycoingecko import CoinGeckoAPI
import discord
import os
import requests
import json
import random
from replit import db

cg = CoinGeckoAPI()
client = discord.Client()

bitcoin = cg.get_price(ids='bitcoin', vs_currencies='usd')
print(bitcoin['bitcoin']['usd'])
if "active" not in db.keys():
  db["active"] = True

def get_coin(ids, vs_currencies):
  current_price = cg.get_price(ids, vs_currencies)
  return current_price[ids][vs_currencies]


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

  if message.author == client.user:
    return

  msg = message.content
  
  #get price
  if msg.startswith("$vs"):
    value = msg.split("$vs", 1)[1]
    [token, vs_currencies] = value.split()
    price = get_coin(token, vs_currencies)
    await message.channel.send("Current {} price is {} {}".format(token, price, vs_currencies))
  
  #list available pairs
  #if msg.startswith("$list"):
   # null

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