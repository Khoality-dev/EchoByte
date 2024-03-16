from discord_api_key import DISCORD_API_KEY
import discord
from discord.ext import commands
from urllib.parse import urlparse

import yt_dlp

# Create an instance of the bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

is_playing = False
list_urls = []

def handle_music_done(voice_client):
    if (len(list_urls) == 0):
        return
    
    list_urls.pop(0)

    handle_play_music(voice_client)

def handle_play_music(voice_client):
    if (len(list_urls) == 0):
        return
    
    url = list_urls[0]

    voice_client.play(discord.FFmpegPCMAudio(url), after=lambda e: handle_music_done(voice_client))

def get_platform(raw_url):
    parsed_url = urlparse(raw_url)
    domain = parsed_url.netloc
    if domain.startswith("www."):
        domain = domain[4:]  # Remove "www." if present
    parts = domain.split('.')
    if len(parts) >= 2:
        main_domain = parts[-2] # Get the last two parts of the domain
        return main_domain
    else:
        return domain

def get_music_url(raw_url):
    platform = get_platform(raw_url)

    if (platform.lower() == "youtube" or platform.lower() == "soundcloud"):
        # Use youtube_dl to extract the audio stream
        ydl_opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(raw_url, download=False)
            url = info['url']
            return url

    return url

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Function to play music
@bot.command()
async def play(ctx, raw_url):
    voice_channel = ctx.author.voice.channel
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if not voice_client is None: #test if voice is None
        if not voice_client.is_connected():
            await voice_channel.connect()
    else:
        await voice_channel.connect()
    
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    url = get_music_url(raw_url)

    list_urls.append(url)
    if (len(list_urls) == 1):
        handle_play_music(voice_client)
    
@bot.command()
async def skip(ctx):
    
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if not voice_client is None: #test if voice is None
        if not voice_client.is_connected():
            return
    else:
        return
    
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    voice_client.stop()

    handle_music_done(voice_client)

# Run the bot
bot.run(DISCORD_API_KEY)