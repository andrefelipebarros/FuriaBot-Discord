import discord
from discord.ext import commands, tasks
from services.live_status import fetch_live_match

live_states = {}

class LiveStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_live_matches.start()

    def cog_unload(self):
        self.check_live_matches.cancel()

    @commands.command(name="live_start")
    async def start_live(self, ctx):
        chat_id = ctx.channel.id
        if live_states.get(chat_id, {}).get("status") == "active":
            return await ctx.reply("🔴 Live já está ativo.")
        live_states[chat_id] = {"status": "active", "message_id": None}
        await ctx.reply("✅ Atualizações ao vivo iniciadas!")

    @commands.command(name="live_stop")
    async def stop_live(self, ctx):
        chat_id = ctx.channel.id
        if chat_id in live_states:
            live_states.pop(chat_id)
            await ctx.reply("🛑 Atualizações ao vivo encerradas.")
        else:
            await ctx.reply("❌ Nenhuma atualização ao vivo em andamento.")

    @tasks.loop(seconds=45)
    async def check_live_matches(self):
        for chat_id, state in list(live_states.items()):
            if state.get("status") != "active":
                continue

            info = await fetch_live_match()
            if not info:
                continue

            text = (
                f"🔴 **Live - Round {info['round']}**\n"
                f"**{info['team1']}** vs **{info['team2']}**\n"
                f"**Placar:** {info['score']}"
            )

            channel = self.bot.get_channel(chat_id)
            if not channel:
                continue

            if state.get("message_id"):
                try:
                    msg = await channel.fetch_message(state["message_id"])
                    await msg.edit(content=text)
                except discord.NotFound:
                    msg = await channel.send(text)
                    state["message_id"] = msg.id
            else:
                msg = await channel.send(text)
                state["message_id"] = msg.id

async def setup(bot: commands.Bot):
    await bot.add_cog(LiveStatus(bot))
