import discord
from discord.ext import commands
from discord.ui import View, button, Button
from services.pandascore import fetch_next_match as _svc_fetch_next_match

async def fetch_next_match(female: bool):
    return await _svc_fetch_next_match()

async def handle_next(interaction: discord.Interaction, female: bool):

    await interaction.response.defer()

    try:
        info = await fetch_next_match(female)
    except Exception:
        return await interaction.edit_original_response(
            content="❌ Erro ao buscar próxima partida.",
            view=NextMatchView()
        )

    if not info:
        return await interaction.edit_original_response(
            content="❌ Nenhuma partida encontrada.",
            view=NextMatchView()
        )

    opponent = info.get('opponent', '')
    league = info.get('league', '')
    if opponent.upper() == "PCIFIC" or opponent.lower() == "getting info" or league == "Paramigo Cup":
        return await interaction.edit_original_response(
            content="❌ Nenhuma partida futura marcada.",
            view=NextMatchView()
        )

    embed = discord.Embed(
        title="🔥 Próxima Partida",
        description=(
            f"**Adversário:** {opponent}\n"
            f"**Quando:** {info['date']}\n"
            f"**Liga:** {league}"
        ),
        color=0xE03A3E
    )
    await interaction.edit_original_response(embed=embed, view=NextMatchView())

class NextMatchView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="Male", style=discord.ButtonStyle.primary, custom_id="next_match_male")
    async def male_button(self, interaction: discord.Interaction, button: Button):
        await handle_next(interaction, female=False)

    @button(label="Female", style=discord.ButtonStyle.primary, custom_id="next_match_female")
    async def female_button(self, interaction: discord.Interaction, button: Button):
        await handle_next(interaction, female=True)

class Matches(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="next", help="Próxima partida da Line de CS:GO!")
    async def next_match(self, ctx):
        """
        Exibe menu próxima partida da Line de CS:GO!
        Uso: !next
        """
        view = NextMatchView()
        await ctx.send("Selecione a linha:", view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(Matches(bot))
