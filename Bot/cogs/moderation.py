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

    @commands.command(aliases=["smuterole","setmr","stmr"])
    @commands.has_permissions(administrator=True)
    async def setmuterol(self, ctx, mute_role: discord.Role):
        try:
            server = Server(**server_schema(db_client.local.servers.find_one({"id": str(ctx.guild.id)})))
            server.mute_role = mute_role.id

            db_client.local.servers.find_one_and_replace({"id": str(ctx.guild.id)}, dict(server))

            conf_embed = discord.Embed(title="Un exito!", color = discord.Color.green()) # Succes
            conf_embed.add_field(name="Seteo del rol", value=f"El rol muteado ahora es: {ctx.author.mention}", inline = False) # the mute role has been set by
        
            await ctx.send(embed = conf_embed)
        except Exception as error:
            print(error)

    @commands.command(name="mute")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member:discord.Member):
        try:
        
                server = Server(**server_schema(db_client.local.servers.find_one({"id": str(ctx.guild.id)})))
                mute_role = discord.utils.get(ctx.guild.roles, id=server.mute_role)
                print(mute_role)
                await member.add_roles(mute_role)
                
        except discord.Forbidden:
            print("No tienes los permisos para hacer esto") # you are not permited to do that
        
        conf_embed = discord.Embed(title="Un exito!", color = discord.Color.green())
        conf_embed.add_field(name="muteo", value=f"Has muteado a alguien! {ctx.author.mention}", inline = False)
        await ctx.send(embed = conf_embed)
    
    @commands.command(name="unmute")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member:discord.Member):
        try:
                server = Server(**server_schema(db_client.local.servers.find_one({"id": str(ctx.guild.id)})))
                mute_role = discord.utils.get(ctx.guild.roles, id=server.mute_role)
                print(mute_role)
                await member.remove_roles(mute_role)
        except discord.Forbidden:
            print("No tienes los permisos para hacer esto")
            
        conf_embed = discord.Embed(title="Succes!", color = discord.Color.green())
        conf_embed.add_field(name="Desmuteo", value=f"Haz desmuteado a alguien! {ctx.author.mention}", inline = False)
        await ctx.send(embed = conf_embed)


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *,  modreason: str):
        try:
            await ctx.guild.kick(member)
        except discord.Forbidden:
            print("No tienes los permisos para hacer esto")

        conf_embed = discord.Embed(title="KICK", color = discord.Color.red())
        conf_embed.add_field(name="Kickeado", value=f"{member.mention} a sido kickeado por {ctx.author.mention}", inline = False)
        conf_embed.add_field(name="Por:", value=modreason, inline = False)

        await ctx.send(embed = conf_embed)

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, modreason: str):
        try:
            await ctx.guild.ban(member)
        except discord.Forbidden:
            print("No tienes los permisos para hacer esto")


        conf_embed = discord.Embed(title="BAN", color = discord.Color.red())
        conf_embed.add_field(name="Baneo", value=f"{member.mention} ha sido baneado por {ctx.author.mention}", inline = False)
        conf_embed.add_field(name="Por", value=modreason, inline = False)

        await ctx.send(embed = conf_embed)

    @commands.command(name="unban")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id):
        user = discord.Object(user_id)
        try:
            await ctx.guild.unban(user)
        except discord.Forbidden:
            print("No tienes los permisos para hacer esto")

        conf_embed = discord.Embed(title="UNBAN", color = discord.Color.green())
        conf_embed.add_field(name="Desbaneo", value=f"@{user_id} ha sido desbaneado por {ctx.author.mention}", inline = False)

        await ctx.send(embed = conf_embed)

"""
    @commands.command()
    @commands.has_permissions(manage_messages=True) ###
    async def warn(self, ctx, member: discord.Member, *, reason="No reason provided"):
        server_data = self.servers.find_one({"id": str(ctx.guild.id)})
        if server_data is None:
            await ctx.send("This server isn't configured yet. Please use the setup command.")
            return

        user_data = self.users.find_one({"id": str(member.id)})
        if user_data is None:
            self.users.insert_one({"id": str(member.id), "warnings": []})
            user_data = self.users.find_one({"id": str(member.id)})

        warning = {"reason": reason, "date": ctx.message.created_at.isoformat()}
        self.users.update_one({"id": str(member.id)}, {"$push": {"warnings": warning}})

        embed = discord.Embed(title="Warning Issued", color=discord.Color.orange())
        embed.add_field(name="User", value=member.mention)
        embed.add_field(name="Reason", value=reason)
        embed.add_field(name="Moderator", value=ctx.author.mention)
        embed.set_thumbnail(url=member.avatar.url)
        await member.mention.send(embed=embed)

        #Optional: DM the user about the warning. Uncomment the below lines if you want to implement this.
        #try:
        #    await member.send(f"You have received a warning in {ctx.guild.name} for: {reason}")
        #except discord.Forbidden:
        #    await ctx.send(f"Could not DM {member.mention} about the warning.")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def removewarn(self, ctx, member: discord.Member, warn_id: int):
        server_data = await self.db["servers"].find_one({"id": str(ctx.guild.id)})
        if not server_data:
            await ctx.send("This server is not configured in the database.")
            return

        if not server_data.get("warnings"):
            await ctx.send("No warnings found for this server.")
            return

        user_warnings = server_data["warnings"].get(str(member.id), [])
        if not user_warnings:
            await ctx.send(f"{member.display_name} has no warnings.")
            return

        try:
            warning_to_remove = next((warn for warn in user_warnings if warn["id"] == warn_id), None)
            if warning_to_remove is None:
                await ctx.send(f"Warning with ID {warn_id} not found for {member.display_name}.")
                return
            
            user_warnings.remove(warning_to_remove)
            await self.db["servers"].update_one(
                {"id": str(ctx.guild.id)},
                {"$set": {f"warnings.{str(member.id)}": user_warnings}}
            )
            await ctx.send(f"Warning {warn_id} removed from {member.display_name}.")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command(name="kick_voice", description="Kicks a user from a voice channel.")
    async def kick_voice(self, ctx, member: discord.Member):
        if not member.voice:
            await ctx.respond("Este usuario no esta en un canal de voz", ephemeral=True)
            return

        try:
            await member.move_to(None)
            await ctx.respond(f"{member.mention} ha sido kickeado de un chat de voz")
        except discord.Forbidden:
            await ctx.respond("No tenemos permiso para hacer esto.", ephemeral=True)

"""


async def setup(client):
    await client.add_cog(moderation(client))