#discord bot to act as interface for z1 yak rover
#use IAMZ1_DISCORD_KEY as an env variable - the key for discord bot. needs read/write permission to some channels

# add a "upload file" command to discord, to upload a python file (this is not instead of git)
# add a "run file". response is sent back on discord as an ascii message
# add a kill file" command, to stop the command
# each rover has its own tag. so "$iamz1 run raise_your_leg PARAM1 PARAM2..."
# we can add a "git xxx" which will pull from the git repository into a directory with same name.
# all files loaded into directories with the username of the discord user (or something)
# video feedback we still need to solve - maybe shoudl be a rover command and nota  discord command? also needs a time limi

# watchdogs. can be uploaded. they are able to stop any prog from interacting with rover parts. not clear what is best way to do it. a message to the Rover object might do it.

#from discord.ext import tasks, commands
import discord
import asyncio
import os
import time
import datetime
import re
import subprocess

from dotenv import load_dotenv
from discord.ext import tasks, commands


from discord_iamz1 import * #especially "bot"



load_dotenv('.env')
USERHOMEDIR="/media/pi/z1-drive/"

@bot.event #needed since it takes time to connect to discord
async def on_ready(): 
    print('We have logged in as {0.user}'.format(bot),  bot.guilds)
    return

@bot.command(name='test', help='test message. go to https://roamresearch.com/#/app/ArtOfGig/page/iBLdEt5Ji to see more about z1 yak rover project')
async def iamz_test(ctx):
        s='this is a test response from z1 rover bot who got a message from '+ctx.author.name
        await splitsend(ctx.channel,s,False)
        return

@bot.command(name='upload', help='upload an attached file to directory of user that sent the message. will only upload one file, for now')
async def iamz1_upload(ctx):
        s='i would have uploaded file to directory of '+ctx.author.name
#check there is a file
#check if there is a directory or create one if needed
#overwrite existing file
        await splitsend(ctx.channel,s,False)
        return

@bot.command(name='run', help='run X ARGS: run a file X in the directory of user that sent the message. send next parameters to running. ')
async def iamz1_run(ctx,name,*args):
    s='i would have run file {0} in directory of {1} with parameters {2}'.format(name,ctx.author.name," ".join(args))
#check there is a file and directory. if not say "oops"
#call script that runs file, etc into a text file
#send back message with pid, for killing
#script will send back the output file by curl
    thestringlist=['source',USERHOMEDIR+name2filename(ctx.author.name)+'/'+runcommand.bash,name]+args
    out = subprocess.Popen(thestringlist, 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    s=s+ '\n'+str(thestringlist)+'\n'+str(stdout,"utf-8").replace("\\n",'\n')

    await splitsend(ctx.channel,s,False)
    return
        
@bot.command(name='watchdog', help='watchdog X ARGS: run AS A WATCHDOG a file X in the directory of user that sent the message. send next parameters to running. ')
async def iamz1_run(ctx,name,*args):
        s='i would have run file {0} in directory of {1} as a watchdog with parameters {2}'.format(name,ctx.author.name,str(*args))
#check there is a file and directory. if not say "oops"
#format for how to run and how to give feedback for watchdog and how to kill one, unclear for now. so maybe use "run"
        await splitsend(ctx.channel,s,False)
        return

@bot.command(name='kill', help='kill PID: kills a pid returned by run. seems open to abuse. ')
async def iamz1_kill(ctx,pid):
        s='i would have killed PID '+pid
#check there is a pid. it needs to include name of execution script or something. if not say "oops"
#hope script will send back the output file by curl
#send kill command
        await splitsend(ctx.channel,s,False)
        return

@bot.command(name='git', help='one day this will do a git pull action into user directory. ')
async def iamz1_git(ctx,git):
        s='i would have pulled git repository '+git+' into user dir '+ctx.author.name
#tbd - what about privacy?
        await splitsend(ctx.channel,s,False)
        return
        
@bot.command(name='video', help='video start/stop duration. one day this will open a video stream to a well known location for duration seconds. maybe a twilio room. ')
async def iamz1_video(ctx,onoff, *arg):
        if len(arg)>1:
            dur=arg[0]
        else:
            dur=30
        s='i would have turned a video stream '+onoff+' for '+str(dur)+' seconds'
#tbd - needs to autoshutdown to save money
        await splitsend(ctx.channel,s,False)
        return

def name2filename(x):
    return re.sub('[^a-zA-Z0-9]+','',x)

def allowed(x,y): #is x allowed to play with item created by y
#permissions - some activities can only be done by yakshaver, etc. or by person who initiated action
    if x==y: #same person. setting one to zero will force role check
        return True
    mid=bot.guilds[0].get_member(message.author.id)
    r=[x.name for x in mid.roles]
    if 'yakshaver' in r or 'yakherder' in r: #for now, both roles are same permissions
        return True
    return False

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
