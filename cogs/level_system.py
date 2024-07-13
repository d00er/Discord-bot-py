import discord 
from discord.ext import commands
import json, asyncio, random, math


class level_system(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.client.loop.create_task(self.save())

        with open("files/users.json", "r") as f:
            self.users = json.load(f)

    def level_up(self, author_id):
        current_experience = self.users[author_id]["Experience"]
        current_level = self.users[author_id]["Level"]

        if current_experience < math.ceil((6 * (current_level) ** 4) / 2.5):
            return False
        else:
            self.users[author_id]["Level"] += 1
            return True


    async def save(self):
        await self.client.wait_until_ready()
        while not self.client.is_closed():
            with open("files/users.json", "w") as f:
                json.dump(self.users, f, indent=4)
            await asyncio.sleep(5)

        


    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is ready")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.client.user.id:
            return
        
        author_id = str(message.author.id)

        if not author_id in self.users:
            self.users[author_id] = {}
            self.users[author_id]["Level"] = 1
            self.users[author_id]["Experience"]=0
        
        random_exp = random.randint(5, 15)

        self.users[author_id]["Experience"]+= random_exp
        try:
            if self.level_up(author_id):
                levelup_embed = discord.Embed(title= "Wohoo - level up", color=discord.Color.green())
                levelup_embed.add_field(name="Congrats", value=f"{message.author.mention} has just leveled up to: {self.users[author_id]["Level"]}")
                await message.channel.send(embed = levelup_embed)
        except Exception as error:
            print(error)

    @commands.command(aliases=["r","lvl","rank"])
    async def level(self, ctx, usuario:discord.User= None):
        try:
            if usuario == None:
                usuario = ctx.author

            level_embed = discord.Embed(title= f"{usuario.name}s level and experience are:", color=discord.Color.random())
            level_embed.add_field(name="Level", value=self.users[str(usuario.id)]["Level"])
            level_embed.add_field(name="Experience", value=self.users[str(usuario.id)]["Experience"])
            level_embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar)

            await ctx.send(embed = level_embed)
        except Exception as error:
            print(error)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def level_channel(self, ctx, channel:discord.TextChannel):
        self.data[str(ctx.guild.id)]["Channel"] = str(channel.name)

        with open("files/welcome.json", "w") as f:
            json.dump(self.data, f, indent=4)
        

        
async def setup(client):
    await client.add_cog(level_system(client))