import discord
from discord.ext import commands

SOCIALS_MALE = {
    "Twitter":    "https://twitter.com/FURIA",
    "YouTube":    "https://youtube.com/FURIA",
    "Instagram":  "https://instagram.com/FURIA",
    "Facebook":   "https://facebook.com/FURIA"
}

SOCIALS_FEMALE = {
    "Twitter":    "https://twitter.com/FURIA_Female",
    "YouTube":    "https://youtube.com/FURIA_Female",
    "Instagram":  "https://instagram.com/FURIA_Female",
    "Facebook":   "https://facebook.com/FURIA_Female"
}

class Socials(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="socials")
    async def show_socials(self, ctx, line: str = "male"):
        """
        Exibe botões com links para redes sociais.
        Uso: !socials [male|female]
        """
        line = line.lower()
        if line == "female":
            socials = SOCIALS_FEMALE
            title = "🌟 Redes Sociais da Line Feminina"
        else:
            socials = SOCIALS_MALE
            title = "🔥 Redes Sociais da Line Masculina"

        embed = discord.Embed(title=title, color=0xE03A3E)
        view = discord.ui.View()
        for name, url in socials.items():
            view.add_item(discord.ui.Button(label=name, url=url))

        await ctx.reply(embed=embed, view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(Socials(bot))
