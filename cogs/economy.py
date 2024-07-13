
import discord 
from discord.ext import commands
import random, json, requests, re

class economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is ready")

    @commands.command(aliases=["bal"])
    async def balance(self, ctx, member: discord.Member=None):
        try:
            with open("files/eco.json") as f:
                user_eco=json.load(f)

            if member is None:
                member = ctx.author
            elif member is not None:
                member=member

            if str(member.id) not in user_eco:

                user_eco[str(member.id)] = {}
                user_eco[str(member.id)]["Balance"] = 100
                user_eco[str(member.id)]["Deposit"] = 0

                with open("files/eco.json", "w") as f:
                    json.dump(user_eco, f, indent=4)
        except Exception as error:
            print(error)

        eco_embed = discord.Embed(title=f"{member.name}'s Current Balance", description="Current balance of this user", color=discord.Color.green())
        eco_embed.add_field(name="Current balance:", value=f"${user_eco[str(member.id)]["Balance"]}.")
        eco_embed.set_footer(text="Want to increase balance? Try running some economy based commands!", icon_url= None)

        await ctx.send(embed=eco_embed)

    @commands.command()
    async def beg(self, ctx, member:discord.Member=None):
        try:
            with open("files/eco.json") as f:
                user_eco=json.load(f)

            if member is None:
                member = ctx.author
            elif member is not None:
                member=member

            if str(ctx.author.id) not in user_eco:

                user_eco[str(ctx.author.id)] = {}
                user_eco[str(ctx.author.id)]["Balance"] = 100
                user_eco[str(ctx.author.id)]["Deposit"] = 0

                with open("files/eco.json", "w") as f:
                    json.dump(user_eco, f, indent=4)
        except Exception as error:
            print(error)

        current_balance = user_eco[str(ctx.author.id)]["Balance"]
        amount = random.randint(-10, 30)
        new_balance = current_balance + amount

        if current_balance > new_balance:
            eco_embed = discord.Embed(title="Oh No! - Youve been robbed!", description="A group of robbers saw an opportunity on taking advantage of you", color=discord.Color.green())
            eco_embed.add_field(name="New balance:", value=f"${new_balance}.", inline= False)
            eco_embed.set_footer(text="Should probably beg in a nicer part of the town", icon_url= None)
            await ctx.send(embed=eco_embed)

            user_eco[str(ctx.author.id)]["Balance"] += amount

            with open("files/eco.json", "w") as f:
                json.dump(user_eco, f, indent=4)

        elif current_balance < new_balance:
            eco_embed = discord.Embed(title="Succes!", description="Some kind souls out there have given you what they could", color=discord.Color.green())
            eco_embed.add_field(name="New balance:", value=f"${new_balance}.", inline= False)
            eco_embed.set_footer(text="Want more? Wait 1 hour to run this command again, or try some others!", icon_url= None)
            await ctx.send(embed=eco_embed)

            user_eco[str(ctx.author.id)]["Balance"] += amount

            with open("files/eco.json", "w") as f:
                json.dump(user_eco, f, indent=4)

        elif current_balance == new_balance:
            eco_embed = discord.Embed(title="awh", description="Begging didnt get you anywhere today", color=discord.Color.green())
            eco_embed.add_field(name="New balance:", value=f"${new_balance}.", inline= False)
            eco_embed.set_footer(text="Want more? Wait 1 hour to run this command again, or try some others", icon_url= None)
            await ctx.send(embed=eco_embed)

            user_eco[str(ctx.author.id)]["Balance"] += amount

            with open("files/eco.json", "w") as f:
                json.dump(user_eco, f, indent=4)

    @commands.command()
    async def work(self, ctx, member:discord.Member = None):
        try:
            with open("files/eco.json") as f:
                user_eco=json.load(f)

            if member is None:
                member = ctx.author
            elif member is not None:
                member=member

            if str(ctx.author.id) not in user_eco:

                user_eco[str(ctx.author.id)] = {}
                user_eco[str(ctx.author.id)]["Balance"] = 100
                user_eco[str(ctx.author.id)]["Deposit"] = 0

                with open("files/eco.json", "w") as f:
                    json.dump(user_eco, f, indent=4)
            amount=random.randint(100, 300)
        except Exception as error:
            print(error)
        

        eco_embed = discord.Embed(title="Phew!", description="After a hard day of worj this is what you have earned!", color=discord.Color.green())
        eco_embed.add_field(name="Earnings", value=f"${amount}.", inline= False)
        new_balance = user_eco[str(ctx.author.id)]["Balance"] + amount
        user_eco[str(ctx.author.id)]["Balance"] = new_balance

        with open("files/eco.json", "w") as f:
            json.dump(user_eco, f, indent=4)

        eco_embed.add_field(name="New balance:", value=f"${new_balance}.", inline= False)
        
        await ctx.send(embed=eco_embed)

    @commands.command()
    async def steal(self, ctx, member:discord.Member):
        try:
            with open("files/eco.json", "r") as f:
                data = json.load(f)
            
            if str(ctx.author.id) not in data:

                data[str(ctx.author.id)] = {}
                data[str(ctx.author.id)]["Balance"] = 100
                data[str(ctx.author.id)]["Deposit"] = 0


            if member == ctx.author:
                await ctx.send("Bro you cant steal yourself")
            elif data[str(member.id)] == None:
                await ctx.send("this member has not used the economy commands yet, try stealing someone else next time")
            else:
                
                prob_of_robbed = random .randint(0,1)

                if prob_of_robbed == 1:
                    amount_robbed = random.randint(15, 30)

                    data[str(member.id)]["Balance"] -= amount_robbed
                    data[str(ctx.author.id)]["Balance"] += amount_robbed

                    steal_embed = discord.Embed(title="You criminal!", description=f"You have succesfully stealed money from: {member.mention}", color=discord.Color.green())
                    steal_embed.add_field(name="You gained:", value=f"${amount_robbed}")

                    with open("files/eco.json", "w") as f:
                        json.dump(data, f, indent=4)
                    
                    await ctx.send(embed = steal_embed)
                elif prob_of_robbed == 0:
                    amount_lost = random.randint(10, 20)
                    
                    data[str(ctx.author.id)]["Balance"] += amount_lost

                    cant_steal_embed = discord.Embed(title="Big mistake!", description="You got caught while robing and now you have to pay a fee", color=discord.Color.red())
                    cant_steal_embed.add_field(name="You lost:", value=f"${amount_lost}")

                    with open("files/eco.json", "w") as f:
                        json.dump(data, f, indent=4)

                await ctx.send(embed = cant_steal_embed)
        except Exception as error:
            print(error)

    @commands.command()
    async def deposite(self, ctx, amount):
        try:
            limit= 250
            amount = int(amount)
            with open("files/eco.json", "r") as f:
                data = json.load(f)
        

            if str(ctx.author.id) not in data:

                data[str(ctx.author.id)] = {}
                data[str(ctx.author.id)]["Balance"] = 100
                data[str(ctx.author.id)]["Deposit"] = 0

            if amount <= 0:
                withdrawl_embed = discord.Embed(title="Wtf you dumb?", description=f"You cant do that", color=discord.Color.red())
                withdrawl_embed.add_field(name="Your bank balance is:", value=data[str(ctx.author.id)]["Deposit"])
                await ctx.send(embed = withdrawl_embed)
            elif amount<=limit:
                data[str(ctx.author.id)]["Deposit"] += amount
                data[str(ctx.author.id)]["Balance"] -= amount

                withdrawl_embed = discord.Embed(title="Succes!", description=f"You have withdrawed", color=discord.Color.green())
                withdrawl_embed.add_field(name="You have withrawed:", value=amount)
                withdrawl_embed.add_field(name="Your bank balance is:", value=data[str(ctx.author.id)]["Deposit"])

                await ctx.send(embed = withdrawl_embed)

                with open("files/eco.json", "w") as f:
                    json.dump(data, f, indent=4)
            
            else:
                await ctx.send(f"This amount is to big, could you please insert one that is less than ${limit}")
        except Exception as error:
            print(error)

    @commands.command()
    async def withdraw(self, ctx, amount: int):
        with open("files/eco.json", "r") as f:
            data = json.load(f)

        if str(ctx.author.id) not in data:

            data[str(ctx.author.id)] = {}
            data[str(ctx.author.id)]["Balance"] = 100
        if amount <= 0 or amount > data[str(ctx.author.id)]["Deposit"]:
            withdrawl_embed = discord.Embed(title="Wtf you dumb?", description=f"You cant do that", color=discord.Color.red())
            withdrawl_embed.add_field(name="Your bank balance is:", value=data[str(ctx.author.id)]["Deposit"])
            await ctx.send(embed = withdrawl_embed)
        else:
            data[str(ctx.author.id)]["Deposit"] -= amount
            data[str(ctx.author.id)]["Balance"] += amount

            withdrawl_embed = discord.Embed(title="Succes!", description=f"You have withdrawed", color=discord.Color.green())
            withdrawl_embed.add_field(name="You have withrawed:", value=amount)
            withdrawl_embed.add_field(name="Your bank balance is:", value=data[str(ctx.author.id)]["Deposit"])

            await ctx.send(embed = withdrawl_embed)

            with open("files/eco.json", "w") as f:
                json.dump(data, f, indent=4)
    
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
            with open("files/shop.json", "r") as f:
                data = json.load(f)
            
            shop_embed= discord.Embed(title="The shop", description="Buy things with your balance", color=discord.Color.yellow())
            
            for i in data[str(ctx.guild.id)]:
                shop_embed.add_field(name=f"{data[str(ctx.guild.id)][str(i)]["name"]}", value={data[str(ctx.guild.id)][str(i)]["price"]}, inline=False)

            await ctx.send(embed = shop_embed)
        except Exception as error:
            print(error)


    @commands.command()
    async def buy(self, ctx, *, item:str):
        
            with open("files/shop.json", "r") as f:
                data = json.load(f)
            

            for i in data[str(ctx.guild.id)]:
                try:
                    if data[str(ctx.guild.id)][i]["name"] == item:
                        with open("files/eco.json", "r") as f:
                            economic = json.load(f)
                
                        if int(data[str(ctx.guild.id)][i]["price"]) < economic[str(ctx.author.id)]["Balance"]:

                            economic[str(ctx.author.id)]["Balance"] -= data[str(ctx.guild.id)][i]["price"]

                            if "Objects" not in economic[str(ctx.author.id)]:
                                economic[str(ctx.author.id)]["Objects"] = {}
                                
                            
                            if data[str(ctx.guild.id)][str(i)]["name"] in economic[str(ctx.author.id)]["Objects"]:
                                economic[str(ctx.author.id)]["Objects"][data[str(ctx.guild.id)][str(i)]["name"]] += 1
                            else:
                                economic[str(ctx.author.id)]["Objects"][data[str(ctx.guild.id)][str(i)]["name"]] = 1

                            buy_embed= discord.Embed(title="Succes!", description="you buyed something", color=discord.Color.teal())
                            buy_embed.add_field(name="You buyed:", value=item)

                            await ctx.send(embed = buy_embed)
                            
                        else: 
                            await ctx.send("you cant buy that, insuficient money")
                        with open("files/eco.json", "w") as f:
                            json.dump(economic, f, indent=4)
                except Exception as error:
                        print(error)

            
    @commands.command()
    async def objects(self, ctx):
        with open("files/eco.json", "r") as f:
            economic = json.load(f)

        await ctx.send(economic[str(ctx.author.id)]["Objects"])
    
    @commands.command()
    async def add_object(self, ctx, *, item:str):
        try:
            with open("files/shop.json", "r") as f:
                economic = json.load(f)
            
            
            for i in economic[str(ctx.guild.id)]:
                cant_items = i
            cant_items = int(cant_items)
            cant_items+=1
            economic[str(ctx.guild.id)][cant_items] = {}
            items = re.split("/", item, re.I)
            economic[str(ctx.guild.id)][cant_items]["name"] = items[0]
            economic[str(ctx.guild.id)][cant_items]["price"] = int(items[1])

            with open("files/shop.json", "w") as f:
                json.dump(economic, f, indent = 4)

            embed_ = discord.Embed(title="Succes!", description=f"You have added the item to the shop", color=discord.Color.green())
            embed_.add_field(name="Object name:", value=items[0])
            embed_.add_field(name="Object value:", value=items[1])

            await ctx.send(embed = embed_)
        
        
        except Exception as error:
            print(error)
    
    @commands.command()
    async def delete_object(self, ctx, *, item:str):
        try:
            with open("files/shop.json", "r") as f:
                economic = json.load(f)
            
            
            for i in economic[str(ctx.guild.id)]:
                if economic[str(ctx.guild.id)][i]["name"] == item:
                    economic[str(ctx.guild.id)].pop(i)
                    break

            with open("files/shop.json", "w") as f:
                json.dump(economic, f, indent = 4)

            embed_ = discord.Embed(title="Succes!", description=f"You have deleted the item to the shop", color=discord.Color.green())
            embed_.add_field(name="Object name:", value=item)

            await ctx.send(embed = embed_)
        
        except Exception as error:
            print(error)





async def setup(client):
    await client.add_cog(economy(client))