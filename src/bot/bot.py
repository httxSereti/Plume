import logging
import os
import nextcord

from supabase import create_client, Client
from datetime import datetime
from nextcord import Embed, ApplicationInvokeError, Forbidden, Interaction, DiscordServerError, Color, Intents
from nextcord.ext.commands import Bot as NextcordBot

from configuration import *
from utils import *

class Bot(NextcordBot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            default_guild_ids=GUILD_IDS,
            intents=Intents.all(),
            help_command=None
        )
        
        self.initialised = False
        self.logger = Logger("bot", "logs/bot.log", print_level=logging.DEBUG)
        self.loaded_cogs: dict[str, int] = {} # {cog path: last modified time}
        
        self.trackedUserIds: list(int) = [SUBJECT_ID]
        self.logChannelId: int = LOG_CHANNEL_ID
        
        # Supabase
        self.supabase: Client = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY")
        )
        
    # # Prevents errors from being printed twice
    # async def on_application_command_error(self, interaction: Interaction, error: ApplicationInvokeError):
    #     print(error)
    #     pass

    async def handle_interaction_error(self, interaction: Interaction, exception: Exception):
        if isinstance(exception, Forbidden):
            embed = Embed(title="**Permission Error**", description="I don't have the necessary permissions to perform this action", color=Color.red())
            await interaction.send(embed=embed, ephemeral=True)
            
        else:
            self.logger.error("An unexpected error occured")
            self.logger.error(interaction.user, f"({interaction.user.id})")
            self.logger.exception(exception)
            
            embed = Embed(title="An unexpected error occured", color=Color.red(), timestamp=datetime.now())
            await interaction.send(embed=embed, ephemeral=True)
            
    async def handle_task_error(self, exception: Exception, task: str):
        if not isinstance(exception, DiscordServerError):
            self.logger.error(f"An unexpected error occured in task `{task}`")
            self.logger.exception(exception)

    
    
    
    