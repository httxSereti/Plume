
import asyncio
import nextcord
import os


from nextcord import Interaction, slash_command, SlashOption, Member
from nextcord.ext.commands import Cog

from bot import Bot

from pprint import pprint

# import torch
# from TTS.api import TTS

# device = "cuda" if torch.cuda.is_available() else "cpu"


class PlayCommand(Cog):

    # tts_models/en/ljspeech/glow-tts
    
    def __init__(self, bot: Bot):
        self.bot = bot
        # self.tts = TTS("tts_models/en/ljspeech/glow-tts").to(device)
        
        self.playing = False

    @slash_command(
        name="play",
        description="Play a song",
    )
    async def play(
        self,
        interaction: Interaction,
        text: str,
        channel: nextcord.channel.VoiceChannel = SlashOption(name="channel", description="The channel you want to use", required=True)  
    ):
        await interaction.send(f"<@{interaction.user.id}> connecting to <#{channel.id}>.")
        
        # self.tts.tts_to_file(text=text, file_path="gen.wav")
        
        try:
            
            source = await nextcord.FFmpegOpusAudio.from_probe("resources/3.mp3", method='fallback')
            voiceClient = await channel.connect()
            print('Repeating...')
            # pprint(source)
            
            if not self.playing:
                self.playing = True
                voiceClient.play(source)
            
            while self.playing:
                await asyncio.sleep(1)
                
                if voiceClient.is_playing() is False:
                    print('playing...')
                    voiceClient.stop()
                    source = await nextcord.FFmpegOpusAudio.from_probe("resources/3.mp3", method='fallback')
                    voiceClient.play(source)
                    print('played...')
                
        except Exception as err:
            print(err)
        
        
        # voiceClient.play(nextcord.FFmpegPCMAudio("resources/love.mp3"))
    @slash_command(
        name="stop",
        description="Stop a song",
    )
    async def stop(
        self,
        interaction: Interaction
    ):
        self.playing = False
        
        await interaction.send(f"Stopping...")

def setup(bot: Bot):
    bot.add_cog(PlayCommand(bot))