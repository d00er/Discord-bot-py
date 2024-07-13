
import discord
from discord.ext import commands, tasks
from itertools import cycle
import consts
# python utils
import os, asyncio, json
# database
from cogs.data_base.client import db_client
from cogs.data_base.model.server import Server
from cogs.data_base.schemas.server import server_schema

# https://discord.com/oauth2/authorize?client_id=1219376993989169282&permissions=8&scope=bot



def get_server_prefixes(client, message):
    server_prefix= Server(**server_schema(db_client.local.servers.find_one({"id": str(message.guild.id)})))
    return server_prefix.prefix


intents=discord.Intents.all()
intents.message_content = True
intents.voice_states = True
client = commands.Bot(command_prefix=get_server_prefixes, intents=intents)
client.remove_command("help")

bot_status = cycle(["type in '!help' for help", "type !config to config de bot to your necesities", "thanks for using!"])
@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(bot_status)))

### EVENTS ###


@client.event
async def on_ready():
    await client.tree.sync()
    print('Logged on bot!')
    change_status.start()

@client.event
async def on_guild_join(guild):
    try:

        default_prefix = "!"
        new_server = dict(Server(id=str(guild.id), prefix=default_prefix))
        print(new_server)
        db_client.local.servers.insert_one(new_server)

    except Exception as error:
        print(error)

    with open("files/mutes.json", "r") as f:
        mute_role = json.load(f)
        mute_role[str(guild.id)] = None

    with open("files/mutes.json", "w") as f:
        json.dump(mute_role, f, indent=3)
    
    with open("files/shop.json", "r") as z:
        shop = json.load(z)
    shop[str(guild.id)] = {}

    with open("files/shop.json", "w") as f:
        json.dump(shop, f, indent=4)
    


@client.event
async def on_guild_remove(guild):

    db_client.local.servers.find_one_and_delete({"id": str(guild.id)})

    with open("files/mutes.json", "r") as f:
        mute_role = json.load(f)

        mute_role.pop(str(guild.id))
    with open("files/mutes.json", "w") as f:
        json.dump(mute_role, f, indent=4)

    with open("files/shop.json", "r") as z:
        shop = json.load(z)
    shop.pop(str(guild.id))

    with open("files/shop.json", "w") as f:
        json.dump(shop, f, indent=4)

### SLASH COMMANDS ###

@client.tree.command(name="hello", description="saluda")
async def hello( interaction= discord.Interaction):
    await interaction.response.send_message("Hello World!")

### COMMANDS ###

@client.command()
async def prefix(ctx):
    try:
        server_prefix= Server(**server_schema(db_client.local.servers.find_one({"id": str(ctx.guild.id)})))
        return ctx.send(server_prefix.prefix)
    except Exception as error:
        print(error)


@client.command()
async def ping(ctx):
    try:
        bot_latency = round(client.latency * 1000)
        await ctx.author.send(f"{bot_latency} ms")
    except Exception as error:
        print(error)

@client.command()
async def server_id( ctx):
    await ctx.author.send(ctx.guild.id)



@client.command()
async def set_prefix(ctx, *, newprefix: str):

    server_change = dict(Server(id=str(ctx.guild.id), prefix=newprefix))
    db_client.local.servers.find_one_and_replace({"id": str(ctx.guild.id)}, server_change)

    prefix_embed = discord.Embed(title="Succes!", description="you changed the prefix of this bot.", color=discord.Color.blurple())
    prefix_embed.add_field(name="the prefix now is:", value=newprefix)

    await ctx.send(embed= prefix_embed)

            
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with client:
        await load()
        await client.start(consts.DISC_BOT_KEY)

asyncio.run(main())


