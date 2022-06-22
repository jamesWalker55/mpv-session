import pytest
import lib.parse as parse
from datetime import datetime as dt


def describe_datetime():
    def parses_correct_date():
        text = "2022-05-30 00:31:13"
        ans = dt(2022, 5, 30, 0, 31, 13)
        assert parse.datetime(text) == ans

    def raises_exception_for_invalid_date():
        text = "2022-05-35 00:31:13"
        with pytest.raises(ValueError):
            parse.datetime(text)

    def raises_exception_for_invalid_format():
        text = "2022-05-30T00:31:13"
        with pytest.raises(ValueError):
            parse.datetime(text)


def describe_playback_time():
    def parses_seconds_only():
        text = "123"
        ans = 123
        assert parse.playback_time(text) == ans

    def does_not_parse_miliseconds():
        text = "123.5"
        with pytest.raises(ValueError):
            parse.playback_time(text)

    def parses_minutes():
        text = "8:46"
        ans = 526
        assert parse.playback_time(text) == ans

    def parses_large_minutes():
        text = "68:16"
        ans = 4096
        assert parse.playback_time(text) == ans

    def parses_hours():
        text = "2:42:53"
        ans = 9773
        assert parse.playback_time(text) == ans

    def does_not_parse_more_than_four_segments():
        text = "2:42:53:99"
        with pytest.raises(ValueError):
            parse.playback_time(text)


def describe_header():
    def parses_typical_header():
        text = "[2022-05-29 19:37:37] Pos=0:00:06, Idx=1"
        saved_at = dt(2022, 5, 29, 19, 37, 37)
        playback_pos = 6
        playlist_pos = 1

        a, b, c = parse.header(text)
        assert a == saved_at
        assert b == playback_pos
        assert c == playlist_pos

    def parses_header_with_more_spacing():
        text = "[ 2022-05-29 19:37:37  ]  Pos = 0:00:06  ,   Idx   =   1 "
        saved_at = dt(2022, 5, 29, 19, 37, 37)
        playback_pos = 6
        playlist_pos = 1

        a, b, c = parse.header(text)
        assert a == saved_at
        assert b == playback_pos
        assert c == playlist_pos

    def does_not_parse_lowercase_header():
        text = "[2022-05-29 19:37:37] pos=0:00:06, idx=1"

        with pytest.raises(ValueError):
            parse.header(text)

    def does_not_parse_invalid_date():
        text = "[hello] Pos=0:00:06, Idx=1"

        with pytest.raises(ValueError):
            parse.header(text)

    def does_not_parse_invalid_position():
        text = "[2022-05-29 19:37:37] Pos=hello, Idx=1"

        with pytest.raises(ValueError):
            parse.header(text)

    def does_not_parse_invalid_index():
        text = "[2022-05-29 19:37:37] Pos=0:00:06, Idx=hello"

        with pytest.raises(ValueError):
            parse.header(text)

    def does_not_parse_missing_position():
        text = "[2022-05-29 19:37:37] Idx=1"

        with pytest.raises(ValueError):
            parse.header(text)

    def does_not_parse_missing_index():
        text = "[2022-05-29 19:37:37] Pos=0:00:06"

        with pytest.raises(ValueError):
            parse.header(text)


def describe_players():
    def parses_typical_session():
        text = (
            "[2022-05-29 19:37:37] Pos=0:00:06, Idx=1\n"
            "  D:/Videos/cool.mp4\n"
            "  https://www.youtube.com/watch?v=dQw4w9WgXcQ\n"
            "[2022-05-29 19:38:01] Pos=0:00:24, Idx=2\n"
            "  D:/Videos/cool.mp4\n"
            "  https://www.youtube.com/watch?v=dQw4w9WgXcQ\n"
        )
        players = parse.players(text)

        assert len(players) == 2

        p = players[0]
        assert p.saved_at == dt(2022, 5, 29, 19, 37, 37)
        assert p.playback_pos == 6
        assert p.playlist_idx == 1
        assert p.playlist == [
            "D:/Videos/cool.mp4",
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        ]

        p = players[1]
        assert p.saved_at == dt(2022, 5, 29, 19, 38, 1)
        assert p.playback_pos == 24
        assert p.playlist_idx == 2
        assert p.playlist == [
            "D:/Videos/cool.mp4",
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        ]

    def parses_single_player():
        text = (
            "[2022-05-30 00:31:13] Pos=2:53:42, Idx=1\n"
            "  D:\\Resources\\test stream.mp4\n"
        )
        players = parse.players(text)

        assert len(players) == 1

        p = players[0]
        assert p.saved_at == dt(2022, 5, 30, 0, 31, 13)
        assert p.playback_pos == 10422
        assert p.playlist_idx == 1
        assert p.playlist == [R"D:\Resources\test stream.mp4"]

    def parses_three_players():
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
            "  D:\\Videos\\Twelve.mp4\n"
            "[2022-06-07 19:42:50] Pos=2:53:43, Idx=1\n"
            "  D:\\Videos\\anybody.mp4\n"
            "[2022-06-07 19:42:51] Pos=3:50:45, Idx=8\n"
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
            "  D:\\Videos\\Twelve.mp4\n"
        )
        players = parse.players(text)

        assert len(players) == 3
        long_playlist = [
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
        ]

        p = players[0]
        assert p.playlist == long_playlist
        assert p.saved_at == dt(2022, 6, 7, 15, 35, 49)
        assert p.playback_pos == 1 * 60 * 60 + 43 * 60 + 27
        assert p.playlist_idx == 8
        assert p.playlist == long_playlist

        p = players[1]
        assert p.saved_at == dt(2022, 6, 7, 19, 42, 50)
        assert p.playback_pos == 2 * 60 * 60 + 53 * 60 + 43
        assert p.playlist_idx == 1
        assert p.playlist == ["D:\\Videos\\anybody.mp4"]

        p = players[2]
        assert p.saved_at == dt(2022, 6, 7, 19, 42, 51)
        assert p.playback_pos == 3 * 60 * 60 + 50 * 60 + 45
        assert p.playlist_idx == 8
        assert p.playlist == long_playlist

    def does_not_parse_videos_before_header():
        text = (
            "  D:/Videos/cool.mp4\n"
            "[2022-05-29 19:37:37] Pos=0:00:06, Idx=1\n"
            "  D:/Videos/cool.mp4\n"
            "  https://www.youtube.com/watch?v=dQw4w9WgXcQ\n"
        )

        with pytest.raises(IndentationError):
            parse.players(text)

    def parses_empty_text():
        text = ""

        players = parse.players(text)

        assert len(players) == 0
