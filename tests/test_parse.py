import pytest
import lib.parse as parse
from datetime import datetime as dt


def assert_date_equals(date, year, month, day, hour, minute, second):
    assert date.year == year
    assert date.month == month
    assert date.day == day
    assert date.hour == hour
    assert date.minute == minute
    assert date.second == second


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

        # text = "[2022-05-29 19:37:37] Pos=0:00:06, Idx=1"

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
