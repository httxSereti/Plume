import nextcord
from nextcord import Interaction, SlashOption, slash_command, user_command, message_command, InteractionType
from nextcord.ext.commands import Cog
from nextcord.ext import commands

from configuration import GUILD_IDS
from utils.embeds import buildMissingPermissionEmbed

from pprint import pprint

class SpeechCommands(Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
        self.bannedWords: dict(int, list(str)) = {}
        
        # self.loadBannedWords()
        
    def loadBannedWords(self):
        self.bannedWords = {}
        
        bannedWordsResponse = (
            self.bot.supabase.table("speech.banned_words")
            .select("*", count="exact")
            .eq("enabled", True)
            .execute()
        )
        
        for item in bannedWordsResponse.data:
            subjectId = item.get("subjectId")
            
            if (subjectId in self.bannedWords):
                self.bannedWords[subjectId].append(item.get('content').lower())
            else:
                self.bannedWords[subjectId] = [item.get('content').lower()]
        
        self.bot.logger.info(f"[Speech] Loaded {bannedWordsResponse.count} banned Words.")

    @slash_command(
        name="speech",
    )
    async def speech(self, interaction: Interaction):
        pass 
    
    @speech.subcommand(
        name="list",
        description="List Words and Sentences forbidden to use of someone or you.",
    )
    async def display(
        self, 
        interaction: Interaction,
        member: nextcord.Member = SlashOption(name="user", description="The User you want ", required=False),
    ):
        if member is None:
            member = interaction.user
            
        bannedWords = (
            self.bot.supabase.table("speech.banned_words")
            .select("*")
            .eq("subjectId", member.id)
            .execute()
        )
        
        pprint(bannedWords)
            
        wordList: str = ""
        
        for word in bannedWords.data:
            wordList += "{} ✿ '{}' | [used {} times...]\n".format(
                '✅' if word.get('enabled') is True else '🟥',
                word.get('content'),
                word.get('trigerred')
            )
            
        embed: nextcord.Embed = nextcord.Embed(
            title=f":sparkles: Words(s)",
            description=f"```{wordList}```",
            color=nextcord.Color.purple()
        )
        
        await interaction.response.send_message(embed=embed)
            
    @speech.subcommand()
    async def word(self, interaction: Interaction):
        pass
        
    @word.subcommand(
        name="ban",
        description="Make a word forbidden to use for someone.",
    )
    async def ban(
        self, 
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(
            name="user",
            description="The User you want ",
            required=True
        ),
        word: str = SlashOption(
            name="word",
            description="Word to ban.",
            required=True
        )
    ): 
        ownership = (
            self.bot.supabase.table("ownerships")
            .select("active", count="exact")
            .eq("ownerId", interaction.user.id)
            .eq("claimedId", member.id)
            .eq("active", True)
            .execute()
        )
        
        if ownership.count != 1:
            await interaction.response.send_message(embed=buildMissingPermissionEmbed(interaction.user.id, "User isn't claimed by you."))
            return 

        bannedWord = (
            self.bot.supabase.table("speech.banned_words")
            .insert({
                "subjectId": member.id,
                "content": word,
            })
            .execute()
        )
            
        embed: nextcord.Embed = nextcord.Embed(
            title=f"Added a new word to the ban list.",
            description="<@{}> added a word to the ban list of <@{}>".format(
                interaction.user.id,
                member.id    
            ),
            color=nextcord.Color.purple()
        )
        
        embed.add_field(
            name="Word:",
            value="||{}||".format(word)
        )
        
        await interaction.response.send_message("Successfully added word to the ban list, reloading banned words...")
        await self.bot.get_channel(self.bot.logChannelId).send(embed=embed)
        
        self.loadBannedWords()
        
    @word.subcommand(
        description="Unban a word from being used.",
    )
    async def unban(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(name="user", description="The User you want to add to Administrators.", required=True),
    ) -> None:
        pass
    
    @word.subcommand(
        description="Toggle a Word from being banned/free to use."
    )
    async def toggle(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(name="user", description="The User you want to remove from Administrators.", required=True),
    ):
        pass
    
    @user_command()
    async def hello(self, interaction: nextcord.Interaction, member: nextcord.Member):
        """Says hi to a user that was right-clicked on"""
        await interaction.response.send_message(f"Hello {member}!")
        
    @message_command(
        name="Report this message",
    )
    async def say(self, interaction: nextcord.Interaction, message: nextcord.Message):
        """Sends the content of the right-clicked message as an ephemeral response"""
        msg = f"'{message.content}'? t'oublie pas des choses stupide chose?"
        await interaction.response.send_message(msg, ephemeral=False)

    @commands.Cog.listener("on_message")
    async def on_message(self, message: nextcord.Message):
        if message.author.id == self.bot.user.id or self.bannedWords is None:
            return
                
        bannedWords = self.bannedWords[message.author.id]

        if bannedWords is None:
            return
        
        for word in bannedWords:
            words: list[str] = message.content.lower().split(' ');
            
            if word in words:
                embed: nextcord.Embed = nextcord.Embed(
                    title=f"Ferme ta gueule.",
                    description="Ce mot t'es interdit pauvre conne.",
                    color=nextcord.Color.red()
                )
                
                embed.add_field(
                    name="Utilisateur:",
                    value=":sparkles: <@{}>".format(message.author.id),
                    inline=True
                )
                
                embed.add_field(
                    name="Mot interdit:",
                    value=":warning: ||{}||".format(word),
                    inline=True
                )
                
                embed.add_field(
                    name="Message:",
                    value=":envelope: ||{}||".format(message.content),
                    inline=False
                )
                
                await message.channel.send(embed=embed)
                await message.delete()      
        
def setup(bot):
    bot.add_cog(SpeechCommands(bot))
    pass