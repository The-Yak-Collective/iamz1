#seperate files so we can split up robot between multiple files, if we want
import discord
from discord.ext import commands

load_dotenv('.env')
from dotenv import load_dotenv

PREAMBLE=os.getenv('YAK_ROVER_NAME')

intents = discord.Intents.default()
#intents.reactions = True
#intents.members = True
bot = commands.Bot(command_prefix='$'+PREAMBLE+' ', intents=intents)
print('bot:',bot)

