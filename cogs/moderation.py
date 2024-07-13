import discord 
from discord.ext import commands
import json

from data_base.client import db_client
from data_base.model.server import Server
from data_base.schemas.server import server_schema


class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is ready")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def erase(self, ctx, count: int):
        await ctx.channel.purge(limit=count)
        await ctx.send(f"{count} message(s) have been deleted")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setmuterol(self, ctx, role:discord.Role):

        server = Server(**server_schema(db_client.local.servers.find_one({"id": str(ctx.guild.id)})))
        server.mute_role = role

        db_client.local.servers.find_one_and_replace({"id": str(ctx.guild.id)}, server)
        
        """with open("files/mutes.json", "r") as f:
            mute_role = json.load(f)
            mute_role[str(ctx.guild.id)] = role.id

        with open("files/mutes.json", "w") as f:
            json.dump(mute_role, f, indent=4)"""

        conf_embed = discord.Embed(title="Succes!", color = discord.Color.green())
        conf_embed.add_field(name="set the role", value=f"the mute role has been set by {ctx.author.mention}", inline = False)
        
        await ctx.send(embed = conf_embed)
    
    @commands.command(name="mute")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member:discord.Member):
        try:
            """ with open("files/mutes.json", "r") as f:
                role = json.load(f)
                print(role[str(ctx.guild.id)])
                mute_role=discord.utils.get(ctx.guild.roles, id=role[str(ctx.guild.id)])"""
            server = Server(**server_schema(db_client.local.servers.find_one({"id": str(ctx.guild.id)})))
            mute_role = server.mute_role
            print(discord.Role(mute_role))
            await member.add_roles(mute_role)
        except discord.Forbidden:
            print("no esta permitido papi")
        
        conf_embed = discord.Embed(title="Succes!", color = discord.Color.green())
        conf_embed.add_field(name="mute", value=f"you muted someone! {ctx.author.mention}", inline = False)
        await ctx.send(embed = conf_embed)
    
    @commands.command(name="unmute")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member:discord.Member):
        try:
            """with open("files/mutes.json", "r") as f:
                role = json.load(f)
                mute_role=discord.utils.get(ctx.guild.roles, id=role[str(ctx.guild.id)])"""
            server = Server(**server_schema(db_client.local.servers.find_one({"id": str(ctx.guild.id)})))
            mute_role = server.mute_role

            await member.remove_roles(mute_role)
        except discord.Forbidden:
            print("no esta permitido papi")
            
        conf_embed = discord.Embed(title="Succes!", color = discord.Color.green())
        conf_embed.add_field(name="unmute", value=f"you unmuted someone! {ctx.author.mention}", inline = False)
        await ctx.send(embed = conf_embed)


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *,  modreason: str):
        await ctx.guild.kick(member)

        conf_embed = discord.Embed(title="Epic", color = discord.Color.green())
        conf_embed.add_field(name="Kicked", value=f"{member.mention} has been kicked by {ctx.author.mention}", inline = False)
        conf_embed.add_field(name="Reason", value=modreason, inline = False)

        await ctx.send(embed = conf_embed)

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, modreason: str):
        try:
            await ctx.guild.ban(member)
        except discord.Forbidden:
            print("no podes, no lo tenes permitido")


        conf_embed = discord.Embed(title="Epic", color = discord.Color.green())
        conf_embed.add_field(name="Banned", value=f"{member.mention} has been banned by {ctx.author.mention}", inline = False)
        conf_embed.add_field(name="Reason", value=modreason, inline = False)

        await ctx.send(embed = conf_embed)

    @commands.command(name="unban")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id):
        user = discord.Object(user_id)
        await ctx.guild.unban(user)

        conf_embed = discord.Embed(title="Epic", color = discord.Color.green())
        conf_embed.add_field(name="UnBanned", value=f"@{user_id} has been unbanned by {ctx.author.mention}", inline = False)

        await ctx.send(embed = conf_embed)




async def setup(client):
    await client.add_cog(moderation(client))