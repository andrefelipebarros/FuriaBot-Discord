from discord.ext import commands
import discord

class MyHelp(commands.MinimalHelpCommand):
    def __init__(self):
        super().__init__()
        self.paginator.max_size = 2000

    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            await destination.send(page)

class HelpMenu(discord.ui.View):
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=120)
        self.bot = bot
        options = [
            discord.SelectOption(label=cmd.name, description=cmd.help or "—")
            for cmd in bot.commands
        ]
        if not options:
            return

        select = discord.ui.Select(
            placeholder="Escolha um comando…",
            options=options[:25],
            custom_id="help_select"
        )
        select.callback = self.select_callback
        self.add_item(select)

    async def select_callback(self, interaction: discord.Interaction):
        cmd_name = interaction.data['values'][0]
        cmd = self.bot.get_command(cmd_name)
        embed = discord.Embed(
            title=f"!{cmd.name}",
            description=cmd.help or "Sem descrição"
        )
        embed.add_field(name="Uso", value=f"`!{cmd.qualified_name} {cmd.signature}`")
        await interaction.response.edit_message(embed=embed, view=self)

def setup_help(bot: commands.Bot):
    bot.help_command = MyHelp()
    bot.remove_command('help')

    @bot.command(name="help", help="Mostra este menu de ajuda interativo")
    async def help_menu(ctx: commands.Context):
        view = HelpMenu(bot)
        embed = discord.Embed(
            title="Menu de Comandos",
            description="Selecione um comando no menu abaixo para ver detalhes."
        )
        await ctx.send(embed=embed, view=view)
