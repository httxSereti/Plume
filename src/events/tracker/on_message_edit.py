from utils import *
from bot import Bot

import nextcord
import datetime

from nextcord.ext.commands import Cog
from nextcord.ext import commands

class OnMessageEdit(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener("on_message_edit")
    async def on_message_edit(
        self,
        before: nextcord.Message,
        after: nextcord.Message
    ):
        if before.content == after.content or before.author == self.bot.user or after.author == self.bot.user:
            return
        
        if before.author.id in self.bot.trackedUserIds:
            embed: nextcord.Embed = nextcord.Embed(
                title="A message has been edited.",
                description="<@{}> edited a message.\n ```{}```".format(
                    after.author.id,
                    after.content
                ),
                color=nextcord.Color.purple(),
                timestamp=datetime.datetime.now()
            )
            
            embed.add_field(
                name="Previous message:",
                value="||```{}```||".format(before.content)
            )
            
            embed.set_author(
                name=after.author.display_name,
                icon_url=after.author.avatar._url,
            )
            
            embed.set_thumbnail(after.author.avatar._url)
            embed.set_footer(text="@plune.app")
            
            await self.bot.get_channel(self.bot.logChannelId).send(embed=embed)

def setup(bot: Bot):
    bot.add_cog(OnMessageEdit(bot))
