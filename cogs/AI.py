import discord 
from discord.ext import commands
import openai, typer
import consts

class AI(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is ready")

    @commands.command()
    async def chatgpt(self, ctx, *, question):
        client = openai.OpenAI(
            api_key = consts.API_KEY_CHATGPT
        )
        Context= {"role": "system", "content": "useful assistant"}
        message=[Context] 

        content=question
    
        message.append({
            "role": "user",
            "content": content,
        })

        response = client.chat.completions.create(
            messages=message,
            model="gpt-3.5-turbo"
        )
        
        response_content = response.choices[0].message.content
        message.append({
                "role": "assistant",
                "content": response_content,
            })
        await ctx.send(response_content) 

async def setup(client):
    await client.add_cog(AI(client))

