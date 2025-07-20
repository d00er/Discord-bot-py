
import discord 
from discord.ext import commands
import random, re

from data_base.client import db_client
from data_base.model.user import User
from data_base.model.server import Server
from data_base.schemas.server import user_schema, server_schema

class economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is ready")

    @commands.command(aliases=["bal"])
    async def balance(self, ctx, member: discord.Member= None):
        try:
            if member == None:
                member = ctx.author
            user = User(**user_schema(db_client.local.users.find_one({"id" : str(member.id)})))
        

            list_images= ["https://media1.tenor.com/m/BU3g2AF5_VwAAAAC/money.gif","https://media1.tenor.com/m/turvWZXEE5EAAAAC/heul-breaking-bad.gif"]

            eco_embed = discord.Embed(title=f"cantidad de monedas de:{member.name}", description="Cantidad de Dcoins de este usuario", color=discord.Color.green())
            eco_embed.add_field(name="Dcoins:", value=f"${user.balance}.")
            inti = random.randint(0, 1)
            eco_embed.set_image(url=list_images[inti])
            eco_embed.set_footer(text="Quieres tener mas? Intenta teniendo usando los comandos de economia! (help economy)", icon_url= None)

            await ctx.send(embed=eco_embed)
        except Exception as error:
            print(error)
            error_embed = discord.Embed(title="BOT ERROR", description=" :(", color=discord.Color.red())
            error_embed.add_field(name="ERROR:", value=f"{error}", inline= False)
            await ctx.send(embed=error_embed)

    @commands.command()
    async def beg(self, ctx, member:discord.Member=None):
        try:
            if member == None:
                member = ctx.author
            user = User(**user_schema(db_client.local.users.find_one({"id" : str(member.id)})))
        except Exception as error:
            error_embed = discord.Embed(title="BOT ERROR", description=" :(", color=discord.Color.red())
            error_embed.add_field(name="ERROR:", value="la base de datos no encontro miembros", inline= False)
            
            await ctx.send(embed=error_embed)

        current_balance = user.balance
        amount = random.randint(-10, 30)
        new_balance = current_balance + amount
        user.balance = new_balance

        if current_balance > new_balance:
            list_images= ["https://media1.tenor.com/m/xyRoHP0ZpbkAAAAC/robbery.gif","https://media1.tenor.com/m/H8Z4VTfZwdsAAAAC/%D0%BE%D1%82%D0%B4%D0%B0%D0%B9.gif"]
            eco_embed = discord.Embed(title="Oh No! - Te robaron!", description="Un grupo de ladrones se aprovecho de tu situacion vulnerable", color=discord.Color.red())
            eco_embed.add_field(name="Nueva cantidad de Dcoins:", value=f"${new_balance}.", inline= False)
            eco_embed.set_footer(text="Deberias pedir en una zona mas segura", icon_url= None)
            inti = random.randint(0, 1)
            eco_embed.set_image(url=list_images[inti])
            await ctx.send(embed=eco_embed)


        elif current_balance < new_balance:
            list_images= ["https://media1.tenor.com/m/pg68op-nERsAAAAC/begging-hamster-hamster.gif","https://media.tenor.com/x7QG3N0bdXcAAAAi/taffy-taffy-coin.gif"]
            eco_embed = discord.Embed(title="Exito!", description="Algunas almas amables te dieron lo que tenian!", color=discord.Color.green())
            eco_embed.add_field(name="Nueva cantidad de Dcoins:", value=f"${new_balance}.", inline= False)
            eco_embed.set_footer(text="Prueba de nuevo!", icon_url= None)
            inti = random.randint(0, 1)
            eco_embed.set_image(url=list_images[inti])
            await ctx.send(embed=eco_embed)


        elif current_balance == new_balance:
            list_images= ["https://media1.tenor.com/m/pg68op-nERsAAAAC/begging-hamster-hamster.gif"]
            eco_embed = discord.Embed(title="awh", description="Pedir no te dio nada hoy", color=discord.Color.dark_grey())
            eco_embed.add_field(name="Cantidad Dcoins", value=f"${new_balance}.", inline= False)
            eco_embed.set_footer(text="Intentalo de nuevo", icon_url= None)
            inti = 0
            eco_embed.set_image(url=list_images[inti])
            await ctx.send(embed=eco_embed)

        db_client.local.users.find_one_and_replace({"id" : str(member.id)}, dict(user))


    @commands.cooldown(1, 3600)
    @commands.command() 
    async def work(self, ctx, member:discord.Member = None):
        try:
            if member == None:
                member = ctx.author
            user = User(**user_schema(db_client.local.users.find_one({"id" : str(member.id)})))
        except Exception as error:
            error_embed = discord.Embed(title="BOT ERROR", description=" :(", color=discord.Color.red())
            error_embed.add_field(name="ERROR:", value="the data base didnt find the member", inline= False)
            await ctx.send(embed=error_embed)

        amount=random.randint(100, 300)

        eco_embed = discord.Embed(title="Phew!", description="Despues de trabajar esto es lo que has ganado!", color=discord.Color.green())
        eco_embed.add_field(name="Ganancias:", value=f"${amount}.", inline= False)
        list_images= ["https://tenor.com/es/view/coin-gif-22689269","https://media.tenor.com/x7QG3N0bdXcAAAAi/taffy-taffy-coin.gif"]
        new_balance = user.balance + amount
        user.balance = new_balance

        eco_embed.add_field(name="Nueva cantidad de Dcoins:", value=f"${new_balance}.", inline= False)
        inti = random.randint(0, 1)
        eco_embed.set_image(url=list_images[inti])
        db_client.local.users.find_one_and_replace({"id" : str(member.id)}, dict(user))

        await ctx.send(embed=eco_embed)

    @commands.command()
    async def steal(self, ctx, member:discord.Member):
        try:

            if member == ctx.author:
                await ctx.send("Eu no te podes autorobar, sos tonto?")
            elif db_client.local.users.find_one({"id" : str(member.id)}) == None:
                await ctx.send("este usuario todavia no ha usado los comandos de economia, intenta robarle a otro")
            else:
                robbed = User(**user_schema(db_client.local.users.find_one({"id" : str(member.id)})))
                robber = User(**user_schema(db_client.local.users.find_one({"id" : str(ctx.author.id)})))
                prob_of_robbed = random .randint(0,1)

                if prob_of_robbed == 1:
                    amount_robbed = random.randint(15, 30)

                    robbed.balance -= amount_robbed
                    robber.balance += amount_robbed

                    steal_embed = discord.Embed(title="Criminal!", description=f"Lograste robarle a: {member.mention}", color=discord.Color.green())
                    steal_embed.add_field(name="Ganaste:", value=f"${amount_robbed}")

                    list_images= ["https://media1.tenor.com/m/_jHMKINZLOUAAAAd/steal-this-is-mine.gif","https://media1.tenor.com/m/-J4j3SV7Z90AAAAC/seipalnft-seiopalnft.gif"]
                    inti = random.randint(0, 1)
                    steal_embed.set_image(url=list_images[inti])

                    db_client.local.users.find_one_and_replace({"id" : str(member.id)}, dict(robbed))
                    db_client.local.users.find_one_and_replace({"id" : str(ctx.author.id)}, dict(robber))



                    await ctx.send(embed = steal_embed)

                elif prob_of_robbed == 0:
                    amount_lost = random.randint(10, 20)

                    loser = User(**user_schema(db_client.local.users.find_one({"id" : str(ctx.author.id)})))
                    
                    loser.balance += amount_lost

                    cant_steal_embed = discord.Embed(title="Gran error!", description="Te encontaron robando y tuviste que pagar una fianza", color=discord.Color.red())
                    cant_steal_embed.add_field(name="Perdiste:", value=f"${amount_lost}")

                    list_images= ["https://media1.tenor.com/m/f35hXAov0iEAAAAC/event.gif","https://media.tenor.com/reEdvp-sAwcAAAAi/xoxoxo.gif"]
                    inti = random.randint(0, 1)
                    cant_steal_embed.set_image(url=list_images[inti])

                    db_client.local.users.find_one_and_replace({"id" : str(ctx.author.id)}, dict(loser))

                    await ctx.send(embed = cant_steal_embed)

        except Exception as error:
            print(error)

    @commands.command()
    async def deposite(self, ctx, amount):
        try:
            limit= 250
            amount = int(amount)
            
            user = User(**user_schema(db_client.local.users.find_one({"id" : str(ctx.author.id)})))

            if amount <= 0:
                withdrawl_embed = discord.Embed(title="Wtf pero que te pasa?", description=f"No se puede hacer eso", color=discord.Color.red())
                withdrawl_embed.add_field(name="Lo que tienes guardado es:", value=user.deposite)
                await ctx.send(embed = withdrawl_embed)
            elif amount<=limit:
                user.deposite += amount
                user.balance -= amount

                withdrawl_embed = discord.Embed(title="Exito!", description=f"Lo has guardado", color=discord.Color.green())
                withdrawl_embed.add_field(name="Guardaste:", value=amount)
                withdrawl_embed.add_field(name="Lo que tienes guardado es:", value=user.deposite)
                list_images= ["https://media1.tenor.com/m/zX8RqBTRCGsAAAAd/kajhit-cat.gif","https://media1.tenor.com/m/L_oCpiP4RDUAAAAC/dep%C3%B3sito-confirmado.gif"]
                inti = random.randint(0, 1)
                withdrawl_embed.set_image(url=list_images[inti])
                await ctx.send(embed = withdrawl_embed)

                db_client.local.users.find_one_and_replace({"id" : str(ctx.author.id)}, dict(user))
            else:
                await ctx.send(f"Ese monto es demasiado, podrias poner uno que sea menor a ${limit}")
        except Exception as error:
            error_embed = discord.Embed(title="BOT ERROR", description=" :(", color=discord.Color.red())
            error_embed.add_field(name="ERROR:", value=f"{error}", inline= False)
            await ctx.send(embed=error_embed)

    @commands.command()
    async def withdraw(self, ctx, amount: int):
        try:
            user = User(**user_schema(db_client.local.users.find_one({"id" : str(ctx.author.id)})))

            if amount <= 0 or amount > user.deposite:
                withdrawl_embed = discord.Embed(title="Wtf sos tonto?", description=f"No podes hacer eso", color=discord.Color.red())
                withdrawl_embed.add_field(name="Lo que tienes en el banco es:", value=user.deposite)
                await ctx.send(embed = withdrawl_embed)
            else:
                user.deposite -= amount
                user.balance += amount

                withdrawl_embed = discord.Embed(title="Exito!", description=f"Retiraste Dcoins", color=discord.Color.green())
                withdrawl_embed.add_field(name="Retiraste:", value=amount)
                withdrawl_embed.add_field(name="Lo que tienes guardado es:", value=user.deposite)
                list_images= ["https://media1.tenor.com/m/zX8RqBTRCGsAAAAd/kajhit-cat.gif","https://media1.tenor.com/m/L_oCpiP4RDUAAAAC/dep%C3%B3sito-confirmado.gif"]
                inti = random.randint(0, 1)
                withdrawl_embed.set_image(url=list_images[inti])

                await ctx.send(embed = withdrawl_embed)

                db_client.local.users.find_one_and_replace({"id" : str(ctx.author.id)}, dict(user))
        except Exception as error:
            error_embed = discord.Embed(title="BOT ERROR", description=" :(", color=discord.Color.red())
            error_embed.add_field(name="ERROR:", value=f"{error}", inline= False)
            await ctx.send(embed=error_embed)
    
    #SCRAPPED BY NOW
    """
    @commands.command()
    async def invest(self, ctx, amount):
        with open("eco.json", "r") as f:
            data = json.load(f)
        
        if str(ctx.author.id) not in data:

            data[str(ctx.author.id)] = {}
            data[str(ctx.author.id)]["Balance"] = 100
        
        if data[str(ctx.author.id)]["Deposit"] == None or data[str(ctx.author.id)]["Deposit"] == 0:
            await ctx.send("You dont have any money to invest, try using other commands before this one")
        
    """
    @commands.command()
    async def shop(self, ctx): 
        try:
            error = False
            server = Server(**server_schema(db_client.local.servers.find_one({"id" : str(ctx.guild.id)})))
            
            shop_embed= discord.Embed(title="La tienda", description="Compra cosas con Dcoins", color=discord.Color.yellow())
            
            for i in server.shop:
                shop_embed.add_field(name=f"{server.shop[str(i)]["name"]}", value={server.shop[str(i)]["price"]}, inline=False)
            if len(server.shop)== 0:
                error_embed = discord.Embed(title="La tienda", description="esta vacia", color=discord.Color.red())
                error_embed.add_field(name=f"añade objetos a la tienda", value="con el comando addobject!", inline=False)
                error = True
                await ctx.send(embed = error_embed)
            shop_embed.set_image(url="https://media.tenor.com/v5agR82UYfAAAAAi/raf-rafs.gif")
            if error == False:
                await ctx.send(embed = shop_embed)
        except Exception as error:
            error_embed = discord.Embed(title="BOT ERROR", description=" :(", color=discord.Color.red())
            error_embed.add_field(name="ERROR:", value=f"{error}", inline= False)
            await ctx.send(embed=error_embed)


    @commands.command()
    async def buy(self, ctx, *, item:str):
        
            server = Server(**server_schema(db_client.local.servers.find_one({"id" : str(ctx.guild.id)})))
            

            for i in server.shop:
                try:
                    if server.shop[str(i)]["name"] == item:

                        user = User(**user_schema(db_client.local.users.find_one({"id" : str(ctx.author.id)})))

                        if int(server.shop[str(i)]["price"]) < user.balance:

                            user.balance -= server.shop[str(i)]["price"]
                            
                            if server.shop[str(i)]["name"] in user.objects:
                                user.objects[server.shop[str(i)]["name"]] += 1
                            else:
                                user.objects[server.shop[str(i)]["name"]] = 1

                            buy_embed= discord.Embed(title="Bien!", description="compraste algo", color=discord.Color.teal())
                            buy_embed.add_field(name="Tu compraste:", value=item)
                            list_images= ["https://media1.tenor.com/m/394BkxcRStgAAAAd/buy-buy-now.gif","https://media1.tenor.com/m/P0YuaFVi_dMAAAAC/want-futurama.gif"]
                            inti = random.randint(0, 1)
                            buy_embed.set_image(url=list_images[inti])

                            await ctx.send(embed = buy_embed)
                            db_client.local.users.find_one_and_replace({"id" : str(ctx.author.id)}, dict(user))
                        else: 
                            await ctx.send("no puedes comprar eso, no tienes las Dcoins suficientes")
                        
                except Exception as error:
                        print(error)

            
    @commands.command()
    async def objects(self, ctx):
        user = User(**user_schema(db_client.local.users.find_one({"id" : str(ctx.author.id)})))

        await ctx.send(user.objects)

    @commands.has_permissions(administrator=True)
    @commands.command(aliases=["Aobject","addobj","Aobj"])
    async def addObject(self, ctx, *, item:str):
        try:
            server = Server(**server_schema(db_client.local.servers.find_one({"id" : str(ctx.guild.id)})))

            cant_items = 0

            for i in server.shop:
                cant_items = i

            cant_items = int(cant_items)
            cant_items+=1
            server.shop[str(cant_items)] = {}

            items = re.split("/", item, re.I)

            server.shop[str(cant_items)]["name"] = items[0]
            server.shop[str(cant_items)]["price"] = int(items[1])

            db_client.local.servers.find_one_and_replace({"id" : str(ctx.guild.id)}, dict(server))

            embed_ = discord.Embed(title="Exito!", description=f"Añadiste un item a la tienda", color=discord.Color.green())
            embed_.add_field(name="Nombre del item:", value=items[0])
            embed_.add_field(name="Valor en Dcoins:", value=items[1])

            await ctx.send(embed = embed_)

        except Exception as error:
            print(error)
    
    @commands.has_permissions(administrator=True)
    @commands.command(aliases=["Dobject","delobj","deleteobject","Dobj"])
    async def deleteObject(self, ctx, *, item:str):
        try:
            server = Server(**server_schema(db_client.local.servers.find_one({"id" : str(ctx.guild.id)})))
            
            for i in server.shop:
                if server.shop[str(i)]["name"] == item:
                    server.shop.pop(str(i))
                    break

            db_client.local.servers.find_one_and_replace({"id" : str(ctx.guild.id)}, dict(server))

            embed_ = discord.Embed(title="Exito!", description=f"Eliminaste un objeto de la tienda", color=discord.Color.red())
            embed_.add_field(name="Nombre del item:", value=item)

            await ctx.send(embed = embed_)
        
        except Exception as error:
            print(error)
"""
    @commands.command(name="rich") ###
    async def rich_people(self, ctx):
        server_data = self.db["servers"].find_one({"id": str(ctx.guild.id)})
        if server_data is None:
            await ctx.send("This server isn't configured for this command.")
            return

        users_collection = self.db["users"]
        users = users_collection.find({})
        rich_users = sorted(users, key=lambda user: user.get('balance', 0), reverse=True)

        embed = discord.Embed(title="Richest People in the Server", color=discord.Color.gold())
        embed.set_thumbnail(url=ctx.guild.icon.url)

        if not rich_users:
            embed.description = "No users found in the database."
        else:
            description = ""
            for i, user in enumerate(rich_users):
                member = ctx.guild.get_member(user["id"])
                if member:
                    description += f"{i+1}. {member.display_name}: {user['balance']} coins\n"
            embed.description = description


        await ctx.send(embed=embed)
"""


async def setup(client):
    await client.add_cog(economy(client))