import discord 
from discord.ext import commands
import random, json, requests

class games(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is ready")

    @commands.command(aliases=["8ball", "bola_suert", "8bola"])
    async def bola_suerte(self, ctx, *, question):
        with open("files/random.txt", "r") as r:
            random_responses = r.readlines()
            response = random.choice(random_responses)
        await ctx.send(response)

    @commands.command()
    async def get_meme(self, ctx):
        response = requests.get("https://meme-api.com/gimme")
        json_data = json.loads(response.text)
        message = json_data["url"] 
        
        await ctx.send(message)


async def setup(client):
    await client.add_cog(games(client))