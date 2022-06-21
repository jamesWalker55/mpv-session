import re
from datetime import datetime as dt


def datetime(text):
    """parse a datetime in this format: 2022-05-30 00:31:13"""

    time_format = "%Y-%m-%d %H:%M:%S"
    return dt.strptime(text, time_format)


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
        raise ValueError("Invalid header format")

    saved_at, playback_pos, playlist_pos = HEADER_RE.fullmatch(line).groups()

    saved_at = datetime(saved_at)
    playback_pos = playback_time(playback_pos)
    playlist_pos = int(playlist_pos)

    return saved_at, playback_pos, playlist_pos


# def _is_header(line):
#     """check if a line of text is a header line"""

#     if len(text.strip()) == 0:
#         return False

#     if text.startswith(" "):
#         return False

#     return True

# def _parse_video_section(cls, section):
#     """parse an entire video section"""

#     # parse the header
#     ostime, playtime, idx = cls._parse_header(lines[0])

#     # parse the rest of the lines
#     items = [x.strip() for x in lines[1:]]
#     original_text = "\n".join(lines)
#     return cls(ostime, playtime, idx, items, original_text)
