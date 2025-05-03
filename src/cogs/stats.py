import discord
from discord.ext import commands
import requests
from services.last_scoreboard import get_furia_scoreboard, build_bo3_url

TEAM_SLUG = "FURIA"

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="stats")
    async def stats(self, ctx, line: str = "male"):
        """
        Mostra Top fragger e scoreboard da última partida da Fúria !
        Uso: !stats [male|female]
        """
        headers = {
            'User-Agent': 'FuriaResultsBot/1.0',
            'Referer': f'https://liquipedia.net/counterstrike/{TEAM_SLUG}'
        }

        slug = "FURIA_Female" if line.lower() == "female" else "FURIA"
        url = build_bo3_url(slug, headers)

        if not url:
            return await ctx.reply("❌ Não foi possível gerar a URL.")

        try:
            board = get_furia_scoreboard(url)
        except requests.exceptions.ReadTimeout:
            return await ctx.reply("⚠️ Timeout ao buscar dados. Tente novamente mais tarde.")
        except Exception as e:
            return await ctx.reply(f"❌ Erro ao obter estatísticas: {e}")

        if not board:
            return await ctx.reply("❌ Não encontrei o placar dos jogadores.")

        mvp_nick, _ = next(iter(board.items()))

        table = "```"
        table += f"{'Jogador':<12}{'K':>5}{'D':>5}{'A':>5}{'Score':>8}\n"
        table += "-" * 35 + "\n"
        for nick, stats in board.items():
            table += f"{nick:<12}{stats['Kills']:>5}{stats['Deaths']:>5}{stats['Assists']:>5}{stats['Score']:>8}\n"
        table += "```"

        description = (
            f"🏆 **MVP – {mvp_nick}** 🏆\n\n"
            f"📋 **Scoreboard:**\n{table}"
        )

        embed = discord.Embed(
            title="🥇 Estatísticas da Última Partida",
            description=description,
            color=0xE03A3E
        )

        await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Stats(bot))
