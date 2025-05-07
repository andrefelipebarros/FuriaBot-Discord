import discord
from discord.ext import commands
from discord.ui import View, button, Button
from services.next_match import fetch_upcoming_matches

# Mapeamento de gênero para team_slug do Draft5
TEAM_SLUGS = {
    "male": "330-FURIA",
    "female": "1200-FURIA-fem",
}

async def handle_next(interaction: discord.Interaction, team_slug: str):
    """Busca e exibe as próximas partidas de uma equipe no Draft5."""
    # Defer para interações já mostra loading no botão
    await interaction.response.defer()

    try:
        upcoming = await fetch_upcoming_matches(team_slug)
    except Exception:
        return await interaction.edit_original_response(
            content="❌ Erro ao buscar próximas partidas.",
            view=MainView()
        )

    if not upcoming:
        return await interaction.edit_original_response(
            content="❌ Nenhuma próxima partida encontrada.",
            view=MainView()
        )

    # Prettify: cada partida em um field separado
    title_map = {"330-FURIA": "FURIA (Male)", "1200-FURIA-fem": "FURIA (Female)"}
    embed = discord.Embed(
        title=f"🔥 Próximas Partidas - {title_map.get(team_slug)}",
        color=0xE03A3E
    )

    # Adiciona campo para cada partida
    for match in upcoming[:5]:
        date_time = f"**{match['date']}** às **{match['time']}**"
        scoreline = f":crossed_swords: **{match['team1']}** `{match['score1']} x {match['score2']}` **{match['team2']}** ({match['best_of']})"
        embed.add_field(
            name=date_time,
            value=f"{scoreline}\n🏆 {match['tournament']}",
            inline=False
        )

    # Link para Draft5
    url = f"https://draft5.gg/equipe/{team_slug}/proximas-partidas"
    embed.add_field(name="🔗 Onde ver", value=f"[Abrir no Draft5]({url})", inline=False)

    await interaction.edit_original_response(embed=embed, view=MatchView(team_slug))

class MainView(View):
    """View inicial com botões para escolher Male ou Female."""
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="Male", style=discord.ButtonStyle.primary, custom_id="next_select_male")
    async def select_male(self, interaction: discord.Interaction, button: Button):
        await handle_next(interaction, TEAM_SLUGS['male'])

    @button(label="Female", style=discord.ButtonStyle.primary, custom_id="next_select_female")
    async def select_female(self, interaction: discord.Interaction, button: Button):
        await handle_next(interaction, TEAM_SLUGS['female'])

class MatchView(View):
    """View após seleção, com botões para atualizar ou voltar."""
    def __init__(self, team_slug: str):
        super().__init__(timeout=None)
        self.team_slug = team_slug

    @button(label="Atualizar", style=discord.ButtonStyle.primary, custom_id="next_refresh")
    async def refresh_button(self, interaction: discord.Interaction, button: Button):
        await handle_next(interaction, self.team_slug)

    @button(label="Trocar Time", style=discord.ButtonStyle.secondary, custom_id="next_back")
    async def back_button(self, interaction: discord.Interaction, button: Button):
        # Volta para seleção inicial
        await interaction.edit_original_response(content="Selecione um time:", embed=None, view=MainView())

class Matches(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="next", help="Mostra as próximas partidas da FURIA CS:GO! Sem args mostra botões, ou use 'male'/'female'.")
    async def next_match(self, ctx, gender: str = None):
        # Indica que o bot está digitando
        async with ctx.typing():
            # Se passou gênero, busca direto
            if gender:
                gender = gender.lower()
                if gender not in TEAM_SLUGS:
                    return await ctx.send("⚠️ Parâmetro inválido. Use `male` ou `female`.")
                team_slug = TEAM_SLUGS[gender]
                upcoming = await fetch_upcoming_matches(team_slug)

                if not upcoming:
                    return await ctx.send("❌ Nenhuma próxima partida encontrada.")

                embed = discord.Embed(
                    title=f"🔥 Próximas Partidas - {title_map.get(team_slug)}",
                    color=0xE03A3E
                )
                for match in upcoming[:5]:
                    date_time = f"**{match['date']}** às **{match['time']}**"
                    scoreline = f":crossed_swords: **{match['team1']}** `{match['score1']} x {match['score2']}` **{match['team2']}** ({match['best_of']})"
                    embed.add_field(name=date_time, value=f"{scoreline}\n🏆 {match['tournament']}", inline=False)
                url = f"https://draft5.gg/equipe/{team_slug}/proximas-partidas"
                embed.add_field(name="🔗 Onde ver", value=f"[Abrir no Draft5]({url})", inline=False)
                await ctx.send(embed=embed, view=MatchView(team_slug))
            else:
                await ctx.send("Selecione um time:", view=MainView())

async def setup(bot: commands.Bot):
    await bot.add_cog(Matches(bot))