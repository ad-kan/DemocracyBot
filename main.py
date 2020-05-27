# Need to implement multi-server support
# Need scheduled voting

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

    pollid = len(pollmanifest)
    pollmanifest.append(pollid)

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

@bot.command() #arg = create, delete, extend, help ; message id. Assign an ID to each poll ; ONE POLL PER MESSAGE ; OPTION TO EITHER CONVERT MESSAGE TO POLL or make bot post poll. latter is better.
async def poll(ctx,action):
    if action == "create":
        def check(reaction,user):
            return str(reaction.emoji) in ['💌','🤖'] and user == ctx.author
        def check2(reaction,user):
            return user == ctx.author and str(reaction.emoji) in ['<:FPTPemote:714825461825536051>','<:IRVemote:714827414106013817>']
        def check3(message):
            return message.author.id == ctx.author.id and message.channel == ctx.channel
        
        message = await ctx.send("```Do you want to convert an existing message into a poll or make the bot post the poll?```")
        await message.add_reaction('💌')
        await message.add_reaction('🤖')
        try:
            reaction, user = await bot.wait_for('reaction_add',timeout=30.0,check=check)
            await message.clear_reaction('💌')
            await message.clear_reaction('🤖')
            
            if str(reaction.emoji) == '💌':
                post_type = "message"
            if str(reaction.emoji) == '🤖':
                post_type = "bot"

            message = await ctx.send("```FPTP or IRV?```")
            await message.add_reaction('<:FPTPemote:714825461825536051>')
            await message.add_reaction('<:IRVemote:714827414106013817>')
            try:
                reaction, user = await bot.wait_for('reaction_add',timeout=30.0,check=check2)
                await message.clear_reaction('<:FPTPemote:714825461825536051>')
                await message.clear_reaction('<:IRVemote:714827414106013817>')
                
                if str(reaction.emoji) == '<:FPTPemote:714825461825536051>':
                    polltype = "FPTP"
                if str(reaction.emoji) == '<:IRVemote:714827414106013817>':
                    polltype = "IRV"
                
                message = await ctx.send("```Poll duration? (hours)```")
                try:
                    duration = await bot.wait_for('message',check=check3,timeout=30.0)
                    duration = int(duration.content)
                except asyncio.TimeoutError:
                    await message.edit(content="```Poll duration? (hours) (timed out)```")
                except:
                    await ctx.send("Invalid entry. Integers only.")
                '''create_poll()
                channel = ctx.channel
                message = await channel.fetch_message(id)'''
            except asyncio.TimeoutError:
                await message.clear_reaction('<:FPTPemote:714825461825536051>')
                await message.clear_reaction('<:IRVemote:714827414106013817>')
                await message.edit(content="```FPTP or IRV? (timed out)```")
        except asyncio.TimeoutError:
            await message.edit(content="```Do you want to convert an existing message into a poll or make the bot post the poll? (timed out)```")
            await message.clear_reaction('💌')
            await message.clear_reaction('🤖')
        
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