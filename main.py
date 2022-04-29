import discord
import os
# from discord.ext import commands, tasks
import asyncio
import requests
from keep_alive import keep_alive

# db["all_ques"] = [
#   "q1",
#   "q2",
#   "q3"
# ]

# db["temp_user"] = {
#   "q1":"who",
#   "q2":"what",
#   "q3":"how"
# }

# value = db["all_ques"]
# value2 = db["temp_user"]

# print(value[0])
# print(value2["q1"])

# Registering discord client 
client = discord.Client()

random_quote_url = "https://api.quotable.io/random"

# Bot token
my_secret = os.environ['TOKEN']

ques = [
  "hello?",
  "hi?",
  "bye?",
]

ct=0

@client.event
async def on_ready():
  # printing bots name using discord_client.user
  print(f'Logged in {client.user}')
  await send()
  

@client.event
async def on_message(message):
  # {message.author} -> sender name
  # {client.user} -> who created the bot
  # checking if both are same then do nothing
  print(message.channel.id)
  if message.author == client.user:
    return

  # if the message recieved is startswith(command)
  # then do task
  if message.content.startswith('sussy') and len(message.content)==5:
    print(message)
    print(message.author.name, message.guild.name)
    await message.channel.send("Yea boeh!?");

  if message.content.startswith('sussy set id'):
    if(message.author.name != message.guild.name):
      await message.channel.send("You wanna get BAN kid? You are not the owner here can't use this command!")
      return
    msg = message.content.split()
    if(len(msg)==4):
      print(message.content)
      print(message.author.name, message.guild.name)
      await message.channel.send("Done! I will send you quotes every hour <3")
      # db[""]
    else:
      await message.channel.send("Give me channel ID \nTry like this `sussy set id channel_id`");


async def send():
  while True:
    try:
      channel = client.get_channel(328424904724709396)
      if channel == None:
        raise Exception("channel not found")
      quote_data = requests.get(random_quote_url)
      quote_data = quote_data.json()
      print(quote_data)
      quote = f'_{quote_data["content"]} \nby {quote_data["author"]}_'
      await channel.send(quote)
      await asyncio.sleep(600)
      
    except:
      print("Channel is not with us anymore")
    
# running discord client / running server as well
# giving bot token to run 
keep_alive()
client.run(my_secret)




