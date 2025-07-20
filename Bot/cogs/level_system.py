import discord 
from discord.ext import commands
import json, asyncio, random, math


from data_base.client import db_client
from data_base.model.user import User
from data_base.model.server import Server
from data_base.schemas.server import user_schema, server_schema


class level_system(commands.Cog):
    def __init__(self, client):
        self.client = client

    def level_up(self, author_id):
        current_user = User(**user_schema(db_client.local.users.find_one({"id": author_id})))

        current_experience = current_user.experience
        current_level = current_user.level

        if current_experience < math.ceil((6 * (current_level) ** 4) / 2.5):
            return False
        else:
            current_user.level += 1
            db_client.local.users.find_one_and_replace({"id": author_id}, dict(current_user))
            return True

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is ready")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.client.user.id:
            return
        
        server = Server(**server_schema(db_client.local.servers.find_one({"id": str(message.author.guild.id)})))
        
        author_id = str(message.author.id)
        
        try:
            user = db_client.local.users.find_one({"id": author_id})

            if user == None:
                new_user = User(id=author_id, level=1, experience=0, balance = 100, deposite=0, objects={})
                db_client.local.users.insert_one(dict(new_user))

            user = User(**user_schema(db_client.local.users.find_one({"id": author_id})))

            random_exp = random.randint(5, 15)
            user.experience += random_exp

            db_client.local.users.find_one_and_replace({"id": author_id}, dict(user))
        except Exception as error:
            print(error)
        

        try:
            if self.level_up(author_id):
                levelup_embed = discord.Embed(title= "WO HOOO - subes de nivel", color=discord.Color.green())
                levelup_embed.add_field(name="Felicidades", value=f"{message.author.mention} ha subido de nivel al nivel: {user.level + 1}")

                if server.level_channel!=None:
                    lvl_channel = discord.utils.get(message.author.guild.channels, name=server.level_channel)
                    
                    await lvl_channel.send(embed = levelup_embed)
                else:
                    await message.channel.send(embed = levelup_embed)
        except Exception as error:
            print(error)

    @commands.command(aliases=["r","lvl","rank"])
    async def level(self, ctx, usuario:discord.User = None):
        try:
            if usuario == None:
                usuario = ctx.author
            user_level = User(**user_schema(db_client.local.users.find_one({"id": str(usuario.id)}))) 
            
            level_embed = discord.Embed(title= f"El nivel y experiencia de {usuario.name} :", color=discord.Color.random())
            level_embed.add_field(name="Nivel", value=user_level.level)
            level_embed.add_field(name="Experiencia", value=user_level.experience)
            level_embed.set_footer(text=f"Pedido por {ctx.author.name}", icon_url=ctx.author.avatar)

            await ctx.send(embed = level_embed)

        except Exception as error:
            print(error)
    
    @commands.command(aliases=["lvlchannel","rankchannel","rChannel"])
    @commands.has_permissions(administrator=True)
    async def level_channel(self, ctx, channel:discord.TextChannel):
        try: 
            server = Server(**server_schema(db_client.local.servers.find_one({"id": str(ctx.guild.id)})))
            server.level_channel = channel.name

            db_client.local.servers.find_one_and_replace({"id": str(ctx.guild.id)}, dict(server))

            info_embed = discord.Embed(title="EXITO!", color = discord.Color.green())
            info_embed.add_field(name="El canal para los niveles ahora es:", value=f"{channel.name}")
            await ctx.send(embed = info_embed)
        except Exception as error:
            print(error)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reset_level(self, ctx, usuario:discord.User = None):
        try:
            if usuario == None:
                usuario = ctx.author
            user_level = User(**user_schema(db_client.local.users.find_one({"id": str(usuario.id)}))) 

            new_user_level = 1    
            new_user_experience= 1
            user_level.level = new_user_level
            user_level.experience = new_user_experience
            level_embed = discord.Embed(title= f"El nivel y experiencia de {usuario.name} :", color=discord.Color.random())
            level_embed.add_field(name="Nivel", value=user_level.level)
            level_embed.add_field(name="Experiencia", value=user_level.experience)
            level_embed.set_footer(text=f"Pedido por {ctx.author.name}", icon_url=ctx.author.avatar)

            db_client.local.users.find_one_and_replace({"id": str(usuario.id)}, dict(user_level) )
            await ctx.send(embed =level_embed)
        except Exception as error:
            print(error)
"""
    @commands.command(name="leaderboard", aliases=["lb"])
    async def leaderboard(self, ctx):
        try:
            server_data = Server(**server_schema(db_client.local.servers.find_one({"id": str(ctx.guild.id)})))
            if server_data is None:
                await ctx.send("Leaderboard not configured for this server.")
                return

            users_data = dict(db_client.local.users)  # Sort by level descending
            
            embed = discord.Embed(title="Level Leaderboard", color=discord.Color.blue())
            
            rank = 1
            for user_data in users_data:
                try:
                    member = ctx.guild.get_member(int(user_data["id"]))
                    if member is None:
                        continue  # Skip users not in the guild

                    embed.add_field(name=f"{rank}. {member.display_name}", value=f"Level: {user_data['level']}", inline=False)
                    rank += 1
                    if rank > 10: # Limit to top 10
                        break
                except Exception as e:
                    print(f"Error processing user {user_data.get('id', 'N/A')}: {e}")
                    continue #Skip users causing errors


            if rank == 1:
                await ctx.send("Leaderboard is empty.")
            else:
                await ctx.send(embed=embed)
        except Exception as error:
            print(error)
""" 
async def setup(client):
    await client.add_cog(level_system(client))