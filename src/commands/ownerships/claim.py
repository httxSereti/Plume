from bot import Bot

import nextcord

from nextcord import slash_command, SlashOption, Member
from nextcord.ext.commands import Cog
from nextcord.ext import menus

from pprint import pprint

class ClaimConfirmView(nextcord.ui.View):
    def __init__(self, subjectId: int):
        super().__init__()
        self.value = None
        self.subjectId = subjectId

    @nextcord.ui.button(label="Accept", style=nextcord.ButtonStyle.green)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user.id is self.subjectId:
            await interaction.response.send_message("You're now owned! :sparkles:", ephemeral=True)
            self.value = True
            self.stop()

    @nextcord.ui.button(label="Decline", style=nextcord.ButtonStyle.grey)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user.id is self.subjectId: 
            await interaction.response.send_message("You have declined this request!", ephemeral=True)
            self.value = False
            self.stop()

class ClaimCommand(Cog, name="Claim", description="Commands to claim someone"):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.description = "Claim commands"

    @slash_command(
        name="claim",
        description="Claim someone as yours.",
    )
    async def claim(
        self,
        interaction: nextcord.Interaction,
        member: Member = SlashOption(name="user", description="The user you want to claim.", required=True)  
    ):
        claimRequestsResponse = None
        
        # Defer response to fetch data
        await interaction.response.defer(ephemeral=True)
        
        try:
            claimRequestsResponse = (
                self.bot.supabase.table("ownershipss")
                .select("subjectId, active", count="exact")
                .eq("ownerId", interaction.user.id)
                .eq("subjectId", member.id)
                .execute()
            )
        except Exception:
            await interaction.followup.send(f"Fetching error! Report this.")
            return
        
        if (claimRequestsResponse.count > 0):
            await interaction.followup.send(f"You have already claimed <@{member.id}>!")
            return
        
        await interaction.followup.send(f"Requesting <@{member.id}> to be yours!", ephemeral=True, delete_after=5)
        
        view = ClaimConfirmView(member.id)
        
        content = f"## <@{member.id}> would you accept to be owned by <@{interaction.user.id}>?\n"
        content += f"-# :sparkles: warning: accepting this will allow {interaction.user.display_name} to have a lot of power over you, restrict you, restrict how you talk, punish you and everything this bot allow.\n"
        
        ownershipAskMessage = await interaction.channel.send(content=content, view=view)
        await view.wait()
        
        if view.value is None:
            await ownershipAskMessage.edit(content=f"## <@{interaction.user.id}> request to claim <@{member.id}> has expired.", view=None)
        elif view.value:
            response = (
                self.bot.supabase.table("ownerships")
                    .insert({
                        "ownerId": interaction.user.id,
                        "subjectId": member.id,
                        "active": True
                    })
                    .execute()
            )
            
            await ownershipAskMessage.edit(content=f"### <@{member.id}> is now owned by <@{interaction.user.id}>!", view=None)
        else:
            await ownershipAskMessage.edit(content=f"## <@{interaction.user.id}> request to claim <@{member.id}> has been declined.", view=None)

def setup(bot: Bot):
    bot.add_cog(ClaimCommand(bot))