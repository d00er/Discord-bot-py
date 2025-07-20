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

            welcome_embed = discord.Embed(title=f"Bienvenido a {member.guild.name}!", description=f"Bienvenido al servidor! Eres el miembro número: {member.guild.member_count}", color=discord.Color.purple()) # Welcome to the server! You are member 
            
            welcome_embed.add_field(name="Bienvenido al servidor!", value=this_server.messageW, inline=False) # Welcome to the server!
            welcome_embed.set_image(url=this_server.imageurlW)
            welcome_embed.set_footer(text="Gracias por unirte!", icon_url=member.avatar) # Glad youve joined!

            auto_role = discord.utils.get(member.guild.roles, name=this_server.autoroleW)

            await member.add_roles(auto_role)

            if this_server.channelW is None:
                await member.send(embed=welcome_embed)
            elif this_server.channelW is not None:
                welcome_channel = discord.utils.get(member.guild.channels, name=this_server.channelW)

                await welcome_channel.send(embed=welcome_embed)

        except Exception as error:
            print(error)
    
    
    @commands.group(name="welcome", invoke_without_command = True)
    @commands.has_permissions(administrator=True)
    async def welcome(self, ctx):
        try:
            info_embed = discord.Embed(title="Configuracion del sistema de bienvenida", description="Crea un sistema de bienvenida unico para tu servidor!", color=discord.Color.teal()) # Welcome system setup # create a unique welcome system for your server
            info_embed.add_field(name="welcome autorole", value="Selecciona el rol que va a tener el miembro cuando se una al server!", inline=False) #select the role that is going to have a person when he enters the server!
            info_embed.add_field(name="welcome message", value="Selecciona el mensaje que estara en el embed de bienvenida!", inline=False) # select the message that is going to be in the welcome embed!
            info_embed.add_field(name="welcome channel", value="Selecciona el canal donde estara el embed de bienvenida!", inline=False) #select the channel that your card is going to be sent in!
            info_embed.add_field(name="welcome image", value="Selecciona la imagen que estara en el embed de bienvenida!", inline=False) #select the image that is going to be in the welcome of a new member
            
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

        welcome_embed = discord.Embed(title="Perfecto!", description="Lo hiciste!", color=discord.Color.teal())
        welcome_embed.add_field(name="Commando exitoso", value=f"{role.name} es ahora el autorol de bienvenida" , inline=False)
        welcome_embed.set_image(url=this_server.imageurlW)
        await ctx.send(embed = welcome_embed)
    
    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def message(self, ctx, *, msg):
        try:
            this_server = Server(**server_schema(db_client.local.servers.find_one({"id": str(ctx.guild.id)})))
            this_server.messageW = str(msg)
            db_client.local.servers.find_one_and_replace({"id": str(ctx.guild.id)}, dict(this_server))
        except Exception as error:
            print(error)
        welcome_embed = discord.Embed(title="Perfecto!", description="Lo hiciste!", color=discord.Color.teal())
        welcome_embed.add_field(name="Commando exitoso", value=f"Tu mensaje es ahora el mensaje de bienvenida" , inline=False)
        welcome_embed.set_image(url=this_server.imageurlW)
        await ctx.send(embed = welcome_embed)

    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def channel(self, ctx, channel:discord.TextChannel):
        try:
            this_server = Server(**server_schema(db_client.local.servers.find_one({"id": str(ctx.guild.id)})))
            this_server.channelW = str(channel.name)
            db_client.local.servers.find_one_and_replace({"id": str(ctx.guild.id)}, dict(this_server))
        except Exception as error:
            print(error)
        welcome_embed = discord.Embed(title="Perfecto!", description="Lo hiciste!", color=discord.Color.teal())
        welcome_embed.add_field(name="Commando exitoso", value=f"{channel.name} es ahora el canal de los mensajes de bienvenida" , inline=False)
        welcome_embed.set_image(url=this_server.imageurlW)
        await ctx.send(embed = welcome_embed)

    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def imageurl(self, ctx, *, url):
        try:
            this_server = Server(**server_schema(db_client.local.servers.find_one({"id": str(ctx.guild.id)})))
            this_server.imageurlW = str(url)
            db_client.local.servers.find_one_and_replace({"id": str(ctx.guild.id)}, dict(this_server))
        except Exception as error:
            print(error)
        welcome_embed = discord.Embed(title="Perfecto!", description="Lo hiciste!", color=discord.Color.teal())
        welcome_embed.add_field(name="Commando exitoso", value=f"esta imagen ahora es la imagen de los mensajes de bienvenida" , inline=False)
        welcome_embed.set_image(url=this_server.imageurlW)
        await ctx.send(embed = welcome_embed)

async def setup(client):
    await client.add_cog(welcome2(client))