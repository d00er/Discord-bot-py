# REPROGRAMAR

from ast import alias
import discord
from discord.ext import commands
from youtubesearchpython import VideosSearch
import yt_dlp 
from youtube_dl import YoutubeDL
import asyncio
class music_cog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

        #all the music related stuff
        self.is_playing = False
        self.is_paused = False

        # 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', "noplaylist": True}
        self.FFMPEG_OPTIONS = {'options': '-vn'}

        self.vc = None
        self.ytdl = YoutubeDL(self.YDL_OPTIONS)

    #searching the item on youtube
    def search_yt(self, item):
        if item.startswith("https://"):
            title = self.ytdl.extract_info(item, download=False)["title"]
            return{'source':item, 'title':title}
        search = VideosSearch(item, limit=1)
        return{'source':search.result()["result"][0]["link"], 'title':search.result()["result"][0]["title"]}

    async def play_next(self, ctx):
        try:
            if self.music_queue:
                url, title = self.music_queue.pop(0)
                source = await discord.FFmpegOpusAudio.from_probe(url, **self.FFMPEG_OPTIONS, executable="c:/Users/Victorino/ffmpeg/ffmpeg.exe")
                ctx.voice_client.play(source, after= lambda _: self.client.loop.create_task(self.play_next(ctx)))
                await ctx.send(f"Now playing **{title}**")
            elif not ctx.voice_client.is_playing():
                await ctx.send("queue is empty!")
        except Exception as error:
            print(error)

    # infinite loop checking 
    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            #try to connect to voice channel if you are not already connected
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                #in case we fail to connect
                if self.vc == None:
                    await ctx.send("```Could not connect to the voice channel```")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])
            #remove the first element as you are currently playing it
            self.music_queue.pop(0)
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(m_url, download=False))
            song = data['url']
            self.vc.play(discord.FFmpegPCMAudio(song, executable= "ffmpeg.exe", **self.FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop))

        else:
            self.is_playing = False

    @commands.command(name="play", aliases=["p","playing"], help="Plays a selected song from youtube")
    async def play(self, ctx, *, search):
        try:
            voice_channel = ctx.author.voice.channel if ctx.author.voice else None
            if not voice_channel:
                await ctx.send("Youre not in a voice channel")
            if not ctx.voice_client:
                await voice_channel.connect()
            async with ctx.typing():
                with yt_dlp.YoutubeDL(self.YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(f"ytsearch:{search}", download = False)
                    if "entries" in info:
                        info = info["entries"][0]
                    url = info["url"]
                    title = info["title"]
                    self.music_queue.append((url, title))
                    await ctx.send(f"Added to queue: **{title}**")
            if not ctx.voice_client.is_playing():
                await self.play_next(ctx)
        except Exception as error:
            print(error)
        

    @commands.command(name="pause", help="Pauses the current song being played")
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()

    @commands.command(name = "resume", help="Resumes playing with the discord bot")
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()

    @commands.command(name="skip", aliases=["s"], help="Skips the current song being played")
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            #try to play next in the queue if it exists
            await ctx.send("Skipped")
            await self.play_next(ctx)



    @commands.command(name="queue", aliases=["q"], help="Displays the current songs in queue")
    async def queue(self, ctx):
        try: # string indices must be integers, not 'str'
            retval = ""
            for i in range(0, len(self.music_queue)):
                retval += f"#{i+1} -" + self.music_queue[i][1] + "\n"

            if retval != "":
                await ctx.send(f"```queue:\n{retval}```")
            else:
                await ctx.send("```No music in queue```")
        except Exception as error:
            print(error)

    @commands.command(name="erases", aliases=["c", "bin"], help="Stops the music and clears the queue")
    async def erases(self, ctx):
        try:
            if self.vc != None and self.is_playing:
                self.vc.stop()
            self.music_queue = []
            await ctx.send("```Music queue cleared```")
        except Exception as error:
            print(error)

    @commands.command(name="stop", aliases=["disconnect", "l", "d"], help="Kick the bot from VC")
    async def dc(self, ctx):
        try:
            if (ctx.voice_client):
                await ctx.guild.voice_client.disconnect()
        except Exception as error:
            print(error)
    
    @commands.command(name="remove", help="Removes last song added to queue")
    async def re(self, ctx):
        try:
            self.music_queue.pop()
            await ctx.send("```last song removed```")
        except Exception as error:
            print(error)

    @commands.command(name="pause", help="Pauses the current song being played")
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()

    @commands.command(name = "resume", help="Resumes playing with the discord bot")
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()


async def setup(client):
    await client.add_cog(music_cog(client))
