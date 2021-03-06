from datetime import datetime
from discord.ext import tasks, commands
from godfather.game import Phase
from godfather.errors import PhaseChangeError


class EventLoop(commands.Cog):
    # the event loop ends pending days/nights
    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        self.event_loop.cancel()  # pylint: disable=no-member

    @tasks.loop(seconds=10.0)
    async def event_loop(self):
        for game in self.bot.games.values():
            if not game.has_started:
                continue
            if game.phase == Phase.STANDBY:
                return
            curr_t = datetime.now()
            phase_end = game.phase_end_at
            if curr_t > phase_end:
                if game.phase == Phase.DAY:
                    # no lynch achieved
                    await game.channel.send('Nobody was lynched')
                try:
                    await game.increment_phase(self.bot)
                except Exception as exc:
                    raise PhaseChangeError(None, *exc.args)

    @event_loop.before_loop
    async def before_loop(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(EventLoop(bot))
