import nextcord

async def buildMissingPermissionEmbed(
    userId: str,
    permission: str,
) -> nextcord.Embed:
    embed: nextcord.Embed = nextcord.Embed(
        title="**Permission Error**",
        description="You don't have the permission to perform this action!",
        color=nextcord.Color.red()
    )
    
    embed.add_field(
        name="User:",
        value=f"<@{userId}>",
        inline=True
    )
    
    embed.add_field(
        name="Permission:",
        value=f"```{permission}```",
        inline=True
    )
    
    return embed
