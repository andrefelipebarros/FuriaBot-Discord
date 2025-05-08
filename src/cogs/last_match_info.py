import discord
from discord.ext import commands
from discord.ui import View, button, Button
from services.result_matcher import get_latest_match_info
import asyncio

# Default headers for requests
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; DiscordBot/1.0; +https://github.com/yourrepo)',
    'Referer': 'https://liquipedia.net'
}

async def fetch_latest_match(team_slug: str):
    """
    Executa a função síncrona get_latest_match_info em um executor para não bloquear o loop.
    """
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None,
        get_latest_match_info,
        team_slug,
        DEFAULT_HEADERS
    )

async def handle_latest(interaction: discord.Interaction, female: bool):
    await interaction.response.defer()
    # Define o slug correto para o time
    team_slug = 'FURIA_Female' if female else 'FURIA'

    try:
        info = await fetch_latest_match(team_slug)
    except Exception:
        return await interaction.edit_original_response(
            content="❌ Erro ao buscar último jogo.",
            view=LatestMatchView()
        )

    if not info:
        return await interaction.edit_original_response(
            content="❌ Último jogo não encontrado.",
            view=LatestMatchView()
        )

    # Construção do embed com informações
    embed = discord.Embed(
        title="⚔️ Último Jogo",
        color=0xE03A3E
    )
    embed.add_field(name="Data", value=info.get('Date', '—'), inline=True)
    embed.add_field(name="Evento", value=info.get('Event', '—'), inline=True)
    embed.add_field(name="Adversário", value=info.get('Opponent', '—'), inline=True)
    embed.add_field(name="Placar", value=info.get('Score', '—'), inline=True)
    embed.add_field(name="Resultado", value=info.get('Result', '—'), inline=False)

    await interaction.edit_original_response(embed=embed, view=LatestMatchView())

class LatestMatchView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="Male", style=discord.ButtonStyle.primary, custom_id="latest_match_male")
    async def male_button(self, interaction: discord.Interaction, button: Button):
        await handle_latest(interaction, female=False)

    @button(label="Female", style=discord.ButtonStyle.primary, custom_id="latest_match_female")
    async def female_button(self, interaction: discord.Interaction, button: Button):
        await handle_latest(interaction, female=True)

class LatestMatch(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="last", help="Último jogo da Line de CS:GO!")
    async def last_match(self, ctx: commands.Context):
        """
        Exibe menu para escolher linha e mostrar último jogo.
        Uso: !last
        """
        view = LatestMatchView()
        await ctx.reply("Selecione a linha para ver o último jogo:", view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(LatestMatch(bot))
