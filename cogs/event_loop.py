import time
from discord.ext import tasks, commands
from game import Phase


class EventLoop(commands.Cog):
    # the event loop ends pending days/nights
    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        self.event_loop.cancel()

    @tasks.loop(seconds=5.0)
    async def event_loop(self):
        for game in self.bot.games.values():
            if not game.has_started:
                continue
            curr_t = time.time()
            phase_end = time.mktime(game.phase_end_at)
            if curr_t > phase_end:
                if game.phase == Phase.DAY:
                    # no lynch achieved
                    await game.channel.send('Nobody was lynched')
                    for player in game.players:
                        player.votes = []
                # wip: resolve night actions here
                await game.increment_phase()

    @event_loop.before_loop
    async def before_loop(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(EventLoop(bot))
