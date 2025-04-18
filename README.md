# EchoByte

A simple Discord bot that plays music from YouTube URLs.

## Usage

To use the bot, simply type `!play` followed by a YouTube URL. The bot will download the audio and play it in the voice channel you are in.

To list the songs in the queue, use the `!list` command.

To stop the current song and clear the queue, use the `!stop` command.

## Setup

Place your Discord bot token in a file named `.env` in the root directory of the project and run the following command:

```
docker compose up -d
```