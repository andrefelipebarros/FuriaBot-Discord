import os
from pathlib import Path
import discord
from discord.ext import commands
import config
from help_menu import setup_help

intents = discord.Intents.all()

# --- BOT SETUP ---
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        setup_help(self)

    async def setup_hook(self):
        await self.tree.sync()
        base = Path(__file__).parent
        cogs_dir = base / "cogs"
        print(f"🔍 Carregando cogs de: {cogs_dir.resolve()}")

        if not cogs_dir.exists():
            print("❌ Diretório cogs/ não encontrado")
            return

        for file in cogs_dir.iterdir():
            if file.suffix == ".py":
                ext = f"cogs.{file.stem}"
                try:
                    await self.load_extension(ext)
                    print(f"✅ Loaded extension {ext}")
                except Exception as e:
                    print(f"❌ Falha ao carregar {ext}: {e}")


bot = MyBot()

# --- BOT ONLINE NOTICE ---
@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")

# --- TEST COMMAND ---
@bot.command(help="Diz olá ao usuário.")
async def ola(ctx):
    await ctx.reply("Olá! Tudo bem?")

if __name__ == "__main__":
    bot.run(config.DISCORD_TOKEN)
