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

    @commands.command(aliases=["embed", "make_EMBED", "message-embed"])
    async def embeds(self, ctx):
        embed_message = discord.Embed(title="Title of embed", description="Description of embed", color=discord.Color.green()) #ctx.author.color

        embed_message.set_author(name=f"Requested by {ctx.author.mention}", icon_url = ctx.author.avatar)
        embed_message.set_thumbnail(url=ctx.guild.icon)
        embed_message.set_image(url=ctx.guild.icon)
        embed_message.add_field(name="Field name", value="Field value", inline=False)
        embed_message.set_footer(text="This is the footer", icon_url=ctx.author.avatar)

        await ctx.send(embed = embed_message)

    
    

    @commands.command()
    async def configs(self, ctx):
        embed_message = discord.Embed(title="Configuration", description="things that you can configurate in this bot", color=discord.Color.green()) #ctx.author.color

        embed_message.add_field(name="prefix", value="set the prefix of the server with the command: set_prefix", inline=False)

        await ctx.send(embed=embed_message)
    
    @commands.command()
    async def update(self, ctx):
        embed_message = discord.Embed(title="LAST UPDATE", description="current version: 0.2", color=discord.Color.purple()) #ctx.author.color
        embed_message.add_field(name="-NEW ECONOMY COMMANDS", value="add and delete objects from the store", inline=False)
        embed_message.add_field(name="-MUSIC", value="music commands", inline=False)
        embed_message.add_field(name="-BIENVENIDAS Y DESPEDIDAS", value="welcome commands", inline=False)

        await ctx.send(embed=embed_message)

    @commands.group(name="help", invoke_without_command = True)
    async def help(self, ctx):
        embed_message = discord.Embed(title="Help", description="types of commands of the bot", color=discord.Color.purple()) #ctx.author.color
        embed_message.add_field(name="this bot has in total:", value="53 commands for you to explore!", inline=False)
        embed_message.add_field(name="help economy", value="see the commands related to economy", inline=False)
        embed_message.add_field(name="help moderation", value="see the commands related to moderation", inline=False)
        embed_message.add_field(name="help fun", value="see the commands related to fun", inline=False)
        embed_message.add_field(name="help welcome", value="see the commands related to welcome", inline=False)
        embed_message.add_field(name="help levels", value="see the commands related to rank", inline=False)
        embed_message.add_field(name="help music", value="see the commands related to music", inline=False)

        await ctx.send(embed=embed_message)

    @help.command()
    async def economy(self, ctx):
        embed_message = discord.Embed(title="Economy commands", description="commands related to economy on the bot", color=discord.Color.purple()) #ctx.author.color
        embed_message.add_field(name="balance",  value="see your balance in this server, youll need to clarify a member", inline=False)
        embed_message.add_field(name="beg", value="beg (you can get robbed bb)", inline=False)
        embed_message.add_field(name="work", value="work to gain money, espameable", inline=False)
        embed_message.add_field(name="steal", value="steals someones money, youll need to clarify a member", inline=False)
        embed_message.add_field(name="deposite", value="deposit money into your online fake bank account, youll need to clarify an amount", inline=False)
        embed_message.add_field(name="withdraw", value="withdraw the money that you deposited previously, youll need to clarify an amount", inline=False)
        embed_message.add_field(name="shop", value="see the shop", inline=False)
        embed_message.add_field(name="buy", value="buy objects from the shop", inline=False)
        embed_message.add_field(name="add_object", value="add an object to the store, to use it you have to put [name of the object]/[price of the object]", inline=False)
        embed_message.add_field(name="delete_object", value="delete an object to the store, to use it you have to put the name of the object", inline=False)
        embed_message.add_field(name="objects", value="see your current objects", inline=False)

        await ctx.send(embed=embed_message)

    @help.command()
    async def moderation(self, ctx):
        embed_message = discord.Embed(title="Moderation commands", description="commands related to moderation on the bot", color=discord.Color.purple()) 
        embed_message.add_field(name="kick", value="kick a member", inline=False)
        embed_message.add_field(name="ban", value="ban a member", inline=False)
        embed_message.add_field(name="unban", value="unban a member", inline=False)
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
        embed_message = discord.Embed(title="Welcome commands", description="commands related to the welcome of a member on the bot (it also works with goodbye command too)", color=discord.Color.purple()) 
        embed_message.add_field(name="welcome", value="the welcome group", inline=False)
        embed_message.add_field(name="goodbye", value="the goodbye group", inline=False)
        embed_message.add_field(name="autorole", value="the autorole in the welcome group", inline=False)
        embed_message.add_field(name="channel", value="the channel in the welcome group", inline=False)
        embed_message.add_field(name="message", value="the message in the welcome group", inline=False)
        embed_message.add_field(name="imageUrl", value="the imageUrl in the welcome group", inline=False)
        
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
        embed_message = discord.Embed(title="level commands", description="commands related to the welcome of a member on the bot", color=discord.Color.purple()) 
        embed_message.add_field(name="lvl", value="the welcome group", inline=False)
        
        await ctx.send(embed=embed_message)







async def setup(client):
    await client.add_cog(configs(client))