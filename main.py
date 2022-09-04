import discord
import os
# from discord.ext import commands, tasks
import asyncio
import requests
from keep_alive import keep_alive
from replit import db
from discord.ext.commands import Bot, has_permissions, CheckFailure

# db["channel_ids"] = []
# print(db.keys())

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

# All channels db json
all_channels = db["channel_ids"]

ques = [
  "hello?",
  "hi?",
  "bye?",
]

ct=0

# time delay
seconds = 5

client = Bot(command_prefix="sussy")

@client.event
async def on_ready():
  # printing bots name using discord_client.user
  print(f'Logged in {client.user}')
  # await send()


@client.command(pass_context=True)
@has_permissions(administrator=True)
async def whoami(ctx):
  print("WHOAMI")
  msg = "You're an admin {}".format(ctx.message.author.mention)  
  await client.send_message(ctx.message.channel, msg)

@whoami.error
async def whoami_error(error, ctx):
  if isinstance(error, CheckFailure):
    msg = "You're an average joe {}".format(ctx.message.author.mention)  
    await client.send_message(ctx.message.channel, msg)

@client.event
async def on_message(message):
  # {message.author} -> sender name
  # {client.user} -> who created the bot
  # checking if both are same then do nothing
  # await whoami(ctx)
  print(message.channel.id)
  if message.author == client.user:
    return

  # if the message recieved is startswith(command)
  # then do task
  if message.content.startswith('sussy') and len(message.content)==5:
    print(message)
    print(message.author.name, message.guild.name)
    await message.channel.send("Yea boeh!?");
    print(all_channels)

  if message.content.startswith('sussy set id'):
    if(message.author.name != message.guild.name):
      await message.channel.send("You wanna get BAN kid? You are not the owner here can't use this command!")
      return
    msg = message.content.split()
    owner_name = f'{message.guild.name}-{message.guild.id}'
    if(len(msg)==3):
      print(all_channels[0]["owner_name"] == owner_name)
      if_exists = False
      channel_idx = -1
      # Check if owner exists
      for channel in all_channels:
        channel_idx += 1
        if channel["owner_name"] == owner_name:
          if_exists = True
          break
      print("ifexists",if_exists)
      if if_exists:
        print("changed",message.channel.id)
        all_channels[channel_idx]["channel_id"] = message.channel.id
      else:
        all_channels.append({
          "owner_name": owner_name,
          "channel_id": message.channel.id,
        })
      print(message.content)
      print(message.author.name, message.guild.name)
      await message.channel.send("Done! I will send you quotes every hour <3")
      # db[""]
    else:
      await message.channel.send("Invalid Command!\nTry like this `sussy set id channel_id`");

async def send():
  while True:
    try:
      print(all_channels)
      quote_data = requests.get(random_quote_url)
      quote_data = quote_data.json()
      print(quote_data)
      quote = f'_{quote_data["content"]} \nby {quote_data["author"]}_'
      for channel in all_channels:
        channel = client.get_channel(channel["channel_id"])
        if channel == None:
          raise Exception("channel not found")
        await channel.send(quote)
        await asyncio.sleep(seconds)
      
    except:
      print("Channel is not with us anymore")
    
# running discord client / running server as well
# giving bot token to run 
keep_alive()
client.run(my_secret)




