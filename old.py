from dataclasses import dataclass
import re
import datetime
import subprocess
from collections import namedtuple
from pprint import pprint

# config

SESSION_PATH = R"C:\Users\James\scoop\persist\mpv\portable_config\session.txt"
LOAD_SESSIONS_WITHIN_THE_LAST = datetime.timedelta(hours=2)
DELETE_SESSIONS_AFTER = datetime.timedelta(days=30)

# code


class PlayerInfoReader:
    HEADER_RE = re.compile(r"\[(.*?)\] *Pos *= *([^ ]*?), *Idx *= *([^ ]*?)")

    @staticmethod
    def _parse_datetime(text):
        """parse a datetime in this format: 2022-05-30 00:31:13"""

        time_format = "%Y-%m-%d %H:%M:%S"
        return datetime.datetime.strptime(text, time_format)

    @staticmethod
    def _parse_play_seconds(text):
        """parse a video play time in this format: 2:53:42"""

        nums = [int(x) for x in text.split(":")]
        seconds = 0

        for i, n in enumerate(nums):
            power = len(nums) - i - 1
            seconds += n * 60**power

        return text

    @classmethod
    def _parse_header(cls, line):
        """parse the header line of a video info section"""

        # use regex to match the header
        match = cls.HEADER_RE.fullmatch(line)
        if not match:
            raise ParseError("Invalid header format")

        added_date, play_seconds, idx = HEADER_RE.fullmatch(line).groups()

        added_date = cls._parse_datetime(added_date)
        play_seconds = cls._parse_play_seconds(play_seconds)
        idx = int(idx)

        return added_date, play_seconds, idx

    @staticmethod
    def _is_header(line):
        """check if a line of text is a header line"""

        if len(text.strip()) == 0:
            return False

        if text.startswith(" "):
            return False

        return True

    @classmethod
    def _parse_video_section(cls, section):
        """parse an entire video section"""

        # parse the header
        ostime, playtime, idx = cls._parse_header(lines[0])

        # parse the rest of the lines
        items = [x.strip() for x in lines[1:]]
        original_text = "\n".join(lines)
        return cls(ostime, playtime, idx, items, original_text)


@dataclass
class PlayerInfo:
    created_at: datetime.datetime
    play_pos: int
    item_idx: int
    items: list[str]
    original_text: str

    @classmethod
    def load_sessions(cls, path):
        with open(path, "r", encoding="utf8") as f:
            content = f.read()

        # get non-empty lines
        lines = content.splitlines()
        lines = [x for x in lines if len(x.strip()) > 0]

        # group lines into sessions
        current_session = None
        sessions = []

        for line in lines:
            if line.startswith("  "):
                # is playlist item
                current_session.append(line)
            else:
                # is header line
                current_session = []
                sessions.append(current_session)
                current_session.append(line)

        # convert each list into a session
        return [cls._parse_info_lines(s) for s in sessions]

    def is_old(self):
        now = datetime.datetime.now()
        return now - self.created_at > DELETE_SESSIONS_AFTER

    def is_current(self):
        now = datetime.datetime.now()
        return now - self.created_at < LOAD_SESSIONS_WITHIN_THE_LAST

    def launch(self):
        args = [
            "mpv",
            *self.items,
            "--pause",
            f"--playlist-start={self.item_idx - 1}",
            f"--script-opts=initial-seek={self.play_pos}",
        ]

        subprocess.Popen(args, creationflags=subprocess.DETACHED_PROCESS)


def discard_old_sessions(path: str, sessions: list[PlayerInfo]):
    sessions = [s for s in sessions if not s.is_old()]
    session_text = "\n".join(s.original_text for s in sessions)
    with open(path, "w", encoding="utf8") as f:
        f.write(session_text)
        f.write("\n")


class ParseError(Exception):
    pass


def main():
    sessions = Video.load_sessions(SESSION_PATH)

    for s in sessions:
        if s.is_current():
            s.launch()

    discard_old_sessions(SESSION_PATH, sessions)
    # discard_old_sessions(sessions)
    # print([s.original_text for s in sessions])
    # for s in sessions:
    #     print(s.original_text)
    # print([s.original_text for s in sessions if not s.is_old()])
    # sessions[0].launch()
    # sessions[1].launch()


main()
