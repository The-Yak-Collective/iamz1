#seperate files so we can split up robot between multiple files, if we want
import discord
from discord.ext import commands
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv()) #'.env') #possibly not really needed

PREAMBLE=os.getenv('YAK_ROVER_NAME')

intents = discord.Intents.default()
#intents.reactions = True
#intents.members = True
intents.messages=True
intents.message_content=True #and now also to read messages...
bot = commands.Bot(command_prefix='$'+PREAMBLE+' ', intents=intents)
print('bot:',bot)

