import argparse
from discord_api_key import DISCORD_API_KEY
import discord
from discord.ext import commands
import yt_dlp

# Create an instance of the bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Command: Ping
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

# Command: Echo
@bot.command()
async def echo(ctx, *, message):
    await ctx.send(message)

# Command: Join
@bot.command()
async def join(ctx):
    # Check if the command invoker is in a voice channel
    if ctx.author.voice:
        # Connect to the voice channel of the command invoker
        voice_channel = ctx.author.voice.channel
        await voice_channel.connect()
    else:
        await ctx.send("You need to be in a voice channel to use this command.")

# Function to play audio from a YouTube link
@bot.command()
async def play_youtube(ctx, url):
    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
        await ctx.send("You need to be in a voice channel to use this command.")
        return

    voice_client = await voice_channel.connect()

    # Use youtube_dl to extract the audio stream
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        voice_client.play(discord.FFmpegPCMAudio(info['url'] ), after=lambda e: print('done', e))


# Function to play music
@bot.command()
async def play(ctx):
    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
        await ctx.send("You need to be in a voice channel to use this command.")
        return

    voice_client = await voice_channel.connect()
    voice_client.play(discord.FFmpegPCMAudio(path))  


# Run the bot
bot.run(DISCORD_API_KEY)