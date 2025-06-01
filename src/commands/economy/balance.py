from bot import Bot

import nextcord

from nextcord import slash_command, SlashOption, Member
from nextcord.ext.commands import Cog

class BalanceCommand(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(
        name="balance",
        description="Check the balance of someone.",
    )
    async def balance(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(name="user", description="The user you want to check balance.", required=False)  
    ):
        if member is None:
            member = interaction.user
            
        balances = (
            self.bot.supabase.table("balances")
            .select("amount")
            .eq("userId", member.id)
            .execute()
        )

        if (len(balances.data) == 0):
            await interaction.send(f"<@{member.id}> doesn't have a balance!")
            return

        await interaction.send(f"<@{member.id}> balance is: `{balances.data[0]['amount']}`.")

def setup(bot: Bot):
    bot.add_cog(BalanceCommand(bot))