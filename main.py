# Need to implement multi-server support
# add scheduled voting

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
async def poll(ctx,action,id=None):
    if action == "create":
        if id == None:
            pass #error

        message = await ctx.send("```FPTP or IRV?```")
        def check(reaction,user):
            return user == ctx.author and str(reaction.emoji) in ['<:FPTPemote:714825461825536051>','<:IRVemote:714827414106013817>']
        await message.add_reaction('<:FPTPemote:714825461825536051>')
        await message.add_reaction('<:IRVemote:714827414106013817>')
        try:
            reaction, user = await bot.wait_for('reaction_add',timeout=30.0,check=check)
            if str(reaction.emoji) == '<:FPTPemote:714825461825536051>':
                polltype = "FPTP"
            if str(reaction.emoji) == '<:IRVemote:714827414106013817>':
                polltype = "IRV"
            await message.clear_reaction('<:FPTPemote:714825461825536051>')
            await message.clear_reaction('<:IRVemote:714827414106013817>')
            await ctx.send("Poll duration? (hours)")
            try:
                
            create_poll()
            channel = ctx.channel
            message = await channel.fetch_message(id)
        except asyncio.TimeoutError:
            await message.clear_reaction('<:FPTPemote:714825461825536051>')
            await message.clear_reaction('<:IRVemote:714827414106013817>')
            await message.edit(content="```FPTP or IRV? **(Timed out)**```")

        await ctx.send("Done.")
    if action == "remove":
        pass
    if action == "flush":
        pass
    if action == "extend":
        pass
    if action == "help":
        pass

@bot.command()
async def pollmanifest(ctx):
    pass

bot.run(key)