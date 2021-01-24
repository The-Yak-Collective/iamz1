#discord bot to act as interface for z1 yak rover
#use GIGAYAK_DISCORD_KEY as an env variable - the key for discord bot. needs read/write permission to channels

#from discord.ext import tasks, commands
import discord
import asyncio
import os
import time
import datetime

from dotenv import load_dotenv


from discord_iamz1 import *



load_dotenv('.env')


@client.event #needed since it takes time to connect to discord
async def on_ready(): 
    print('We have logged in as {0.user}'.format(client),  client.guilds)
    return


def allowed(x,y): #is x allowed to play with item created by y
#permissions - some activities can only be done by yakshaver, etc. or by person who initiated action
    if x==y: #same person. setting one to zero will force role check
        return True
    mid=client.guilds[0].get_member(message.author.id)
    r=[x.name for x in mid.roles]
    if 'yakshaver' in r or 'yakherder' in r: #for now, both roles are same permissions
        return True
    return False


@client.event 
async def on_message(message): 
    if message.author == client.user:
        return #ignore own messages to avoid loops

    dmtarget=await dmchan(message.author.id) #build backchannel to user, so we can choose to  not answer in general channel

    if message.content.startswith("$z1test"):
        s='this is a test response from z1 rover bot'
        await splitsend(message.channel,s,False)
        return
		
    if message.content.startswith("$z1help"):
        s='''
$z1help               this message
$z1test               a test message

go to https://roamresearch.com/#/app/ArtOfGig/page/iBLdEt5Ji to see more about z1 yak rover project
        '''
        await splitsend(message.channel,s,True)
        return
    return



async def dmchan(t):
#create DM channel betwen bot and user
    target=client.get_user(t)
    if (not target): 
        print("unable to find user and create dm",flush=True)
    return target
    target=target.dm_channel
    if (not target): 
        print("need to create dm channel",flush=True)
        target=await client.get_user(t).create_dm()
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
client.run(discord_token) 
