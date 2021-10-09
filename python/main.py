import os
import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from dotenv import load_dotenv
import youtube_dl 

load_dotenv()

queues = {}

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='-', intents=intents)

#-----------------------------------------------------------------------------

def check_queue(ctx, id):
    if queues[id] != []:
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)
        voice.play(source) 

def is_connected(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    

@client.command()
async def ping(ctx):
    await ctx.send("pong")

#-----------------------------------------------------------------------------

@client.command(pass_context = True)
async def p(ctx, url:str):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        if is_connected(ctx) != True:
            voice = await channel.connect()
        else:
            voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

        ydl_opts = {
          'format':'bestaudio/best',
          'postprocessors':[{
            'key':'FFmpegExtractAudio',
            'preferredcodec':'mp3',
            'preferredquality':'192',
          }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
          ydl.download([url])
        for file in os.listdir("./"):
          if file.endswith(".mp3"):
            os.rename(file, 'song.mp3')

        source = FFmpegPCMAudio('song.mp3')
        player = voice.play(source, after=lambda x=None: check_queue(ctx, ctx.message.guild.id))
        
    else:
        await ctx.send('You have to be in a voice channel to do that!')



@client.command(pass_context = True)
async def leave(ctx):
    if ctx.guild.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Goodbye")
    else:
        await ctx.send("I'm not in a voice channel!")
        
@client.command(pass_context = True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing:
        voice.pause()
    else:
        await ctx.senfd('There is nothing to pause. Play some music by using: -p link')

@client.command(pass_context = True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.senfd('There is nothing to resume. Play some music by using: -p link')

@client.command(pass_context = True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()
    
@client.command(pass_context = True)
async def q(ctx, url:str):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    ydl_opts = {
      'format':'bestaudio/best',
      'postprocessors':[{
        'key':'FFmpegExtractAudio',
        'preferredcodec':'mp3',
        'preferredquality':'192',
      }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download([url])
    for file in os.listdir("./"):
      if file.endswith(".mp3"):
        os.rename(file, 'song.mp3')

    source = FFmpegPCMAudio('song.mp3')   
    guild_id = ctx.message.guild.id
    if guild_id in queues:
        queues [guild_id].append(source)
    else:
        queues[guild_id] = [source]
        
    await ctx.send("Added to the queue.")

#-----------------------------------------------------------------------------
    
client.run(os.getenv('discord_bot_token'))