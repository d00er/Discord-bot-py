# especificar bien comandos

import discord 
from discord.ext import commands
import json

class configs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is ready")
    
    @commands.command()
    async def update(self, ctx): ###
        embed_message = discord.Embed(title="LAST UPDATE", description="current version: 0.3", color=discord.Color.purple()) #ctx.author.color
        embed_message.add_field(name="-CODE REWORK", value="all the data is secure in a data base", inline=False)

        await ctx.send(embed=embed_message)

    @commands.group(name="help", invoke_without_command = True)
    async def help(self, ctx):
        embed_message = discord.Embed(title="Help", description="types of commands of the bot", color=discord.Color.purple()) #ctx.author.color
        embed_message.add_field(name="this bot has in total:", value="50 commands for you to explore!", inline=False)
        embed_message.add_field(name="help economy", value="see the commands related to economy", inline=False)
        embed_message.add_field(name="help moderation", value="see the commands related to moderation", inline=False)
        embed_message.add_field(name="help fun", value="see the commands related to games", inline=False)
        embed_message.add_field(name="help welcome", value="see the commands related to welcome of a member", inline=False)
        embed_message.add_field(name="help goodbye", value="see the commands related to saying bye to a member", inline=False)
        embed_message.add_field(name="help levels", value="see the commands related to rank", inline=False)
        embed_message.add_field(name="help music", value="see the commands related to music", inline=False)
        embed_message.add_field(name="help other", value="other commands", inline=False)
        embed_message.set_image(url=ctx.guild.icon)

        await ctx.send(embed=embed_message)

    @help.command()
    async def economy(self, ctx):
        embed_message = discord.Embed(title="Economy commands", description="commands related to economy on the bot", color=discord.Color.purple()) #ctx.author.color
        embed_message.add_field(name="balance",  value="see your balance in this server, you'll need to clarify a member", inline=False)
        embed_message.add_field(name="beg", value="while begging you have a small probability of getting robbed", inline=False)
        embed_message.add_field(name="work", value="work to gain money", inline=False)
        embed_message.add_field(name="steal", value="steals someones money, youll need to clarify a member (they police can catch you)", inline=False)
        embed_message.add_field(name="deposite", value="deposit money, youll need to clarify an amount", inline=False)
        embed_message.add_field(name="withdraw", value="withdraw the money that you deposited previously, youll need to clarify an amount", inline=False)
        embed_message.add_field(name="shop", value="see the shop", inline=False)
        embed_message.add_field(name="buy", value="buy objects from the shop, you need to specify the name of the object", inline=False)
        embed_message.add_field(name="addObject", value="add an object to the store, to use it you have to put [name of the object]/[price of the object]", inline=False)
        embed_message.add_field(name="deleteObject", value="delete an object to the store, to use it you have to put the name of the object", inline=False)
        embed_message.add_field(name="objects", value="see your current objects", inline=False)

        await ctx.send(embed=embed_message)

    @help.command()
    async def moderation(self, ctx):
        embed_message = discord.Embed(title="Moderation commands", description="commands related to moderation on the bot", color=discord.Color.purple()) 
        embed_message.add_field(name="kick", value="kick a member", inline=False)
        embed_message.add_field(name="ban", value="ban a member", inline=False)
        embed_message.add_field(name="unban", value="unban a member", inline=False)
        embed_message.add_field(name="setmuterole", value="you need to specify a role id", inline=False)
        embed_message.add_field(name="mute", value="mute a member", inline=False)
        embed_message.add_field(name="unmute", value="unmute a member", inline=False)

        await ctx.send(embed=embed_message)
    
    @help.command()
    async def fun(self, ctx):
        embed_message = discord.Embed(title="fun commands", description="commands related to games on the bot", color=discord.Color.purple()) 
        embed_message.add_field(name="8ball", value="ask a question to the 8 ball", inline=False)
        embed_message.add_field(name="meme", value="receive a random meme", inline=False)

        await ctx.send(embed=embed_message)

    @help.command()
    async def welcome(self, ctx):
        embed_message = discord.Embed(title="Welcome commands", description="the goodbye group to use its comands you have to put first the name of the group and then its command for example: !welcome channel", color=discord.Color.purple()) 
        embed_message.add_field(name="welcome", value="the welcome group", inline=False)
        embed_message.add_field(name="autorole", value="the id of the role that its given when a person joins the server. You need to specify a role id", inline=False)
        embed_message.add_field(name="channel", value="the id of the channel in the welcome group. You need to specify the channel id", inline=False)
        embed_message.add_field(name="message", value="the message in the welcome group", inline=False)
        embed_message.add_field(name="imageUrl", value="the imageUrl in the welcome group", inline=False)
        
        await ctx.send(embed=embed_message)
    
    @help.command()
    async def goodbye(self, ctx):
        embed_message = discord.Embed(title="Welcome commands", description="commands related to the welcome of a member on the bot (it also works with goodbye command too)", color=discord.Color.purple()) 
        embed_message.add_field(name="goodbye", value="the goodbye group to use its comands you have to put first the name of the group (goodbye) and then its command for example: !goodbye channel ", inline=False)
        embed_message.add_field(name="channel", value="the id of the channel in the goodbye group. You need to specify the channel id", inline=False)
        embed_message.add_field(name="message", value="the message in the goodbye group", inline=False)
        embed_message.add_field(name="imageUrl", value="the imageUrl in the goodbye group", inline=False)
        
        await ctx.send(embed=embed_message)
    
    @help.command()
    async def music(self, ctx):
        embed_message = discord.Embed(title="Music commands", description="commands related to music on the bot", color=discord.Color.purple()) 
        embed_message.add_field(name="play", value="use it to play music on a vc. put the command and a link or text related to what you want to hear, if you are hearing something it only adds the song to the queue", inline=False)
        embed_message.add_field(name="skip", value="skip the current song", inline=False)
        embed_message.add_field(name="queue", value="the queue of the music", inline=False)
        embed_message.add_field(name="erase", value="erase the whole queue", inline=False)
        embed_message.add_field(name="remove", value="remove the first song of the queue", inline=False)
        embed_message.add_field(name="disconnect", value="disconnects the bot for the voice chat ", inline=False)
        
        await ctx.send(embed=embed_message)
    @help.command()
    async def levels(self, ctx):
        embed_message = discord.Embed(title="level commands", description="commands related to the level a members", color=discord.Color.purple()) 
        embed_message.add_field(name="lvl", value="see your level", inline=False)
        embed_message.add_field(name="level_channel", value="the customizable level channel, you need to add the id of a discord channel", inline=False)
        
        await ctx.send(embed=embed_message)

    @help.command()
    async def other(self, ctx):
        embed_message = discord.Embed(title="other commands", description="commands related to the welcome of a member on the bot", color=discord.Color.purple()) 
        embed_message.add_field(name="prefix", value="set the prefix of the server with the command: set_prefix", inline=False)
        embed_message.add_field(name="server id", value="see the id of the server with server_id", inline=False)
        embed_message.add_field(name="ping", value="current ping of the bot", inline=False)
        
        await ctx.send(embed=embed_message)

async def setup(client):
    await client.add_cog(configs(client))