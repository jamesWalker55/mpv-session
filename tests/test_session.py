from io import StringIO
import lib.session as session
from lib.parse import PlayerInfo
from datetime import datetime as dt
import pytest
from random import Random

random = Random("test_session")


@pytest.fixture
def one_session():
    # list of players must be sorted by saved_at time
    players = [
        # 1
        PlayerInfo(dt(2022, 1, 1, 1, 0, 0), 0, 0, []),
        PlayerInfo(dt(2022, 1, 1, 1, 0, 10), 0, 0, []),
    ]
    ranges = [(0, 2)]
    return players, ranges


@pytest.fixture
def two_sessions():
    # list of players must be sorted by saved_at time
    players = [
        # 1
        PlayerInfo(dt(2022, 1, 1, 1, 0, 0), 0, 0, []),
        PlayerInfo(dt(2022, 1, 1, 1, 0, 10), 0, 0, []),
        PlayerInfo(dt(2022, 1, 1, 1, 0, 30), 0, 0, []),
        # 2
        PlayerInfo(dt(2022, 1, 1, 1, 8, 40), 0, 0, []),
        PlayerInfo(dt(2022, 1, 1, 1, 9, 10), 0, 0, []),
    ]
    ranges = [(0, 3), (3, 5)]
    return players, ranges


@pytest.fixture
def three_sessions():
    # list of players must be sorted by saved_at time
    players = [
        # 1
        PlayerInfo(dt(2022, 1, 1, 1, 0, 0), 0, 0, []),
        PlayerInfo(dt(2022, 1, 1, 1, 0, 10), 0, 0, []),
        PlayerInfo(dt(2022, 1, 1, 1, 0, 30), 0, 0, []),
        # 2
        PlayerInfo(dt(2022, 1, 1, 1, 8, 40), 0, 0, []),
        PlayerInfo(dt(2022, 1, 1, 1, 9, 10), 0, 0, []),
        PlayerInfo(dt(2022, 1, 1, 1, 10, 40), 0, 0, []),
        # 3
        PlayerInfo(dt(2022, 1, 1, 9, 27, 10), 0, 0, []),
        PlayerInfo(dt(2022, 1, 1, 9, 27, 40), 0, 0, []),
        PlayerInfo(dt(2022, 1, 1, 9, 27, 58), 0, 0, []),
    ]
    ranges = [(0, 3), (3, 6), (6, 9)]
    return players, ranges


def describe_from_players():
    @pytest.mark.parametrize(
        "fixture_name",
        ["one_session", "two_sessions", "three_sessions"],
    )
    def creates_sessions_from_sorted_players(
        fixture_name, request: pytest.FixtureRequest
    ):
        print(f"Testing session creation from: #{fixture_name}")

        players, ranges = request.getfixturevalue(fixture_name)

        ss = session.from_players(players)

        assert len(ss) == len(ranges)

        for s, r in zip(ss, ranges):
            a, b = r
            assert s == players[a:b]

    @pytest.mark.parametrize(
        "fixture_name",
        ["two_sessions", "three_sessions"],
    )
    def creates_sessions_from_unsorted_players(
        fixture_name, request: pytest.FixtureRequest
    ):
        print(f"Testing session creation from: #{fixture_name}")

        players, ranges = request.getfixturevalue(fixture_name)

        shuffled_players = random.sample(players, k=len(players))
        ss = session.from_players(shuffled_players)

        assert len(ss) == len(ranges)

        for s, r in zip(ss, ranges):
            a, b = r
            assert s == players[a:b]

    def creates_no_sessions_from_empty_list():
        ss = session.from_players([])

        assert len(ss) == 0


def describe_to_players():
    @pytest.mark.parametrize(
        "fixture_name",
        ["one_session", "two_sessions", "three_sessions"],
    )
    def retains_order_of_players(fixture_name, request: pytest.FixtureRequest):
        print(f"Testing with: #{fixture_name}")

        players, _ = request.getfixturevalue(fixture_name)

        new_players = session.to_players(session.from_players(players))

        assert players == new_players

    def accepts_empty_list():
        players = session.to_players([])

        assert len(players) == 0


@pytest.fixture
def typical_fd():
    f = StringIO(
        "[2022-05-29 19:37:37] Pos=0:00:06, Idx=1\n"
        "  D:/Videos/cool.mp4\n"
        "  https://www.youtube.com/watch?v=dQw4w9WgXcQ\n"
        "[2022-05-29 19:38:01] Pos=0:00:24, Idx=2\n"
        "  D:/Videos/cool.mp4\n"
        "  https://www.youtube.com/watch?v=dQw4w9WgXcQ\n"
    )
    yield f
    f.close()


@pytest.fixture
def empty_fd():
    f = StringIO("")
    yield f
    f.close()


def describe_load():
    def loads_empty_file(empty_fd):
        s = session.load(empty_fd)
        assert len(s) == 0

    def loads_typical_session(typical_fd):
        s = session.load(typical_fd)
        assert len(s) == 1


def describe_save():
    def saves_empty_session(empty_fd):
        session.save(empty_fd, [])

        empty_fd.seek(0)
        text = empty_fd.read()
        assert text == ""

    def saves_typical_session(typical_fd):
        s = session.load(typical_fd)

        typical_fd.seek(0)

        session.save(typical_fd, s)

        typical_fd.seek(0)
        text = typical_fd.read()
        assert text == (
            "[2022-05-29 19:37:37] Pos=0:00:06, Idx=1\n"
            "  D:/Videos/cool.mp4\n"
            "  https://www.youtube.com/watch?v=dQw4w9WgXcQ\n"
            "[2022-05-29 19:38:01] Pos=0:00:24, Idx=2\n"
            "  D:/Videos/cool.mp4\n"
            "  https://www.youtube.com/watch?v=dQw4w9WgXcQ\n"
        )
