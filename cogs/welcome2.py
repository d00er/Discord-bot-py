import discord 
from discord.ext import commands
import json

from data_base.client import db_client
from data_base.model.server import Server
from data_base.schemas.server import server_schema

class welcome2(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is ready")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            this_server = Server(**server_schema(db_client.local.servers.find_one({"id": str(member.guild.id)})))

            welcome_embed = discord.Embed(title=f"Welcome to {member.guild.name}!", description=f"Welcome to the server! You are member {member.guild.member_count}", color=discord.Color.purple())
            
            welcome_embed.add_field(name="Welcome to the server!", value=this_server.messageW, inline=False)
            welcome_embed.set_image(url=this_server.imageurlW)
            welcome_embed.set_footer(text="Glad youve joined!", icon_url=member.avatar)

            auto_role = discord.utils.get(member.guild.roles, name=this_server.autoroleW)

            await member.add_roles(auto_role)

            if this_server.channelW is None:
                await member.send(embed=welcome_embed)
            elif this_server.channelW is not None:
                welcome_channel = discord.utils.get(member.guild.channels, name=this_server.channelW)

                await welcome_channel.send(embed=welcome_embed)

        except Exception as error:
            print(error)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            this_server = Server(**server_schema(db_client.local.servers.find_one({"id": str(member.guild.id)})))

            welcome_embed = discord.Embed(title=f"Welcome to {member.guild.name}!", description=f"Welcome to the server! You are member {member.guild.member_count}", color=discord.Color.purple())
            
            welcome_embed.add_field(name="Welcome to the server!", value=this_server.messageG, inline=False)
            welcome_embed.set_image(url=this_server.imageurlG)
            welcome_embed.set_footer(text="Glad youve joined!", icon_url=member.avatar)


            if this_server.channelG is None:
                await member.send(embed=welcome_embed)
            elif this_server.channelG is not None:
                welcome_channel = discord.utils.get(member.guild.channels, name=this_server.channelG)

                await welcome_channel.send(embed=welcome_embed)

        except Exception as error:
            print(error)
    
    @commands.group(name="welcome", invoke_without_command = True)
    @commands.has_permissions(administrator=True)
    async def welcome(self, ctx):
        try:
            info_embed = discord.Embed(title="Welcome system setup", description="create a unique welcome system for your server", color=discord.Color.teal())
            info_embed.add_field(name="autorole", value="select the role that is going to have a person when he enters the server!", inline=False)
            info_embed.add_field(name="message", value="select the message that is going to be in the welcome embed!", inline=False)
            info_embed.add_field(name="channel", value="select the channel that your card is going to be sent in!", inline=False)
            info_embed.add_field(name="image", value="select the image that is going to be in the welcome of a new member", inline=False)
            
            await ctx.send(embed = info_embed)
        except Exception as error:
            print(error)

    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def autorole(self, ctx, role: discord.Role):
        try:
            this_server = Server(**server_schema(db_client.local.servers.find_one({"id": str(ctx.guild.id)})))
            this_server.autoroleW = str(role.name)
            db_client.local.servers.find_one_and_replace({"id": str(ctx.guild.id)}, dict(this_server))
        except Exception as error:
            print(error)

        info_embed = discord.Embed(title="succes", description="succes", color=discord.Color.teal())
        info_embed.add_field(name="succes", value="succes", inline=False)
        await ctx.send(embed = info_embed)
    
    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def message(self, ctx, *, msg):
        try:
            this_server = Server(**server_schema(db_client.local.servers.find_one({"id": str(ctx.guild.id)})))
            this_server.messageW = str(msg)
            db_client.local.servers.find_one_and_replace({"id": str(ctx.guild.id)}, dict(this_server))
        except Exception as error:
            print(error)
        info_embed = discord.Embed(title="succes", description="succes", color=discord.Color.teal())
        info_embed.add_field(name="succes", value="succes", inline=False)
        await ctx.send(embed = info_embed)

    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def channel(self, ctx, channel:discord.TextChannel):
        try:
            this_server = Server(**server_schema(db_client.local.servers.find_one({"id": str(ctx.guild.id)})))
            this_server.channelW = str(channel.name)
            db_client.local.servers.find_one_and_replace({"id": str(ctx.guild.id)}, dict(this_server))
        except Exception as error:
            print(error)
        info_embed = discord.Embed(title="succes", description="succes", color=discord.Color.teal())
        info_embed.add_field(name="succes", value="succes", inline=False)
        await ctx.send(embed = info_embed)

    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def imageurl(self, ctx, *, url):
        try:
            this_server = Server(**server_schema(db_client.local.servers.find_one({"id": str(ctx.guild.id)})))
            this_server.imageurlW = str(url)
            db_client.local.servers.find_one_and_replace({"id": str(ctx.guild.id)}, dict(this_server))
        except Exception as error:
            print(error)
        info_embed = discord.Embed(title="succes", description="succes", color=discord.Color.teal())
        info_embed.add_field(name="succes", value="succes", inline=False)
        await ctx.send(embed = info_embed)
    
    @commands.group(name="goodbye", invoke_without_command = True)
    @commands.has_permissions(administrator=True)
    async def goodbye(self, ctx):
        try:
            info_embed = discord.Embed(title="Welcome system setup", description="create a unique goodbye system for your server", color=discord.Color.teal())
            info_embed.add_field(name="message", value="select the message that is going to be in the welcome embed!", inline=False)
            info_embed.add_field(name="channel", value="select the channel that your card is going to be sent in!", inline=False)
            info_embed.add_field(name="image", value="select the image that is going to be in the welcome of a new member", inline=False)
            
            await ctx.send(embed = info_embed)
        except Exception as error:
            print(error)
    
    @goodbye.command()
    @commands.has_permissions(administrator=True)
    async def message(self, ctx, *, msg):
        try:
            this_server = Server(**server_schema(db_client.local.servers.find_one({"id": str(ctx.guild.id)})))
            this_server.messageG = str(msg)
            db_client.local.servers.find_one_and_replace({"id": str(ctx.guild.id)}, dict(this_server))
        except Exception as error:
            print(error)
        info_embed = discord.Embed(title="succes", description="succes", color=discord.Color.teal())
        info_embed.add_field(name="succes", value="succes", inline=False)
        await ctx.send(embed = info_embed)

    @goodbye.command()
    @commands.has_permissions(administrator=True)
    async def channel(self, ctx, channel:discord.TextChannel):
        try:
            this_server = Server(**server_schema(db_client.local.servers.find_one({"id": str(ctx.guild.id)})))
            this_server.channelG = str(channel.name)
            db_client.local.servers.find_one_and_replace({"id": str(ctx.guild.id)}, dict(this_server))
        except Exception as error:
            print(error)
        info_embed = discord.Embed(title="succes", description="succes", color=discord.Color.teal())
        info_embed.add_field(name="succes", value="succes", inline=False)
        await ctx.send(embed = info_embed)

    @goodbye.command()
    @commands.has_permissions(administrator=True)
    async def imageurl(self, ctx, *, url):
        try:
            this_server = Server(**server_schema(db_client.local.servers.find_one({"id": str(ctx.guild.id)})))
            this_server.imageurlG = str(url)
            db_client.local.servers.find_one_and_replace({"id": str(ctx.guild.id)}, dict(this_server))
        except Exception as error:
            print(error)
        info_embed = discord.Embed(title="succes", description="succes", color=discord.Color.teal())
        info_embed.add_field(name="succes", value="succes", inline=False)
        await ctx.send(embed = info_embed)

async def setup(client):
    await client.add_cog(welcome2(client))