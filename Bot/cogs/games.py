import discord 
from discord.ext import commands
import random, json, requests

class games(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is ready")

    @commands.command(aliases=["8ball", "bola8", "8bola"])
    async def bola_suerte(self, ctx, *, question):
        try:
            with open("C:/VICTORINO/Coding/PYTHON/Py-projects/discord_bot/bot/cogs/files/random.txt", "r") as r:
                random_responses = r.readlines()
                response = random.choice(random_responses)
            await ctx.send(response)
        except Exception as error:
            print(error)

    @commands.command()
    async def meme(self, ctx):
        try:
            response = requests.get("https://meme-api.com/gimme")
            json_data = json.loads(response.text)
            message = json_data["url"] 
            
            await ctx.send(message)
        except Exception as error: 
                print(error)
    
    @commands.command(name="rps", aliases=["rockpaperscissors"])
    async def rock_paper_scissors(self, ctx, choice: str):
        choices = ["piedra", "papel", "tijeras"]
        if choice.lower() not in choices:
            await ctx.send("Eleccion no valida, por favor elegir solo piedra, papel o tijeras...")
            return

        bot_choice = random.choice(choices)
        await ctx.send(f"Tu elegiste {choice.lower()}, Yo elegi {bot_choice}.")

        if choice.lower() == bot_choice:
            await ctx.send("Es un empate!")
        elif (choice.lower() == "piedra" and bot_choice == "tijeras") or \
            (choice.lower() == "papel" and bot_choice == "piedra") or \
            (choice.lower() == "tijeras" and bot_choice == "papel"):
            await ctx.send(f"Tu ganas! Haz elegido {choice} y yo elegi {bot_choice} ")
        else:
            await ctx.send(f"Tu perdiste! Haz elegido {choice} y yo elegi {bot_choice} ")


async def setup(client):
    await client.add_cog(games(client))