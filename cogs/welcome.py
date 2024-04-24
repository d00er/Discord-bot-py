import discord 
from discord.ext import commands
import json

class welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

        with open("files/welcome.json", "r") as f:
            self.data = json.load(f)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is ready")
    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            with open("files/welcome.json") as f:
                data = json.load(f)
            welcome_embed = discord.Embed(title=f"Welcome to {member.guild.name}!", description=f"Welcome to the server! You are member {member.guild.member_count}", color=discord.Color.purple())
            
            welcome_embed.add_field(name="Welcome to the server!", value=data[str(member.guild.id)]["Message"], inline=False)
            welcome_embed.set_image(url=data[str(member.guild.id)]["ImageUrl"])
            welcome_embed.set_footer(text="Glad youve joined!", icon_url=member.avatar)

            auto_role = discord.utils.get(member.guild.roles, name=data[str(member.guild.id)]["AutoRole"])

            await member.add_roles(auto_role)

            if data[str(member.guild.id)]["Channel"] is None:
                await member.send(embed=welcome_embed)
            elif data[str(member.guild.id)]["Channel"] is not None:
                welcome_channel = discord.utils.get(member.guild.channels, name=data[str(member.guild.id)]["Channel"])

                await welcome_channel.send(embed=welcome_embed)
        except Exception as error:
            print(error)



    @commands.group(name="welcome", invoke_without_command = True)
    @commands.has_permissions(administrator=True)
    async def welcome(self, ctx):

        with open("files/welcome.json", "r") as f:
            data = json.load(f)

        data[str(ctx.guild.id)] = {}
        data[str(ctx.guild.id)]["Channel"] = None
        data[str(ctx.guild.id)]["Message"] = None
        data[str(ctx.guild.id)]["AutoRole"] = None
        data[str(ctx.guild.id)]["ImageUrl"] = None
        

        with open("files/welcome.json", "w") as f:
            json.dump(data, f, indent=4)
            
        info_embed = discord.Embed(title="Welcome system setup", description="create a unique welcome system for your server", color=discord.Color.teal())
        info_embed.add_field(name="autorole", value="select the role that is going to have a person when he enters the server!", inline=False)
        info_embed.add_field(name="message", value="select the message that is going to be in the welcome embed!", inline=False)
        info_embed.add_field(name="channel", value="select the channel that your card is going to be sent in!", inline=False)
        info_embed.add_field(name="image", value="select the image that is going to be in the welcome of a new member", inline=False)
        
        await ctx.send(embed = info_embed)


    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def autorole(self, ctx, role:discord.Role):
        self.data[str(ctx.guild.id)]["AutoRole"] = str(role.name)

        with open("files/welcome.json", "w") as f:
            json.dump(self.data, f, indent=4)
    
    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def message(self, ctx, *, msg):
        self.data[str(ctx.guild.id)]["Message"] = str(msg)

        with open("files/welcome.json", "w") as f:
            json.dump(self.data, f, indent=4)
    
    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def channel(self, ctx, channel:discord.TextChannel):
        self.data[str(ctx.guild.id)]["Channel"] = str(channel.name)

        with open("files/welcome.json", "w") as f:
            json.dump(self.data, f, indent=4)

    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def imageurl(self, ctx, *, url):
        self.data[str(ctx.guild.id)]["ImageUrl"] = str(url)

        with open("files/welcome.json", "w") as f:
            json.dump(self.data, f, indent=4)




async def setup(client):
    await client.add_cog(welcome(client))

    #:)