#discord bot to act as interface for z1 yak rover
#use IAMZ1_DISCORD_KEY as an env variable - the key for discord bot. needs read/write permission to some channels


# add a "upload file" command to discord, to upload a python file (this is not instead of git)
# add a "run file". response is sent back on discord as an ascii message
# add a kill file" command, to stop the command
# each rover has its own tag. so "$run iamz1 raise_your_leg PARAM1 PARAM2..."
# we can add a "git xxx" which will pull from the git repository into a directory with same name.
# all files loaded into directories with the username of the discord user (or something)
# video feedback we still need to solve

# update on proposal:
# each python code that can run starts command of the format rover= Rover(camera='R',legs='W',time=30)
# means - want to get a rover object and i need rights of R for camera and W of legs. and i want 30 minutes. this information is put in a common table.
# each bot has a different model which si served locallyt for example, for spiderPI it includes camera, servos, legs and gaits. so:
# the call to Rover gives you a submodel of this model, the part you have access to.
# the command rover.leg1.tipto((x,y,z)). will check if leg1 is part of the model and if you have the right to do "tipto()" and if yes, move the tip of the leg to that position.
# video stream (when we decide how to do, maybe twitch?) will also be such a resource, which disconnects when the time allocated is done.
# you can also have complex rights like maximum power, maximum speed of a particular serveo, etc. so not only RW

# Output is in log file put on discord
# You also get a command to send back messages

# two more items:

# watchdogs. can be uploaded. they are able to stop any prog from interacting with rover parts. not clear what is best way to do it. a message to the Rover object might do it.
# communication. we will have a text-type channel between anything (also rovers) and rovers. one example can be to have a flask server on vultr and use webhook to communicate. resulting IP may be used for direct communication maybe.


#from discord.ext import tasks, commands
import discord
import asyncio
import os
import time
import datetime

from dotenv import load_dotenv
from discord.ext import tasks, commands


from discord_iamz1 import * #especially "bot"



load_dotenv('.env')


@bot.event #needed since it takes time to connect to discord
async def on_ready(): 
    print('We have logged in as {0.user}'.format(bot),  bot.guilds)
    return


def allowed(x,y): #is x allowed to play with item created by y
#permissions - some activities can only be done by yakshaver, etc. or by person who initiated action
    if x==y: #same person. setting one to zero will force role check
        return True
    mid=bot.guilds[0].get_member(message.author.id)
    r=[x.name for x in mid.roles]
    if 'yakshaver' in r or 'yakherder' in r: #for now, both roles are same permissions
        return True
    return False




@bot.command(name='test', help='test message. go to https://roamresearch.com/#/app/ArtOfGig/page/iBLdEt5Ji to see more about z1 yak rover project')
async def iamz_test(ctx):
        s='this is a test response from z1 rover bot who got a message from '+ctx.author.name
        await splitsend(ctx.channel,s,False)
        return


async def dmchan(t):
#create DM channel betwen bot and user
    target=bot.get_user(t)
    if (not target): 
        print("unable to find user and create dm",flush=True)
    return target
    target=target.dm_channel
    if (not target): 
        print("need to create dm channel",flush=True)
        target=await bot.get_user(t).create_dm()
    return target

async def splitsend(ch,st,codeformat):
#send messages within discord limit + optional code-type formatting
    if len(st)<1900: #discord limit is 2k and we want some play)
        if codeformat:
            await ch.send('```'+st+'```')
        else:
            await ch.send(st)
    else:
        x=st.rfind('\n',0,1900)
        if (x<0):
            x=1900
        if codeformat:
            await ch.send('```'+st[0:x]+'```')
        else:
            await ch.send(st[0:x])
        await splitsend(ch,st[x+1:],codeformat)

discord_token=os.getenv('IAMZ1_DISCORD_KEY')
bot.run(discord_token) 
