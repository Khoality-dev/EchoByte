from discord_api_key import DISCORD_API_KEY
import asyncio
import discord
from discord.ext import commands
from urllib.parse import urlparse

import re
import yt_dlp

# Create an instance of the bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

is_playing = False
list_songs = []


def is_url(string):
    # Regular expression pattern to match URLs
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    # Match the string against the URL pattern
    return bool(re.match(url_pattern, string))

def get_song_titles(list_songs):
    message = ""
    for song in list_songs:
        message += song[0] + "\n"

    if (message == ""):
        message = "No song in the list"

    return message

def handle_music_done(voice_client, e):
    if (len(list_songs) == 0):
        return
    
    list_songs.pop(0)

    handle_play_music(voice_client)

def handle_play_music(voice_client):
    if (len(list_songs) == 0):
        return
    
    title, url = list_songs[0]

    # fix suddenly stop playing https://stackoverflow.com/questions/75493436/why-is-the-ffmpeg-process-in-discordpy-terminating-without-playing-anything
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.25"'}
    audio_source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
    voice_client.play(audio_source, after=lambda e: handle_music_done(voice_client, e))

def get_platform(raw_url):
    parsed_url = urlparse(raw_url)
    domain = parsed_url.netloc
    if domain.startswith("www."):
        domain = domain[4:]
    parts = domain.split('.')
    if len(parts) >= 2:
        main_domain = parts[-2]
        return main_domain
    else:
        return domain

def get_music_url(str_input):
    isUrl = is_url(str_input)
    
    if (isUrl):
        platform = get_platform(str_input)
    else:
        platform = 'youtube'

    if (platform.lower() == "youtube" or platform.lower() == "soundcloud"):
        # Use youtube_dl to extract the audio stream
        ydl_opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if (isUrl):
                info = ydl.extract_info(str_input, download=False)
            else:
                info = ydl.extract_info(f'ytsearch:{str_input}', download=False)

                if 'entries' in info:
                    # Select the first search result
                    info = info['entries'][0]

            url = info['url']
            title = info['title']
            return title, url

    return title, url

async def set_presense():
    while True:
        if (len(list_songs) == 0):
            title = "Idle!"
        else:
            title, _ = list_songs[0]

        await bot.change_presence(activity=discord.Game(name=title))

        await asyncio.sleep(10)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

    bot.loop.create_task(set_presense())
    

# Function to play music
@bot.command()
async def play(ctx, *, raw_url):
    voice_channel = ctx.author.voice.channel
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if not voice_client is None: #test if voice is None
        if not voice_client.is_connected():
            await voice_channel.connect()
    else:
        await voice_channel.connect()
    
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    
    title, url = get_music_url(raw_url)

    list_songs.append((title, url))

    message = get_song_titles(list_songs)
    await ctx.send(message)

    if not(voice_client.is_playing()):
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

@bot.command()
async def list(ctx):
    message = get_song_titles(list_songs)
    await ctx.send(message)

@bot.command()
async def stop(ctx):
    
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if not voice_client is None: #test if voice is None
        if not voice_client.is_connected():
            return
    else:
        return
    
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    voice_client.stop()

    voice_client.disconnect()

# Run the bot
bot.run(DISCORD_API_KEY)