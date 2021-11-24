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
#rover name set in system environment - a property of the SP itself
#from discord.ext import tasks, commands

#most of these imports not needed any more
import discord
import asyncio
import os
import time
import datetime
import re
import subprocess
import sys
import shutil #for creating sqlite db
import io # so that we are transparent to how file gets here

from discordsupport import *
from unsupportedcommands import *

from dotenv import load_dotenv, find_dotenv
from discord.ext import tasks, commands


from discord_iamz1 import * #especially "bot"
from rovercommands import *



@bot.event #needed since it takes time to connect to discord
async def on_ready(): 
    print('We have logged in as {0.user}'.format(bot),  bot.guilds)
    return

@bot.command(name='test', help='test message. go to https://roamresearch.com/#/app/ArtOfGig/page/iBLdEt5Ji to see more about z1 yak rover project', before_invoke=gotit)
async def iamz_test(ctx):
        s=dotest(ctx.author.name)
        await splitsend(ctx.channel,s,False)
        return


@bot.command(name='cmdupload', help='upload an attached file to general command directory . will only upload one file, for now', before_invoke=gotit)
async def iamz1_cmdupload(ctx):
    if (len(ctx.message.attachments)>0):#for discord. for http, needs to be different
        print('has attachment')
        thefilename=ctx.message.attachments[0].filename
        f=io.BytesIO()
        await ctx.message.attachments[0].save(f)
        s=docmdupload(thefilename,f)
    else:
        s="no attachment"
    await splitsend(ctx.channel,s,False)
    return

    
@bot.command(name='cmdlist', help='list (python) commands available', before_invoke=gotit)
async def iamz1_cmdlist(ctx):
    s=docmdlist()
    await splitsend(ctx.channel,s,False)
    return

    
@bot.command(name='cmdrun', help='run X ARGS: run a file X (python) in the general directory. send next parameters to running. ', before_invoke=gotit)
async def iamz1_cmdrun(ctx,name,*args):
    s=docmdrun(ctx.author.name,name,*args)
    await splitsend(ctx.channel,s,False)
    return
        

@bot.command(name='raglist', help='show list of action groups we can rag',hidden=True)
async def iamz1_raglist(ctx):
    s=doraglist()
    await splitsend(ctx.channel,s,False)
    return


@bot.command(name='stop', help='stops any ongoing action group (rag) and camera motion (cam). we hope', before_invoke=gotit)
async def iamz1_stop(ctx):
    s=dostop()
    await splitsend(ctx.channel,s,False)
    return


@bot.command(name='rag', help='run action group NAME [TIMES] times. "list" shows list of available actions. "stop" stops running action. ',before_invoke=gotit)
async def iamz1_rag(ctx, name, *args):
    await gotit(ctx) #must we?
    s=dotherag(name,*args)
    await splitsend(ctx.channel,s,False)
    return



@bot.command(name='seq', help='run a sequence of commands NAME [TIMES] times. "list" shows list of available sequence files actions. "stop" stops running action. ',before_invoke=gotit)
#sequnces in subfolder "seqs"
async def iamz1_seq(ctx, name, *args):
    await gotit(ctx)
    s=dotheseq(name,*args)
    await splitsend(ctx.channel,s,False)
    return


@bot.command(name='cam', help='move camera pan/tilt +/-/x OR x,y OR rest. "list" shows list of available actions. ', before_invoke=gotit)
async def iamz1_cam(ctx, *args):
    await gotit(ctx)

    s=dothecam(*args)
    await splitsend(ctx.channel,s,False)
    return
        
    
@bot.command(name='unload', help='move all servos to unload configuration')
async def iamz1_unloadservos(ctx):
    s=dotheunload()
    await splitsend(ctx.channel,s,False)
    return



@bot.command(name='run', help='run X ARGS: run a file X in the directory of user that sent the message. send next parameters to running. ', before_invoke=gotit)
async def iamz1_run(ctx,name,*args):
    s=dorun(ctx.author.name,name,*args)
    await splitsend(ctx.channel,s,False)
    return


        
@bot.command(name='video', help='video on/off duration. for now it can only start and only for 5 min. ', before_invoke=gotit)
async def iamz1_video(ctx,onoff, *arg):
    s=dovideo(onoff,*arg)
    await splitsend(ctx.channel,s,False)
    return


@bot.command(name='tweet', help='tweet on/off. tweet a picture of outcome of command after doing command', before_invoke=gotit)
async def tweetonoff(ctx,onoff):
    s=dotweetonoff(onoff)
    await splitsend(ctx.channel,s,False)
    return


@bot.command(name='aunload', help='aunload on/off. automaic unload after each rag command', before_invoke=gotit)
async def unloadonoff(ctx,onoff):
    s=dounloadonoff(onoff)
    await splitsend(ctx.channel,s,False)
    return


@bot.command(name='log', help='log on/off. start/stop logging into a dedicated directory', before_invoke=gotit)
async def logonoff(ctx,onoff):
    s=dologonoff(onoff)
    await splitsend(ctx.channel,s,False)
    return



@bot.command(name='clip', help='clip on/off. capture clip next rag', before_invoke=gotit)
async def cliponoff(ctx,onoff): #later make this persistent and also how long. maybe also do a pan-clip
        s=docliponoff(onoff)
        await splitsend(ctx.channel,s,False)
        return





discord_token=os.getenv('IAMZ1_DISCORD_KEY')
bot.run(discord_token) 
