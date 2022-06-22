import re
from datetime import datetime as dt
from typing import NamedTuple

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def datetime(text):
    """parse a datetime in this format: 2022-05-30 00:31:13"""

    return dt.strptime(text, DATETIME_FORMAT)


def playback_time(text):
    """parse a video play time in this format: 2:53:42"""

    match [int(x) for x in text.split(":")]:
        case [s]:
            return s
        case [m, s]:
            return m * 60 + s
        case [h, m, s]:
            return h * 3600 + m * 60 + s
        case _:
            raise ValueError("More than 3 segments. Invalid time format.")


HEADER_RE = re.compile(
    r" *\[ *([^ ].+?[^ ]?) *\] *Pos *= *([^ ]*?) *, *Idx *= *([^ ]*?) *"
)


def header(line):
    """parse the header line of a video info section"""

    match = HEADER_RE.fullmatch(line)
    if not match:
        raise ValueError(f"Invalid header format: {line}")

    saved_at, playback_pos, playlist_pos = HEADER_RE.fullmatch(line).groups()

    saved_at = datetime(saved_at)
    playback_pos = playback_time(playback_pos)
    playlist_pos = int(playlist_pos)

    return saved_at, playback_pos, playlist_pos


def should_be_header(line):
    """check if a line of text should be a header line (i.e. line has no indentation)"""

    if len(line.strip()) == 0:
        return False

    if line.startswith(" "):
        return False

    return True


class PlayerInfo(NamedTuple):
    saved_at: dt
    playback_pos: int
    playlist_idx: int
    playlist: list[str]

    def validate(self):
        if 0 <= self.playlist_idx < len(self.playlist):
            return

        raise IndexError(
            f"Playlist has {len(self.playlist)} items, but playlist index is {self.playlist_idx}."
        )


def players(lines: str | list[str]) -> list[PlayerInfo]:
    """parse text containing definitions of players, i.e. a session file"""

    if isinstance(lines, str):
        lines = lines.splitlines()

    all_players = []

    for l in lines:
        if len(l.strip()) == 0:
            continue

        if should_be_header(l):
            saved_at, playback_pos, playlist_idx = header(l)
            p = PlayerInfo(saved_at, playback_pos, playlist_idx, [])
            all_players.append(p)
        else:
            if len(all_players) == 0:
                raise IndentationError("A non-header line is found before any headers")

            all_players[-1].playlist.append(l.strip())

    return all_players
