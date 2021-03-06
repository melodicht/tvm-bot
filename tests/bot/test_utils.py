import unittest
from datetime import datetime, timedelta
from godfather.utils import from_now


class TestUtils(unittest.TestCase):

    def test_fromnow(self):
        time_now = datetime.now()
        delta_minutes = timedelta(minutes=1.2)
        delta_seconds = timedelta(seconds=45)

        time_future = time_now + delta_minutes
        time_past = time_now - delta_seconds

        self.assertEqual(from_now(time_future), 'in 1 minute')
        self.assertEqual(from_now(time_past), '45 seconds ago')
