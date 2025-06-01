import nextcord


from datetime import datetime
from bot import Bot

from nextcord import Interaction, slash_command, SlashOption, Member
from nextcord.ext.commands import Cog

from pprint import pprint

class RulesCommand(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(
        name="rules",
        description="View Rules of someone.",
    )
    async def rules(
        self,
        interaction: Interaction,
        member: Member = SlashOption(name="user", description="The user you want to see.", required=True)  
    ):
        
        rulesResponse = (
            self.bot.supabase.table("rules")
            .select("*")
            .eq("subjectId", member.id)
            .order("created_at", desc=False)
            .execute()
        )
        
        rulesText = ""
        
        for rule in rulesResponse.data:
            rulesText += "```{}```\n".format(rule.get("content"))
        
        embed: nextcord.Embed = nextcord.Embed(
            title=":sparkles: Rules",
            description=f"{rulesText}"
        )
        
        embed.set_footer(text="@plune.app - Powered by Lucie")
                
        await interaction.send(f"<@{member.id}>'s rules.", embed=embed)

def setup(bot: Bot):
    bot.add_cog(RulesCommand(bot))