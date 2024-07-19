
import discord 
from discord.ext import commands
import random, json, requests, re

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

            eco_embed = discord.Embed(title=f"{member.name}'s Current Balance", description="Current balance of this user", color=discord.Color.green())
            eco_embed.add_field(name="Current balance:", value=f"${user.balance}.")
            inti = random.randint(0, 1)
            eco_embed.set_image(url=list_images[inti])
            eco_embed.set_footer(text="Want to increase balance? Try running some economy based commands!", icon_url= None)

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
            error_embed.add_field(name="ERROR:", value="the data base didnt find the member", inline= False)
            
            await ctx.send(embed=error_embed)

        current_balance = user.balance
        amount = random.randint(-10, 30)
        new_balance = current_balance + amount
        user.balance = new_balance

        if current_balance > new_balance:
            list_images= ["https://media1.tenor.com/m/xyRoHP0ZpbkAAAAC/robbery.gif","https://media1.tenor.com/m/H8Z4VTfZwdsAAAAC/%D0%BE%D1%82%D0%B4%D0%B0%D0%B9.gif"]
            eco_embed = discord.Embed(title="Oh No! - Youve been robbed!", description="A group of robbers saw an opportunity on taking advantage of you", color=discord.Color.red())
            eco_embed.add_field(name="New balance:", value=f"${new_balance}.", inline= False)
            eco_embed.set_footer(text="Should probably beg in a nicer part of the town", icon_url= None)
            inti = random.randint(0, 1)
            eco_embed.set_image(url=list_images[inti])
            await ctx.send(embed=eco_embed)


        elif current_balance < new_balance:
            list_images= ["https://media1.tenor.com/m/pg68op-nERsAAAAC/begging-hamster-hamster.gif","https://media.tenor.com/x7QG3N0bdXcAAAAi/taffy-taffy-coin.gif"]
            eco_embed = discord.Embed(title="Succes!", description="Some kind souls out there have given you what they could", color=discord.Color.green())
            eco_embed.add_field(name="New balance:", value=f"${new_balance}.", inline= False)
            eco_embed.set_footer(text="Want more? Wait 1 hour to run this command again, or try some others!", icon_url= None)
            inti = random.randint(0, 1)
            eco_embed.set_image(url=list_images[inti])
            await ctx.send(embed=eco_embed)


        elif current_balance == new_balance:
            list_images= ["https://media1.tenor.com/m/pg68op-nERsAAAAC/begging-hamster-hamster.gif"]
            eco_embed = discord.Embed(title="awh", description="Begging didnt get you anywhere today", color=discord.Color.dark_grey())
            eco_embed.add_field(name="New balance:", value=f"${new_balance}.", inline= False)
            eco_embed.set_footer(text="Want more? Wait 1 hour to run this command again, or try some others", icon_url= None)
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

        eco_embed = discord.Embed(title="Phew!", description="After a hard day of worj this is what you have earned!", color=discord.Color.green())
        eco_embed.add_field(name="Earnings", value=f"${amount}.", inline= False)
        list_images= ["https://tenor.com/es/view/coin-gif-22689269","https://media.tenor.com/x7QG3N0bdXcAAAAi/taffy-taffy-coin.gif"]
        new_balance = user.balance + amount
        user.balance = new_balance

        eco_embed.add_field(name="New balance:", value=f"${new_balance}.", inline= False)
        inti = random.randint(0, 1)
        eco_embed.set_image(url=list_images[inti])
        db_client.local.users.find_one_and_replace({"id" : str(member.id)}, dict(user))

        await ctx.send(embed=eco_embed)

    @commands.command() 
    async def chambear(self, ctx, member:discord.Member = None):
        try:
            if member == None:
                member = ctx.author
            user = User(**user_schema(db_client.local.users.find_one({"id" : str(member.id)})))
        except Exception as error:
            error_embed = discord.Embed(title="BOT ERROR", description=" :(", color=discord.Color.red())
            error_embed.add_field(name="ERROR:", value="the data base didnt find the member", inline= False)
            await ctx.send(embed=error_embed)

        amount=random.randint(100, 300)

        eco_embed = discord.Embed(title="Phew!", description="After a hard day of worj this is what you have earned!", color=discord.Color.green())
        eco_embed.add_field(name="Earnings", value=f"${amount}.", inline= False)
        
        new_balance = user.balance + amount
        user.balance = new_balance

        eco_embed.add_field(name="New balance:", value=f"${new_balance}.", inline= False)
        list_images= ["https://tenor.com/es/view/coin-gif-22689269","hhttps://media.tenor.com/x7QG3N0bdXcAAAAi/taffy-taffy-coin.gif"]
        inti = random.randint(0, 1)
        eco_embed.set_image(url=list_images[inti])
        db_client.local.users.find_one_and_replace({"id" : str(member.id)}, dict(user))

        await ctx.send(embed=eco_embed)


    @commands.command()
    async def steal(self, ctx, member:discord.Member):
        try:

            if member == ctx.author:
                await ctx.send("Bro you cant steal yourself")
            elif db_client.local.users.find_one({"id" : str(member.id)}) == None:
                await ctx.send("this member has not used the economy commands yet, try stealing someone else next time")
            else:
                robbed = User(**user_schema(db_client.local.users.find_one({"id" : str(member.id)})))
                robber = User(**user_schema(db_client.local.users.find_one({"id" : str(ctx.author.id)})))
                prob_of_robbed = random .randint(0,1)

                if prob_of_robbed == 1:
                    amount_robbed = random.randint(15, 30)

                    robbed.balance -= amount_robbed
                    robber.balance += amount_robbed

                    steal_embed = discord.Embed(title="You criminal!", description=f"You have succesfully stealed money from: {member.mention}", color=discord.Color.green())
                    steal_embed.add_field(name="You gained:", value=f"${amount_robbed}")

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

                    cant_steal_embed = discord.Embed(title="Big mistake!", description="You got caught while robing and now you have to pay a fee", color=discord.Color.red())
                    cant_steal_embed.add_field(name="You lost:", value=f"${amount_lost}")

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
                withdrawl_embed = discord.Embed(title="Wtf you dumb?", description=f"You cant do that", color=discord.Color.red())
                withdrawl_embed.add_field(name="Your bank balance is:", value=user.deposite)
                await ctx.send(embed = withdrawl_embed)
            elif amount<=limit:
                user.deposite += amount
                user.balance -= amount

                withdrawl_embed = discord.Embed(title="Succes!", description=f"You have withdrawed", color=discord.Color.green())
                withdrawl_embed.add_field(name="You have withrawed:", value=amount)
                withdrawl_embed.add_field(name="Your bank balance is:", value=user.deposite)
                list_images= ["https://media1.tenor.com/m/zX8RqBTRCGsAAAAd/kajhit-cat.gif","https://media1.tenor.com/m/L_oCpiP4RDUAAAAC/dep%C3%B3sito-confirmado.gif"]
                inti = random.randint(0, 1)
                withdrawl_embed.set_image(url=list_images[inti])
                await ctx.send(embed = withdrawl_embed)

                db_client.local.users.find_one_and_replace({"id" : str(ctx.author.id)}, dict(user))
            else:
                await ctx.send(f"This amount is to big, could you please insert one that is less than ${limit}")
        except Exception as error:
            error_embed = discord.Embed(title="BOT ERROR", description=" :(", color=discord.Color.red())
            error_embed.add_field(name="ERROR:", value=f"{error}", inline= False)
            await ctx.send(embed=error_embed)

    @commands.command()
    async def withdraw(self, ctx, amount: int):
        try:
            user = User(**user_schema(db_client.local.users.find_one({"id" : str(ctx.author.id)})))

            if amount <= 0 or amount > user.deposite:
                withdrawl_embed = discord.Embed(title="Wtf you dumb?", description=f"You cant do that", color=discord.Color.red())
                withdrawl_embed.add_field(name="Your bank balance is:", value=user.deposite)
                await ctx.send(embed = withdrawl_embed)
            else:
                user.deposite -= amount
                user.balance += amount

                withdrawl_embed = discord.Embed(title="Succes!", description=f"You have withdrawed", color=discord.Color.green())
                withdrawl_embed.add_field(name="You have withrawed:", value=amount)
                withdrawl_embed.add_field(name="Your bank balance is:", value=user.deposite)
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
            server = Server(**server_schema(db_client.local.servers.find_one({"id" : str(ctx.guild.id)})))
            
            shop_embed= discord.Embed(title="The shop", description="Buy things with your balance", color=discord.Color.yellow())
            
            for i in server.shop:
                shop_embed.add_field(name=f"{server.shop[str(i)]["name"]}", value={server.shop[str(i)]["price"]}, inline=False)

            shop_embed.set_image(url="https://media.tenor.com/v5agR82UYfAAAAAi/raf-rafs.gif")
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

                            buy_embed= discord.Embed(title="Succes!", description="you buyed something", color=discord.Color.teal())
                            buy_embed.add_field(name="You buyed:", value=item)
                            list_images= ["https://media1.tenor.com/m/394BkxcRStgAAAAd/buy-buy-now.gif","https://media1.tenor.com/m/P0YuaFVi_dMAAAAC/want-futurama.gif"]
                            inti = random.randint(0, 1)
                            buy_embed.set_image(url=list_images[inti])

                            await ctx.send(embed = buy_embed)
                            db_client.local.users.find_one_and_replace({"id" : str(ctx.author.id)}, dict(user))
                        else: 
                            await ctx.send("you cant buy that, insuficient money")
                        
                except Exception as error:
                        print(error)

            
    @commands.command()
    async def objects(self, ctx):
        user = User(**user_schema(db_client.local.users.find_one({"id" : str(ctx.author.id)})))

        await ctx.send(user.objects)
    
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

            embed_ = discord.Embed(title="Succes!", description=f"You have added the item to the shop", color=discord.Color.green())
            embed_.add_field(name="Object name:", value=items[0])
            embed_.add_field(name="Object value:", value=items[1])

            await ctx.send(embed = embed_)

        except Exception as error:
            print(error)
    
    @commands.command(aliases=["Dobject","delobj","deleteobject","Dobj"])
    async def deleteObject(self, ctx, *, item:str):
        try:
            server = Server(**server_schema(db_client.local.servers.find_one({"id" : str(ctx.guild.id)})))
            
            for i in server.shop:
                if server.shop[str(i)]["name"] == item:
                    server.shop.pop(str(i))
                    break

            db_client.local.servers.find_one_and_replace({"id" : str(ctx.guild.id)}, dict(server))

            embed_ = discord.Embed(title="Succes!", description=f"You have deleted the item to the shop", color=discord.Color.red())
            embed_.add_field(name="Object name:", value=item)

            await ctx.send(embed = embed_)
        
        except Exception as error:
            print(error)


async def setup(client):
    await client.add_cog(economy(client))