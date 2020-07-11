import unittest
from unittest.mock import AsyncMock, Mock, patch
from godfather.cogs.mafia import mafia


class MafiaCogTestCase(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.bot = Mock()
        self.cog = mafia.Mafia(self.bot)

    async def test_create_game_on_server(self):
        """Test cases:
        - Already a mafia game running on the server, STOP
        - A mafia game running on another server, CONT
        - No games running on any server, CONT

        Mock:
        - self.bot.games
        - ctx.guild.id
        - ctx.send
        """
        # REFUSE_SUBSTRING = "A game of mafia is already running in this server."
        # MAKE_SUBSTRING = "Started a game of mafia in"

        # test_values = (
        #     ({11: Mock(), 22: Mock()}, 11, REFUSE_SUBSTRING),
        #     ({11: Mock(), 22: Mock()}, 33, MAKE_SUBSTRING),
        #     ({}, 11, MAKE_SUBSTRING)
        # )

        # for bot_games, guild_id, expected in test_values:
        #     with self.subTest(bot_games=bot_games, guild_id=guild_id,
        #                       expected=expected):
        #         mock_ctx = AsyncMock(**{'guild.id': guild_id})
        #         self.cog.bot.games = bot_games

        #         await self.cog.creategame(mock_ctx)
        #         self.assertTrue(mock_ctx.send.call_args[0].startswith(expected))
        pass

    async def test_join(self):
        # Test cases:
        # - Any player, game already started
        # - Player already inside game, already joined
        # - Player already inside game and max reached, already joined
        # - Player not inside game and max reached, max reached
        # - Not started, player not in game, not max reached, can join
        # Mock:
        # - ctx (guild.id)
        # - bot (games)
        # - json
        pass
