#seperate files so we can split up robot between multiple files, if we want
import discord
from discord.ext import commands

intents = discord.Intents.default()
#intents.reactions = True
#intents.members = True
bot = commands.Bot(command_prefix='$iamz1 ', intents=intents)
print('bot:',bot)

#move from "client" to "bot" commands
#import discord

#intents = discord.Intents.default()
#intents.members = True


#client = discord.Client()#intents=intents)
