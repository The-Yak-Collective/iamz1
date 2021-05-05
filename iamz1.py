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

import discord
import asyncio
import os
import time
import datetime
import re
import subprocess
import sys

from dotenv import load_dotenv, find_dotenv
from discord.ext import tasks, commands


from discord_iamz1 import * #especially "bot"
ourdir=os.path.dirname(os.path.abspath(__file__))
load_dotenv(find_dotenv()) #'.env')
USERHOMEDIR=os.getenv('USERHOMEDIR',default="/media/pi/z1-drive/") 
WHEREIRUNDIR=os.getenv('WHEREIRUNDIR',default="/media/pi/z1-drive/maier/iamz1/") 
#PREAMBLE=os.getenv('YAK_ROVER_NAME') #happens in discord file

@bot.event #needed since it takes time to connect to discord
async def on_ready(): 
    print('We have logged in as {0.user}'.format(bot),  bot.guilds)
    return

@bot.command(name='test', help='test message. go to https://roamresearch.com/#/app/ArtOfGig/page/iBLdEt5Ji to see more about z1 yak rover project', before_invoke=gotit)
async def iamz_test(ctx):
        s='this is a test response from z1 rover bot who got a message from '+ctx.author.name
        await splitsend(ctx.channel,s,False)
        return



@bot.command(name='upload', help='upload an attached file to directory of user that sent the message. will only upload one file, for now', before_invoke=gotit)
async def iamz1_upload(ctx):
        s='i would have uploaded file to directory of '+ctx.author.name
#check there is a file
#check if there is a directory or create one if needed
#overwrite existing file
        await splitsend(ctx.channel,s,False)
        return

@bot.command(name='cmdupload', help='upload an attached file to general command directory . will only upload one file, for now', before_invoke=gotit)
async def iamz1_cmdupload(ctx):
    if (len(ctx.message.attachments)>0):
        print('has attachment')
        thefilename=ctx.message.attachments[0].filename
        with open(WHEREIRUNDIR+"/cmd/"+thefilename,'wb') as f:
            await ctx.message.attachments[0].save(f)#probbaly also works if we save direct to file name, not f
    s="uploaded file "+thefilename
    await splitsend(ctx.channel,s,False)
    return
    
@bot.command(name='cmdlist', help='list (python) commands available', before_invoke=gotit)
async def iamz1_cmdlist(ctx):
    thedir=WHEREIRUNDIR+'cmd'
    f=os.listdir(thedir)
    ff=[x for x in f if x[-3:]=='.py']
    s="list of python files in cmd directory:\n"+"\n".join(ff)
    await splitsend(ctx.channel,s,False)
    return

@bot.command(name='cmdrun', help='run X ARGS: run a file X (python) in the general directory. send next parameters to running. ', before_invoke=gotit)
async def iamz1_cmdrun(ctx,name,*args):
    s='i am running  file {0} in home directory, ({3}) with parameters {2}, for user {1}'.format(name,ctx.author.name," ".join(args),WHEREIRUNDIR)
#check there is a file and directory. if not say "oops"
    thefiletorun=WHEREIRUNDIR+'cmd/'+name
    if not os.path.exists(thefiletorun):
        print('oops no such file: '+thefiletorun)
        await splitsend(ctx.channel,'oops no such file: '+thefiletorun,False)
        return
#call script that runs file, etc into a text file
#send back message with pid, for killing
#script will send back the output file by curl
    sys.path.append(WHEREIRUNDIR)
    sys.path.append('/home/pi/SpiderPi/HiwonderSDK')
    thestringlist=["/bin/bash",WHEREIRUNDIR+"runcommand.bash","runpython3.bash",thefiletorun]+list(args)
    print(thestringlist)
    out = subprocess.Popen(thestringlist, 
           cwd=WHEREIRUNDIR,
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    s=s+ '\n'+str(thestringlist)+'\n'+str(stdout,"utf-8").replace("\\n",'\n')

    await splitsend(ctx.channel,s,False)
    return
        


@bot.command(name='raglist', help='show list of action groups we can rag')
async def iamz1_raglist(ctx):
    out = subprocess.Popen(['/usr/bin/python3', 'raglist.py'],
           cwd=WHEREIRUNDIR,
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    s='available action groups:\n'+str(stdout,"utf-8").replace("\\n",'\n')
    await splitsend(ctx.channel,s,False)
    return

@bot.command(name='stop', help='stops any ongoing action group (rag) and camera motion (cam). we hope', before_invoke=gotit)
async def iamz1_stop(ctx):
    out = subprocess.Popen(['/bin/bash', 'kill', '-9', '''$(ps ax | grep 'rag.py' | awk '{printf $1 " "}')'''],
           cwd=WHEREIRUNDIR,
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    s1='did i stop (freeze more like it)?'+str(stdout,"utf-8").replace("\\n",'\n')
    
    out1 = subprocess.Popen(['/bin/bash', 'kill', '-9', '''$(ps ax | grep 'cam.py' | awk '{printf $1 " "}')'''],
           cwd=WHEREIRUNDIR,
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    s2=s1+'\n'+str(stdout,"utf-8").replace("\\n",'\n')
    await splitsend(ctx.channel,s2,False)
    return
        
@bot.command(name='rag', help='run action group NAME [TIMES] times. "list" shows list of available actions. "stop" stops running action. ',before_invoke=gotit)
async def iamz1_rag(ctx, name, *args):
    out = subprocess.Popen(['/usr/bin/python3', 'rag.py', name]+list(args),
           cwd=WHEREIRUNDIR,
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    s=str(stdout,"utf-8").replace("\\n",'\n')
    await splitsend(ctx.channel,s,False)
    return

@bot.command(name='cam', help='move camera pan/tilt +/-/x OR x,y OR rest. "list" shows list of available actions. ', before_invoke=gotit)
async def iamz1_cam(ctx, *args):
    out = subprocess.Popen(['/usr/bin/python3', 'cam.py']+list(args),
           cwd=WHEREIRUNDIR,
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    s=str(stdout,"utf-8").replace("\\n",'\n')
    await splitsend(ctx.channel,s,False)
    return
        
        
@bot.command(name='unload', help='move all servos to unload configuration')
async def iamz1_unloadservos(ctx):
    out = subprocess.Popen(['/usr/bin/python3', 'testunload.py'],
           cwd=WHEREIRUNDIR,
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    s='ah. feeling unloaded'
    await splitsend(ctx.channel,s,False)
    return
        


@bot.command(name='run', help='run X ARGS: run a file X in the directory of user that sent the message. send next parameters to running. ', before_invoke=gotit)
async def iamz1_run(ctx,name,*args):
    s='i am running  file {0} in directory of {1} ({3}) with parameters {2}'.format(name,ctx.author.name," ".join(args),name2filename(ctx.author.name))
#check there is a file and directory. if not say "oops"
    thefiletorun=USERHOMEDIR+name2filename(ctx.author.name)+'/'+name
    if not os.path.exists(thefiletorun):
        print('oops no such file: '+thefiletorun)
        await splitsend(ctx.channel,'oops no such file: '+thefiletorun,False)
        return
#call script that runs file, etc into a text file
#send back message with pid, for killing
#script will send back the output file by curl
    thestringlist=["/bin/bash",WHEREIRUNDIR+"runcommand.bash",thefiletorun]+list(args)
    print(thestringlist)
    out = subprocess.Popen(thestringlist, 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    s=s+ '\n'+str(thestringlist)+'\n'+str(stdout,"utf-8").replace("\\n",'\n')

    await splitsend(ctx.channel,s,False)
    return
        
@bot.command(name='watchdog', help='watchdog X ARGS: run AS A WATCHDOG a file X in the directory of user that sent the message. send next parameters to running. ')
async def iamz1_runwatchdog(ctx,name,*args):
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
        
@bot.command(name='video', help='video start/stop duration. for now it can only start and only for 5 min. ', before_invoke=gotit)
async def iamz1_video(ctx,onoff, *arg):
        if len(arg)>0:
            dur=arg[0]
        else:
            dur="300"
        if (onoff=='off'):
            subprocess.call(['/bin/bash', 'stopvideo'],cwd=WHEREIRUNDIR)
            s='tried to turn off video using kill (stopvideo). if video was not running, effect on system stability unpredictable'
        else:
            subprocess.call(['/bin/bash', 'streamviatwilio', dur],cwd=WHEREIRUNDIR)
            s="tried to start video. unpredictible reults if last run not over yet. see video using 'runonviewer.html'."
        await splitsend(ctx.channel,s,False)
        return

async def gotit(ctx):
        s='I got: {0} from {1}'.format(ctx.message.content, ctx.author.name)
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
    st=PREAMBLE+": "+st
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
