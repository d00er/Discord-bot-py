import discord 
from discord.ext import commands
import random, json, requests

from data_base.client import db_client
from data_base.model.user import User
from data_base.model.server import Server
from data_base.schemas.server import user_schema, server_schema

class secret(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is ready")

    @commands.command() 
    async def chambear(self, ctx, member:discord.Member = None):
        try:
            if member == None:
                member = ctx.author
            user = User(**user_schema(db_client.local.users.find_one({"id" : str(member.id)})))
        except Exception:
            error_embed = discord.Embed(title="BOT ERROR", description=" :(", color=discord.Color.red())
            error_embed.add_field(name="ERROR:", value="la base de datos no encontro tus datos", inline= False)   # the data base didnt find the member
            await ctx.send(embed=error_embed)

        amount=random.randint(100, 300)

        eco_embed = discord.Embed(title="Phew!", description="Despues de un largo dia de trabajo, esto es lo que ganaste!", color=discord.Color.green()) #After a hard day of worj this is what you have earned!
        eco_embed.add_field(name="Ganancias:", value=f"${amount}.", inline= False) # Earnings:
        
        new_balance = user.balance + amount
        user.balance = new_balance

        eco_embed.add_field(name="Nuevo saldo:", value=f"${new_balance}.", inline= False) # New balance
        list_images= ["https://tenor.com/es/view/coin-gif-22689269","https://media.tenor.com/x7QG3N0bdXcAAAAi/taffy-taffy-coin.gif"]
        inti = random.randint(0, 1)
        eco_embed.set_image(url=list_images[inti])
        db_client.local.users.find_one_and_replace({"id" : str(member.id)}, dict(user))

        await ctx.send(embed=eco_embed)

    @commands.command() 
    async def boludo(self, ctx, member:discord.Member = None):
        if member == None:
            await ctx.send(f"{ctx.author} sos un boludo!")
        else:
            await ctx.send(f"{member.name} es un boludo!")


async def setup(client):
    await client.add_cog(secret(client))