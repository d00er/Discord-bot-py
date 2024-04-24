
import discord
from discord.ext import commands, tasks
from itertools import cycle
import consts
#python utils
import os, asyncio, json

def get_server_prefixes(client, message):
    with open("files/prefixes.json", "r") as j:
        prefix = json.load(j)

    return prefix[str(message.guild.id)]

client = commands.Bot(command_prefix=get_server_prefixes, intents=discord.Intents.all())
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
    with open("files/prefixes.json", "r") as j:
        prefix = json.load(j)

    prefix[str(guild.id)] = "!"

    with open("files/prefixes.json", "w") as f:
        json.dump(prefix, f, indent=4)

    with open("files/mutes.json", "r") as f:
        mute_role = json.load(f)
        mute_role[str(guild.id)] = None

    with open("files/mutes.json", "w") as f:
        json.dump(mute_role, f, indent=3)
    



@client.event
async def on_guild_remove(guild):
    with open("files/prefixes.json", "r") as j:
        prefix = json.load(j)

    prefix.pop(str(guild.id))

    with open("files/prefixes.json", "w") as f:
        json.dump(prefix, f, indent=4)

    with open("files/mutes.json", "r") as f:
        mute_role = json.load(f)

        mute_role.pop(str(guild.id))
    with open("files/mutes.json", "w") as f:
        json.dump(mute_role, f, indent=4)

### SLASH COMMANDS ###

@client.tree.command(name="hello", description="saluda")
async def hello( interaction= discord.Interaction):
    await interaction.response.send_message("Hello World!")

### COMMANDS ###

@client.command()
async def prefix(ctx):
    try:
        with open("files/prefixes.json", "r") as f:
            prefixes=json.load(f)
            
        await ctx.send(prefixes[str(ctx.guild.id)])
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
    with open("files/prefixes.json", "r") as j:
        prefix = json.load(j)

    prefix[str(ctx.guild.id)] = newprefix

    with open("files/prefixes.json", "w") as f:
        json.dump(prefix, f, indent=4)

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


