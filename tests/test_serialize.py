import pytest
import lib.serialize as serialize
from lib.parse import PlayerInfo
from datetime import datetime as dt


def describe_datetime():
    def serializes_date():
        time = dt(2022, 5, 6, 4, 54, 13)
        assert serialize.datetime(time) == "2022-05-06 04:54:13"


def describe_seconds():
    def serializes_seconds():
        time = 5
        assert serialize.seconds(time) == "0:00:05"

    def serializes_minutes():
        time = 4 * 60 + 53
        assert serialize.seconds(time) == "0:04:53"

    def serializes_hours():
        time = 9 * 60 * 60 + 4 * 60 + 53
        assert serialize.seconds(time) == "9:04:53"

    def serializes_large_hours():
        time = 119 * 60 * 60 + 4 * 60 + 53
        assert serialize.seconds(time) == "119:04:53"


@pytest.fixture
def simple_a():
    player = PlayerInfo(
        dt(2022, 5, 29, 19, 37, 37),
        6,
        1,
        ["D:/Videos/cool.mp4", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"],
    )
    text = (
        "[2022-05-29 19:37:37] Pos=0:00:06, Idx=1\n"
        "  D:/Videos/cool.mp4\n"
        "  https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )
    return player, text


@pytest.fixture
def simple_b():
    player = PlayerInfo(
        dt(2022, 5, 29, 19, 38, 1),
        24,
        2,
        ["D:/Videos/cool.mp4", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"],
    )
    text = (
        "[2022-05-29 19:38:01] Pos=0:00:24, Idx=2\n"
        "  D:/Videos/cool.mp4\n"
        "  https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )
    return player, text


@pytest.fixture
def short_a():
    player = PlayerInfo(
        dt(2022, 6, 7, 19, 42, 50),
        2 * 3600 + 53 * 60 + 43,
        1,
        ["D:\\Videos\\anybody.mp4"],
    )
    text = "[2022-06-07 19:42:50] Pos=2:53:43, Idx=1\n  D:\\Videos\\anybody.mp4"
    return player, text


@pytest.fixture
def long_a():
    player = PlayerInfo(
        dt(2022, 6, 7, 15, 35, 49),
        1 * 3600 + 43 * 60 + 27,
        8,
        [
            "D:\\Videos\\One.mp4",
            "D:\\Videos\\Two.mp4",
            "D:\\Videos\\Three.mp4",
            "D:\\Videos\\Four.mp4",
            "D:\\Videos\\Five.mp4",
            "D:\\Videos\\Six.mp4",
            "D:\\Videos\\Seven.mp4",
            "D:\\Videos\\Eight.mp4",
            "D:\\Videos\\Nine.mp4",
            "D:\\Videos\\Ten.mp4",
            "D:\\Videos\\Eleven.mp4",
            "D:\\Videos\\Twelve.mp4",
        ],
    )
    text = (
        "[2022-06-07 15:35:49] Pos=1:43:27, Idx=8\n"
        "  D:\\Videos\\One.mp4\n"
        "  D:\\Videos\\Two.mp4\n"
        "  D:\\Videos\\Three.mp4\n"
        "  D:\\Videos\\Four.mp4\n"
        "  D:\\Videos\\Five.mp4\n"
        "  D:\\Videos\\Six.mp4\n"
        "  D:\\Videos\\Seven.mp4\n"
        "  D:\\Videos\\Eight.mp4\n"
        "  D:\\Videos\\Nine.mp4\n"
        "  D:\\Videos\\Ten.mp4\n"
        "  D:\\Videos\\Eleven.mp4\n"
        "  D:\\Videos\\Twelve.mp4"
    )
    return player, text


def describe_player():
    @pytest.mark.parametrize(
        "fixture_name",
        ["simple_a", "simple_b", "short_a", "long_a"],
    )
    def serializes_player(fixture_name, request: pytest.FixtureRequest):
        print(f"Testing serialization of: #{fixture_name}")

        player, text = request.getfixturevalue(fixture_name)

        assert serialize.player(player) == text


def describe_players():
    def serializes_case_1(simple_a, simple_b):
        a_player, a_text = simple_a
        b_player, b_text = simple_b

        text = "\n".join((a_text, b_text))
        assert serialize.players((a_player, b_player)) == text

    def serializes_case_2(simple_a, simple_b, long_a):
        a_player, a_text = simple_a
        b_player, b_text = simple_b
        long_player, long_text = long_a

        text = "\n".join((a_text, long_text, b_text))
        assert serialize.players((a_player, long_player, b_player)) == text
