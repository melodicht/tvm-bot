from godfather.roles import Role
from godfather.roles import all_roles

DESCRIPTION = 'You must get your target lynched by all means necessary.'


class Executioner(Role):
    def __init__(self):
        super().__init__(name='Executioner', role_id='executioner', description=DESCRIPTION)
        self.target = None

    async def on_death(self, game, player):
        # exe only attacks townies
        if not player.faction.name == 'Town':
            return
        for exe in game.filter_players(role='Executioner'):
            if exe.target == player:
                # exe becomes jester
                await exe.user.send('Your target has died. You are now a Jester!')
                Jester = all_roles['jester']
                exe.role = Jester()
                await exe.user.send(exe.role_pm)
