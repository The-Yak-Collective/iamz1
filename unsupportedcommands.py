from discord_iamz1 import * #especially "bot"
from discordsupport import *

##from here unsupported functions

@bot.command(name='upload', help='upload an attached file to directory of user that sent the message. will only upload one file, for now', before_invoke=gotit)
async def iamz1_upload(ctx):
        s='i would have uploaded file to directory of '+ctx.author.name
#check there is a file
#check if there is a directory or create one if needed
#overwrite existing file
        await splitsend(ctx.channel,s,False)
        return

@bot.command(name='watchdog', help='watchdog X ARGS: run AS A WATCHDOG a file X in the directory of user that sent the message. send next parameters to running. ',hidden=True)
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

@bot.command(name='git', help='one day this will do a git pull action into user directory. ', hidden=True)
async def iamz1_git(ctx,git):
        s='i would have pulled git repository '+git+' into user dir '+ctx.author.name
#tbd - what about privacy?
        await splitsend(ctx.channel,s,False)
        return

##till here unsupported functions