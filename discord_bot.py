import discord
import asyncio

import config
import voice
import random

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


class DefVoice:
    def __init__(self):
        self.voice_client: discord.VoiceClient = None
        self.is_playing = False

    async def default_voice_play(self):
        if not self.is_playing:
            source = discord.FFmpegPCMAudio(source=config.white_noice_dir, executable=config.executable_dir)
            self.voice_client.play(source)
            time_sleep = random.randint(45, 75)
            print(time_sleep)
            await asyncio.sleep(time_sleep)
            if not self.is_playing:
                self.voice_client.stop()
                x = random.randint(0, 1)
                default_sound_source = discord.FFmpegPCMAudio(source=config.default_voices_dir[x],
                                                              executable=config.executable_dir)
                self.voice_client.play(default_sound_source)
                await asyncio.sleep(config.default_voices_duration[x])
                self.voice_client.stop()
                await self.default_voice_play()

    async def default_voice_continue(self):
        self.is_playing = False
        if not self.voice_client.is_playing():
            await self.default_voice_play()

    def set_voice_client(self, voice_client: discord.VoiceClient):
        self.voice_client = voice_client


default_voice_client = DefVoice()


@client.event
async def on_message(message):
    global default_voice_client
    if message.author == client.user:
        return
    else:
        print('from ' + str(message.author) + ': ' + str(message.content))
        if message.content.startswith(config.ds_set['prefix'] + 'join'):
            channel = message.author.voice.channel
            await channel.connect()
            await message.reply('connected')
            default_voice_client.set_voice_client(discord.utils.get(client.voice_clients, guild=message.guild))
            await default_voice_client.default_voice_continue()

        elif message.content.startswith(config.ds_set['prefix'] + 'leave'):
            for x in client.voice_clients:
                if x.channel == message.author.voice.channel:
                    await x.disconnect()
                    await message.reply('disconnected')
        elif message.content.startswith(config.ds_set['prefix'] + 'voice'):
            key = voice.extract_key(message.content)
            if voice.is_key_correct(key):
                voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=message.guild)
                default_voice_client.set_voice_client(voice_client)
                if voice_client.is_playing():
                    voice_client.stop()

                default_voice_client.is_playing = True
                dir = voice.get_voice_dir(key)
                audio_source = discord.FFmpegPCMAudio(source=dir, executable=config.executable_dir)
                voice_client.play(source=audio_source)
                await asyncio.sleep(9)
                await default_voice_client.default_voice_continue()
                await message.reply('OK')
            else:
                await message.reply('invalid key')
        elif message.content.startswith(config.ds_set['prefix'] + 'list'):
            await message.reply(voice.get_list())


client.run(config.ds_set['token'])
