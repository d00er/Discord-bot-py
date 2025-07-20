import discord 
from discord.ext import commands
import json

from data_base.client import db_client
from data_base.model.server import Server
from data_base.schemas.server import server_schema

class goodbye(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is ready")
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            this_server = Server(**server_schema(db_client.local.servers.find_one({"id": str(member.guild.id)})))

            welcome_embed = discord.Embed(title=f"Adios :(", description=f"esperamos que la hayas pasado bien...", color=discord.Color.purple()) #Welcome to {member.guild.name}!   
            
            welcome_embed.add_field(name="Buena suerte!", value=this_server.messageG, inline=False) #elcome to the server!
            welcome_embed.set_image(url=this_server.imageurlG)
            welcome_embed.set_footer(text="Esperamos verte pronto!", icon_url=member.avatar) #Glad youve joined!


            if this_server.channelG is None:
                await member.send(embed=welcome_embed)
            elif this_server.channelG is not None:
                welcome_channel = discord.utils.get(member.guild.channels, name=this_server.channelG)

                await welcome_channel.send(embed=welcome_embed)

        except Exception as error:
            print(error)
    
    @commands.group(name="goodbye", invoke_without_command = True)
    @commands.has_permissions(administrator=True)
    async def goodbye(self, ctx):
        try:
            info_embed = discord.Embed(title="Configuracion del sistema de despedida", description="Crea un sistema de despedida para tu servidor!", color=discord.Color.teal()) # Welcome system setup # create a unique welcome system for your server
            info_embed.add_field(name="goodbye message", value="Selecciona el mensaje que estara en el embed de despedida!", inline=False) # select the message that is going to be in the welcome embed!
            info_embed.add_field(name="goodbye channel", value="Selecciona el canal donde estara el embed de despedida!", inline=False) #select the channel that your card is going to be sent in!
            info_embed.add_field(name="goodbye image", value="Selecciona la imagen que estara en el embed de despedida!", inline=False) #select the image that is going to be in the welcome of a new member
            
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
        goodbye_embed = discord.Embed(title="Perfecto!", description="Lo hiciste!", color=discord.Color.teal())
        goodbye_embed.add_field(name="Commando exitoso", value=f"Tu mensaje es ahora el mensaje de despedida" , inline=False)
        goodbye_embed.set_image(url=this_server.imageurlG)
        await ctx.send(embed = goodbye_embed)

    @goodbye.command()
    @commands.has_permissions(administrator=True)
    async def channel(self, ctx, channel:discord.TextChannel):
        try:
            this_server = Server(**server_schema(db_client.local.servers.find_one({"id": str(ctx.guild.id)})))
            this_server.channelG = str(channel.name)
            db_client.local.servers.find_one_and_replace({"id": str(ctx.guild.id)}, dict(this_server))
        except Exception as error:
            print(error)
        goodbye_embed = discord.Embed(title="Perfecto!", description="Lo hiciste!", color=discord.Color.teal())
        goodbye_embed.add_field(name="Commando exitoso", value=f"{channel.name} es ahora el canal de los mensajes de despedida" , inline=False)
        goodbye_embed.set_image(url=this_server.imageurlG)
        await ctx.send(embed = goodbye_embed)

    @goodbye.command()
    @commands.has_permissions(administrator=True)
    async def imageurl(self, ctx, *, url):
        try:
            this_server = Server(**server_schema(db_client.local.servers.find_one({"id": str(ctx.guild.id)})))
            this_server.imageurlG = str(url)
            db_client.local.servers.find_one_and_replace({"id": str(ctx.guild.id)}, dict(this_server))
        except Exception as error:
            print(error)
        goodbye_embed = discord.Embed(title="Perfecto!", description="Lo hiciste!", color=discord.Color.teal())
        goodbye_embed.add_field(name="Commando exitoso", value=f"esta imagen ahora es la imagen de los mensajes de despedida" , inline=False)
        goodbye_embed.set_image(url=this_server.imageurlW)
        await ctx.send(embed = goodbye_embed)

async def setup(client):
    await client.add_cog(goodbye(client))