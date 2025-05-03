import discord
from discord.ext import commands
from discord.ui import View, Button
from services.roster_service import get_current_roster

class PollView(View):
    def __init__(self, options: list[str]):
        super().__init__(timeout=None)

        self.counts: dict[str, int] = {opt: 0 for opt in options}
        self.voters: set[int] = set()

        for opt in options:
            btn = Button(label=f"{opt} (0)", style=discord.ButtonStyle.secondary, custom_id=f"poll_{opt}")
            async def callback(interaction: discord.Interaction, opt=opt, btn=btn):
                user_id = interaction.user.id

                if user_id in self.voters:
                    # informa que já votou
                    await interaction.response.send_message("❌ Você já votou.", ephemeral=True)
                    return
                
                self.voters.add(user_id)
                self.counts[opt] += 1
                btn.label = f"{opt} ({self.counts[opt]})"

                await interaction.response.edit_message(view=self)
                
                await interaction.followup.send(f"Você votou em **{opt}**!", ephemeral=True)
            btn.callback = callback
            self.add_item(btn)

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="poll")
    async def cheer_poll(self, ctx, line: str = "male"):
        """
        Exibe enquete de votação para torcida!
        Uso: !poll [male|female]
        """
        slug = "FURIA_Female" if line.lower() == "female" else "FURIA"
        try:
            options = await get_current_roster(slug)
        except Exception:
            options = ["yuurih", "KSCERATO", "FalleN", "molodoy", "YEKINDAR"]

        if not options or len(options) > 10:
            return await ctx.reply("❌ Número inválido de opções para a enquete.")

        view = PollView(options)
        await ctx.send(
            content="🌟 Quem vai brilhar hoje? Clique no botão para votar!", 
            view=view
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(Poll(bot))
