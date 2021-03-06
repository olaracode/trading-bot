from pycoingecko import CoinGeckoAPI
import discord
import os
import requests
import json
import random
from replit import db

cg = CoinGeckoAPI()
client = discord.Client()

if "active" not in db.keys():
  db["active"] = True

if "favourites" not in db.keys():
  db["favourites"] = ["bitcoin", "ethereum", "litecoin"]

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

  #List vs_currency
  if msg.startswith("$list"):
  
    vs_currencies = cg.get_supported_vs_currencies()
    vs_message = ""
    #loop thru the vs_currencies array and add the currency to the vs_message string
    for currency in vs_currencies:
      #if the currency is the last item on the array the string template change
      if currency == vs_currencies[-1]:
        vs_message += "***{}***".format(currency)
      else:
        vs_message += "***{}*** - ".format(currency)
    await message.channel.send("The **VS_currency** is the way we call the token/coin/currency with which we compare the coin of your choice. This are the ones we support\n> {}".format(vs_message))

  #get pair price
  if msg.startswith("$vs"): 
    #takes 2 arguments, the coin and which coin to compare its value
    try: #Check if the message has more than one word
      value = msg.split("$vs ", 1)[1]
      # Spread the value.split into two different variables
      [token, vs_currencies] = value.split()
      try:
        price = get_coin(ids=token, vs_currencies=vs_currencies)
        await message.channel.send("Current {} price is {} {}".format(token, price, vs_currencies))
      except:
        await message.channel.send("There was a problem getting the pair price :face_with_spiral_eyes: Verify the availability and spelling of the coin id you used.\n> To see a coin id reffer to coingecko.com and look for the coin or use:\n > **$get_id + token contract**")

    except:
      await message.channel.send("Remember to write the coin id you want to get the price off and the pair! Eg: \n> $vs bitcoin usd :thumbsup:\n> $vs bitcoin :x:")
     
  #Get favourites price
  if msg.startswith("$fav"):
    if len(db["favourites"]) > 0:
      try:
        value = msg.split("$fav ", 1)[1]
        try:
          if value == "list":
            for favourite in db["favourites"]:
              await message.channel.send(favourite)
          else:
            favourite_values = get_favourites(db["favourites"], value)
            favourites_message = ""
            for favourite_value in favourite_values:
              favourites_message += "> {} price is {} {}\n".format(favourite_value[0], favourite_value[1], value)
            await message.channel.send(favourites_message)
        except:
          await message.channel.send("There has been a problem fetching the servers favourite coins :skull: try: \n> -Checking your internet conection :white_check_mark:  \n> -Using **$status** to check the coingecko API status :white_check_mark: \n> -Try again later")   
      except:
        await message.channel.send("Make sure to include the currency pair :sweat_smile: Eg: \n\n$fav usd :+1: \n\n$fav :x:")
    else:
      await message.reply("You need to add a coin/token to your favourites list! You can add one doing:\n> **$server+** token_contract\n You can also create your personal list by using:\n> **$personal** init\n> **$personal+** token_contract")

  #Add a server favourite
  if msg.startswith("$server+"):
    try:
      value = msg.split("$server+ ", 1)[1]
      try:
        print(value)
        cg.get_coin_by_id(value)
        if value not in db["favourites"]:
          favourites = db["favourites"]
          favourites.append(value)
          db["favourites"] = favourites
          # db["favourites"].extend(value)
          await message.reply("You have added {} successfully to the favourites list".format(value))

        else:
          await message.reply("{} is already a favourite :rolling_eyes:".format(value))
      except: 
        await message.channel.send("Oops :sweat_smile: we can't find a token with this id. To see the correct id for any coin/token please refer to **coingecko.com** and look for id API in your desired coin details page")
    except:
      await message.channel.send("You need to include a token contract")
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