import discord

import config
import voice

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(config.ds_set['prefix'] + 'join'):
        channel = message.author.voice.channel
        await channel.connect()
        await message.reply('connected')
    elif message.content.startswith(config.ds_set['prefix'] + 'leave'):
        for x in client.voice_clients:
            if x.channel == message.author.voice.channel:
                await x.disconnect()
                await message.reply('disconnected')
    elif message.content.startswith(config.ds_set['prefix'] + 'voice'):
        key = voice.extract_key(message.content)

        if voice.is_key_correct(key):
            voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=message.guild)
            audio_source = discord.FFmpegPCMAudio(source=voice.get_voice_dir(key), executable='venv/Lib/site-packages/ffmpeg-5.1-full_build/bin/ffmpeg.exe')
            voice_client.play(audio_source)
            await message.reply('OK')
        else:
            await message.reply('invalid key')
    elif message.content.startswith(config.ds_set['prefix'] + 'list'):
        await message.reply(voice.get_list())


client.run(config.ds_set['token'])