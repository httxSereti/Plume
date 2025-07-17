from utils import *
from bot import Bot

import nextcord
import datetime

from nextcord.ext.commands import Cog
from nextcord.ext import commands

class OnMessageDelete(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener("on_message_delete")
    async def on_message_delete(
        self, 
        before: nextcord.Message
    ):
        if before.author == self.bot.user:
            return
        
        if before.author.id in self.bot.trackedUserIds:
            embed: nextcord.Embed = nextcord.Embed(
                title="A message has been deleted.",
                description="<@{}> deleted a message.".format(
                    before.author.id,
                ),
                color=nextcord.Color.purple(),
                timestamp=datetime.datetime.now()
            )
            
            embed.add_field(
                name="Deleted message:",
                value="||```{}```||".format(before.content)
            )
            
            embed.set_author(
                name=before.author.display_name,
                icon_url=before.author.avatar._url,
            )
            
            embed.set_thumbnail(before.author.avatar._url)
            embed.set_footer(text="@plune.app")
            
            await self.bot.get_channel(self.bot.logChannelId).send(embed=embed)

def setup(bot: Bot):
    bot.add_cog(OnMessageDelete(bot))
