# especificar bien comandos

import discord 
from discord.ext import commands
import json

class configs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is ready")
    
    @commands.command()
    async def update(self, ctx): ###
        embed_message = discord.Embed(title="ULTIMA ACTUALIZACION", description="Version actual: 0.5", color=discord.Color.purple()) #ctx.author.color
        embed_message.add_field(name="-CODE REWORK", value="todos los datos estan seguros en una base de datos", inline=False)
        embed_message.add_field(name="-CORRECCION DE ERRORES", value="corregimos todos los errores vistos para poder publicar el bot", inline=False)

        await ctx.send(embed=embed_message)

    @commands.command()
    async def nextupdate(self, ctx): ###
        embed_message = discord.Embed(title="COSAS POSIBLE PARA LA SIGUIENTE ACTUALIZACION", description="Siguiente version: 0.6", color=discord.Color.purple()) #ctx.author.color
        embed_message.add_field(name="-FUNCIONAR COMANDOS ABANDONADOS.", value="Hacer funcionar ideas que quedaron en el tintero, como por ejemplo leaderboards de niveles, warnings, y mas", inline=False)
        embed_message.add_field(name="-FUNCIONAR MUSICA DEL BOT", value="Hacer funcionar musica del bot", inline=False)
        embed_message.add_field(name="-APLICAR IDEAS Y SUGERENCIAS", value="Usar ideas de la comunidad y meterlas al bot", inline=False)

        await ctx.send(embed=embed_message)

    @commands.group(name="help", invoke_without_command = True)
    async def help(self, ctx):
        embed_message = discord.Embed(title="Help", description="tipos de comandos del bot", color=discord.Color.purple()) #ctx.author.color
        embed_message.add_field(name="Este bot tiene:", value="50 comandos para que explores! y 2 secretos", inline=False)
        embed_message.add_field(name="help economy", value="mira los comandos relacionados a la economia", inline=False)
        embed_message.add_field(name="help moderation", value="mira los comandos relacionados a la moderacion", inline=False)
        embed_message.add_field(name="help fun", value="mira los comandos relacionados a los juegos", inline=False)
        embed_message.add_field(name="help welcome", value="mira los comandos relacionados a la bienvenida de un miembro", inline=False)
        embed_message.add_field(name="help goodbye", value="mira los comandos relacionados a la despedida de un miembro", inline=False)
        embed_message.add_field(name="help levels", value="mira los comandos relacionados a niveles y rangos", inline=False)
        #embed_message.add_field(name="help music", value="mira los comandos relacionados a la musica", inline=False)
        embed_message.add_field(name="help suggestion", value="mira los comandos relacionados a las sugerencias para mejorar al bot", inline=False)
        embed_message.add_field(name="help other", value="otros comandos", inline=False)
        embed_message.set_image(url=ctx.guild.icon)

        await ctx.send(embed=embed_message)

    @help.command()
    async def economy(self, ctx):
        embed_message = discord.Embed(title="Comandos de economia", description="Comandos relacionados a la economia del bot, basada en dCoins (moneda ficticia)", color=discord.Color.purple()) #ctx.author.color
        embed_message.add_field(name="balance",  value="ver tu saldo en este servidor, necesitarás aclarar un miembro", inline=False)
        embed_message.add_field(name="beg", value="Suplicar por dCoins. Mientras suplicas tienes una pequeña probabilidad de que te roben.", inline=False)
        embed_message.add_field(name="work", value="Trabaja para ganar dCoins", inline=False)
        embed_message.add_field(name="steal", value="robale a alguien, tienes que aclarar un miembro del server (la policia puede atraparte)", inline=False)
        embed_message.add_field(name="deposite", value="deposita dinero, para que asi no te lo puedan robar, tendras que aclarar un monto", inline=False)
        embed_message.add_field(name="withdraw", value="Retira el dinero que depositaste anteriormente, deberás aclarar un monto.", inline=False)
        embed_message.add_field(name="shop", value="ve la tienda", inline=False)
        embed_message.add_field(name="buy", value="compra objetos de la tienda ficticia, tienes que aclarar el nombre del objeto", inline=False)
        embed_message.add_field(name="addObject (Aobject, addobj, Aobj)", value="añade un nuevo objeto a la tienda, para usarlo tienes que poner [nombre del objeto]/[precio del objeto]", inline=False)
        embed_message.add_field(name="deleteObject (Dobject, delobject, Dobj)", value="elimina un objeto de la tienda, para usarlo pon el nombre del objeto", inline=False)
        embed_message.add_field(name="objects", value="mira tus objetos actuales", inline=False)

        await ctx.send(embed=embed_message)

    @help.command()
    async def moderation(self, ctx):
        embed_message = discord.Embed(title="Comandos de moderacion", description="comandos relacionados a moderar tu server con nuestro bot", color=discord.Color.purple()) 
        embed_message.add_field(name="kick", value="kickea a un miembro", inline=False)
        embed_message.add_field(name="ban", value="banea un miembro", inline=False)
        embed_message.add_field(name="unban", value="desbanea a un miembro", inline=False)
        embed_message.add_field(name="setmuterole (smuterole, setmr, stmr)", value="necesitas especificar el role id", inline=False)
        embed_message.add_field(name="mute", value="mutea a un miembro", inline=False)
        embed_message.add_field(name="unmute", value="desmutea a un miembro", inline=False)

        await ctx.send(embed=embed_message)
    
    @help.command()
    async def fun(self, ctx):
        embed_message = discord.Embed(title="Comandos divertidos", description="comandos relacionados a juegos en el bot", color=discord.Color.purple()) 
        embed_message.add_field(name="8ball (bola8, 8bola)", value="haz una pregunta a la bola ocho", inline=False)
        embed_message.add_field(name="meme", value="recibe un meme random", inline=False)
        embed_message.add_field(name="rps (rock-papel-scissors, rockpaperscissors) / piedra papel y tijera", value="juega al piedra papel o tijera con el bot", inline=False)

        await ctx.send(embed=embed_message)

    @help.command()
    async def welcome(self, ctx):
        embed_message = discord.Embed(title="Comandos de bienvenida", description="comandos relacionados a la bienvenida de un miembro al server", color=discord.Color.purple()) 
        embed_message.add_field(name="welcome", value="el grupo de comandos", inline=False)
        embed_message.add_field(name="autorole", value="el rol que se le dara a los miembros cuando se unen al servidor. Tenes que especificar el id del role", inline=False)
        embed_message.add_field(name="channel", value="el canal donde se pondran los embeds de bienvenida. Tienes que especificar el channel id", inline=False)
        embed_message.add_field(name="message", value="el mensaje en el embed de bienvenida", inline=False)
        embed_message.add_field(name="imageUrl", value="La imagen en el embed de bienvenida", inline=False)
        
        await ctx.send(embed=embed_message)
    
    @help.command()
    async def goodbye(self, ctx):
        embed_message = discord.Embed(title="Comandos de despedida", description="comandos relacionados a la despedida de miembros en el grupo.", color=discord.Color.purple()) 
        embed_message.add_field(name="goodbye", value="el grupo de comandos", inline=False)
        embed_message.add_field(name="channel", value="el canal donde se pondran los embeds de despedida. Tienes que especificar el channel id", inline=False)
        embed_message.add_field(name="message", value="el mensaje en el embed de despedida", inline=False)
        embed_message.add_field(name="imageUrl", value="La imagen en el embed de despedida", inline=False)
        
        await ctx.send(embed=embed_message)
    
    @help.command()
    async def music(self, ctx):
        """
        embed_message = discord.Embed(title="Comandos de musica", description="comandos relacionados a la musica en el bot", color=discord.Color.purple()) 
        embed_message.add_field(name="play", value="pon musica en el bot. add a link of the music you want to hear, si ya estabas escuchando algo, la nueva cancion se añade a la lista", inline=False)
        embed_message.add_field(name="skip", value="skipear la cancion actual", inline=False)
        embed_message.add_field(name="queue", value="mostrar la lista de la musica", inline=False)
        embed_message.add_field(name="erase", value="borrar toda la lista", inline=False)
        embed_message.add_field(name="remove", value="remover la primera cancion de la lista", inline=False)
        embed_message.add_field(name="disconnect", value="desconectar al bot del chat de voz ", inline=False)
        
        await ctx.send(embed=embed_message)
        """
        embed_message = discord.Embed(title="WARNING!", description="UNFINISHED, UNFINISHED I SAY", color=discord.Color.yellow()) 
        embed_message.add_field(name="IF YOU WANT TO MAKE IT HAPPEN...", value="Just keep waiting. We will do our best.", inline=False)
        
        await ctx.send(embed=embed_message)
    @help.command()
    async def levels(self, ctx):
        embed_message = discord.Embed(title="Commandos de nivel", description="Commandos relacionados al nivel de los miembros del servidor", color=discord.Color.purple()) 
        embed_message.add_field(name="level (lvl, r, rank)", value="Mira tu nivel", inline=False)
        embed_message.add_field(name="level_channel (lvlchannel, rankchannel, rChannel)", value="el canal customizable de los niveles, tienes que añadir el id del canal seleccionado.", inline=False)
        
        await ctx.send(embed=embed_message)

    @help.command()
    async def suggestion(self, ctx):
        embed_message = discord.Embed(title="Comandos de sugerencia", description="Comandos relacionados a sugerir cosas para mejorar el bot", color=discord.Color.purple()) 
        embed_message.add_field(name="suggest", value="Sugiere un comando que sera mandado directamente a los creadores del bot.", inline=False)
        embed_message.add_field(name="check_suggestion", value="Verifica si tu comando que quieres sugerir ya esta en el bot", inline=False)
        embed_message.add_field(name="report_bug", value="Reporta un bug del bot al desarrollador", inline=False)
        embed_message.add_field(name="report_idea", value="Reporta una idea al desarrollador", inline=False)
        
        await ctx.send(embed=embed_message)

    @help.command()
    async def other(self, ctx):
        embed_message = discord.Embed(title="Otros comandos", description="Comandos varios que no tienen mucho que ver entre si.", color=discord.Color.purple()) 
        embed_message.add_field(name="prefix", value="setea el prefijo del bot con el comando: set_prefix", inline=False)
        embed_message.add_field(name="server id", value="ve el id del servidor con el comando: server_id", inline=False)
        embed_message.add_field(name="ping", value="Actual ping del bot", inline=False)
        embed_message.add_field(name="update", value="Mira lo que se hizo en la ultima actualizacion del bot", inline=False)
        embed_message.add_field(name="nextupdate", value="Whats coming to the bot", inline=False)
        
        await ctx.send(embed=embed_message)

async def setup(client):
    await client.add_cog(configs(client))


"""
    set_prefix, server_id, ping,(lvl commands) lvl, level_channel, (music commands) play, skip, queue, erase, remove, disconnect,  (goodbye  and weolcome commands) goodbye,channel, message, imageUrl,  (mod commands)kick, ban, unban, setmuterole, mute, unmute (fun commands) 8ball, meme, (economy commands) balance, beg, work, steal, deposite, withdraw, shop, buy, addObject, deleteObject, objects,(help commands) help economy, help moderation, help fun, help welcome, help goodbye, help levels, help music, help other, ask_command, question_command.

"""