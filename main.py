# Need to implement multi-server support

import discord
from discord import File
from discord.ext import commands

import json
import asyncio

bot = commands.Bot(command_prefix = '.')

filelocation = '/Users/adityakannan/PythonProjects/DemocracyBot/'

with open(filelocation + 'key.json','r') as keys:
    key = json.load(keys)

def create_poll():
    try:
        with open(filelocation + 'pollmanifest.json','r') as manifest:
            pollmanifest = json.load(manifest)
    except:
        pollmanifest = []
        with open(filelocation + 'pollmanifest.json','w') as manifest:
            json.dump(pollmanifest,manifest)

    pollid = pollmanifest.append(len(pollmanifest))

    with open(filelocation + 'pollmanifest.json','w') as manifest:
            json.dump(pollmanifest,manifest)
        
    poll = []    
    with open(filelocation + 'polls/' + str(pollid) + '.json','w') as pollfile:
        json.dump(poll,pollfile)

def save_poll(): #need to save at 1 minute intervals + end of the poll
    pass

@bot.event
async def on_ready():
    print("DemocracyBot is ready")

@bot.command() #arg = create, delete, extend, help ; message id. Assign an ID to each poll
async def poll(ctx,type,id):
    if type == "create":
        create_poll()
        await ctx.send("Done.")
    if type == "remove":
        pass
    if type == "flush":
        pass
    if type == "extend":
        pass
    if type == "help":
        pass

@bot.command()
async def pollmanifest(ctx):
    pass

bot.run(key)