import discord 
from discord.ext import commands
import consts
import google.generativeai as genai

genai.configure(api_key=consts.API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

class suggestion(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is ready")

    @commands.command()
    async def chat_return(self, ctx, *, petition):
        try:
            response = model.generate_content(petition)
            await ctx.send(response.text)
        except Exception as error: 
                print(error)

    @commands.cooldown(1, 7200)
    @commands.command()
    async def suggestion(self, ctx, *, petition):
        try:
            await ctx.send("💡Please wait, these could take a couple of minutes...")

            code = model.generate_content(f"Make the code for this idea of acommand for a discord bot:{petition}. Only answer with the code, nothing else. You also dont have to   make the part of the code to function the discord bot, only the command with his async func in a cog. The code has to be made in python. If you need to save data of any type (like levels, money in the economy of the bot, etc) use a database. In this proyect I am using a database of mongodb. In the code is name as db_client.local. It also has 2 sub files called users and servers. Please try to use these and if you need to make other subfile tell me in the code. Each server in servers has this set of variables: id=str(guild.id), prefix=default_prefix, mute_role=None, level_channel=None, shop = dict, channelW= None,messageW= None, autoroleW= None,imageurlW= None channelG= None, messageG= None, autoroleG= None, imageurlG= None. And each user in users has this set of variables: id:  $oid: 675399bf4df1a688dc262571, id: 444684784178954247, level: 4, experience: 460,balance: 100,deposite: 0,objects: dict")
            

            discord_command = model.generate_content(f"Now make a message interpreting this code for a discord command: {code}, make a message like what would happen if you were a discord bot and you receive this command. Just write only the interpretation of this code. You can use embeds if you need to.  Please dont write:-Anything else none related to the comand, Dont write the code, Dont  translate anything, dont take an opinion on the command, dont talk about the code and dont explain the comand. Just await the messages that the code says that will be awaited")

            discord_explanation = model.generate_content(f"Now make a message explaining this code for a discord command: {code}, make a message explaining what would happen if this command was used in a discord bot or server. Just write only the explanation of this code. You can use embeds if you need to. Please clarify correctly the grades of configuration and personalization that this command has and needs. Please dont write:-Anything else none related to the comand, Dont write the code, Dont  translate anything, dont take an opinion on the command, dont talk about the code. Talk about the necesary things. You dont have to clarify the MongoDB database and the configuration if it doesnt have any. But if it has, clarify what you can configure and personalize. Try to explain it 1-30 words")

            my_embed = discord.Embed(title="NEW COMMAND SUGGESTED", color = discord.Color.green())
            my_embed.add_field(name="USER: ", value=ctx.author.name, inline = False)
            my_embed.add_field(name="PROMPT: ", value=petition, inline =False)

            user = await self.client.fetch_user(consts.CREATOR_USER_ID)
            await user.send(embed = my_embed)
            await user.send(code.text)
            await ctx.send(discord_command.text)
            await ctx.send(discord_explanation.text)
            conf_embed = discord.Embed(title="New command to be made", color = discord.Color.green())
            conf_embed.add_field(name="SUCCES", value=f"La idea del comando a sido enviada a los creadores del bot! Enhorabuena!", inline = False)

            await ctx.send(embed = conf_embed)
        
        except Exception as error: 
                print(error)

    @commands.command()
    async def check_suggestion(self, ctx, *, petition):
        try:
            #await ctx.send("💡Please wait, these could take a couple of minutes...")

            answer = model.generate_content(f"This petition: {petition} is a prompt for a command for a discord bot. Please verify if it has already been used a petition or a command similar like that in this list of commands in my discord bot: set_prefix, server_id, ping,(lvl commands) lvl, level_channel, (music commands) play, skip, queue, erase, remove, disconnect,  (goodbye  and weolcome commands) goodbye,channel, message, imageUrl,  (mod commands)kick, ban, unban, setmuterole, mute, unmute (fun commands) 8ball, meme, (economy commands) balance, beg, work, steal, deposite, withdraw, shop, buy, addObject, deleteObject, objects,(help commands) help economy, help moderation, help fun, help welcome, help goodbye, help levels, help music, help other. These are just the name of the commands. If a command has any kind of similarity, clarify it, and if it has a similarity, please keen on the side of that it has already been used in the bot. Try to explain it 1-20 words")

            await ctx.send(answer.text)
        
        except Exception as error: 
                print(error)
    
    @commands.command()
    async def find_user(self,ctx):
        try:
            user_id = 858323215357050901
            user = await self.client.fetch_user(user_id)
            await user.send("¿hola?")
        except Exception as error:
            await ctx.send(f"No se pudo enviar el mensaje {error}")



async def setup(client):
    await client.add_cog(suggestion(client))

  # Ajusta el nombre del archivo del modelo descargado
