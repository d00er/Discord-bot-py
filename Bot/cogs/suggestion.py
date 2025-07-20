import discord 
from discord.ext import commands
import google.generativeai as genai
from decouple import config


genai.configure(api_key=config("API_KEY"))
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

    @commands.cooldown(1, 86400)
    @commands.command()
    async def suggest(self, ctx, *, petition):
        try:
            await ctx.send("💡Por favor espera, esto podria tardar un rato...")

            code = model.generate_content(f"Make the code for this idea of acommand for a discord bot:{petition}. Only answer with the code, nothing else. You also dont have to   make the part of the code to function the discord bot, only the command with his async func in a cog. The code has to be made in python. If you need to save data of any type (like levels, money in the economy of the bot, etc) use a database. In this proyect I am using a database of mongodb. In the code is name as db_client.local. It also has 2 sub files called users and servers. Please try to use these and if you need to make other subfile tell me in the code. Each server in servers has this set of variables: id=str(guild.id), prefix=default_prefix, mute_role=None, level_channel=None, shop = dict, channelW= None,messageW= None, autoroleW= None,imageurlW= None channelG= None, messageG= None, autoroleG= None, imageurlG= None. And each user in users has this set of variables: id:  $oid: 675399bf4df1a688dc262571, id: 444684784178954247, level: 4, experience: 460,balance: 100,deposite: 0,objects: dict")
            

            discord_command = model.generate_content(f"Ahora haz un mensaje interpretando este código para un comando de Discord: {code}, haz un mensaje como lo que sucedería si fueras un bot de Discord y recibieras este comando. Simplemente escriba solo la interpretación de este código.  Simplemente espere los mensajes que ocurrirían si el comando se ejecutara exitosamente con su propósito original, no hable de errores en espera o datos no encontrados en espera. Puede utilizar embeds si es necesario.  Por favor, no escriba: -Nada más que no esté relacionado con el comando, no escriba el código, no traduzca nada, no opine sobre el comando, no hable sobre el código y no explique el comando.")

            discord_explanation = model.generate_content(f"Ahora escriba un mensaje explicando este código para un comando de Discord: {code}, escriba un mensaje explicando qué pasaría si este comando se usara en un bot o servidor de Discord. Simplemente escriba solo la explicación de este código. Puede utilizar embeds si es necesario. Por favor aclarar correctamente los grados de configuración y personalización que tiene y necesita este comando. Por favor, no escriba: nada más que no esté relacionado con el comando, no escriba el código, no traduzca nada, no opine sobre el comando, no hable sobre el código, no hable sobre mongodb. Habla de las cosas necesarias. Si no tiene ninguna configuración no hables de ello. Pero si es así, aclara qué puedes configurar y personalizar. Intenta explicarlo entre 1 y 30 palabras.")

            my_embed = discord.Embed(title="NEW COMMAND SUGGESTED", color = discord.Color.green())
            my_embed.add_field(name="USER: ", value=ctx.author.name, inline = False)
            my_embed.add_field(name="PROMPT: ", value=petition, inline =False)

            user = await self.client.fetch_user(config("CREATOR_USER_ID"))
            await user.send(embed = my_embed)
            await user.send(code.text)
            await ctx.send(discord_command.text)
            await ctx.send(discord_explanation.text)
            conf_embed = discord.Embed(title="Nuevo comando para hacerse", color = discord.Color.green())  # New command to be made
            conf_embed.add_field(name="Gracias!", value=f"La idea del comando a sido enviada a los creadores del bot! Enhorabuena!", inline = False)

            await ctx.send(embed = conf_embed)
        
        except Exception as error: 
                print(error)


    @commands.cooldown(1, 86400)
    @commands.command()
    async def check_suggestion(self, ctx, *, petition):
        try:
            #await ctx.send("💡Please wait, these could take a couple of minutes...")

            answer = model.generate_content(f"Esta petición: {petition} es una solicitud de comando para un bot de discord. Verifique si ya se ha utilizado una petición o un comando similar a este en esta lista de comandos en mi bot de discord: set_prefix, server_id, ping,(lvl commands) lvl, level_channel, (music commands) play, skip, queue, erase, remove, disconnect,  (goodbye  and weolcome commands) goodbye,channel, message, imageUrl,  (mod commands)kick, ban, unban, setmuterole, mute, unmute (fun commands) 8ball, meme, (economy commands) balance, beg, work, steal, deposite, withdraw, shop, buy, addObject, deleteObject, objects,(help commands) help economy, help moderation, help fun, help welcome, help goodbye, help levels, help music, help other. Estos son sólo los nombres de los comandos. Si un comando tiene algún tipo de similitud, aclárelo, y si tiene alguna similitud, tenga mas cuenta que ya podria estar siendo utilizado en el bot. Intenta explicarlo entre 1 y 20 palabras.")

            await ctx.send(answer.text)
        
        except Exception as error: 
                print(error)

    @commands.cooldown(1, 86400)
    @commands.command()
    async def report_bug(self, ctx, *, petition):
        try:
            #await ctx.send("💡Please wait, these could take a couple of minutes...")
            info_embed = discord.Embed(title="BUG REPORTADO!", description=f"El bug ha sido reportado", color=discord.Color.red())
            info_embed.add_field(name="BUG:", value=f"{petition}")
            
            user = await self.client.fetch_user(config("CREATOR_USER_ID"))
            await user.send(embed = info_embed)

            succes_embed = discord.Embed(title="BUG REPORTADO!", description=f"Un bug ha sido reportado", color=discord.Color.green())
            succes_embed.add_field(name="GRACIAS!", value=f"Gracias por reportar el bug, gracias a ti podemos hacer un mejor bot :)")
            await ctx.send(embed = succes_embed)
        except Exception as error: 
                print(error)
    
    @commands.cooldown(1, 86400)
    @commands.command()
    async def report_idea(self, ctx, *, petition):
        try:
            #await ctx.send("💡Please wait, these could take a couple of minutes...")
            info_embed = discord.Embed(title="IDEA PARA TI!", description=f"UNA IDEITAAAAAAAAAAA", color=discord.Color.yellow())
            info_embed.add_field(name="BUG:", value=f"{petition}")
            
            user = await self.client.fetch_user(config("CREATOR_USER_ID"))
            await user.send(embed = info_embed)

            succes_embed = discord.Embed(title="TU IDEA HA SIDO MANDADA!", description=f"que bien ", color=discord.Color.green())
            succes_embed.add_field(name="GRACIAS!", value=f"Gracias por reporta darnos una idea, gracias a ti podemos hacer un mejor bot :)")
            await ctx.send(embed = succes_embed)
        except Exception as error: 
                print(error)


async def setup(client):
    await client.add_cog(suggestion(client))

  # Ajusta el nombre del archivo del modelo descargado
