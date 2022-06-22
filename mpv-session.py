from calendar import month
import lib.session as session
import lib.parse as parse
import lib.serialize as serialize
import lib.run as run
from datetime import timedelta

SESSIONS_PATH = R"C:\Users\James\scoop\persist\mpv\portable_config\session.txt"

MAXIMUM_SESSIONS_COUNT = 30


def main():
    with open(SESSIONS_PATH, "r", encoding="utf8") as f:
        sessions = session.load(f)

    print(f"{len(sessions)} sessions loaded from {SESSIONS_PATH}.")

    # only get the last 30 sessions
    sessions = sessions[-MAXIMUM_SESSIONS_COUNT:]

    if len(sessions) == 0:
        print(
            "Session file is empty. Please save some sessions before using this script!"
        )
        return

    last_session = sessions[-1]

    for player in last_session:
        run.mpv(player.playlist, player.playlist_idx, player.playback_pos)

    with open(SESSIONS_PATH, "w", encoding="utf8") as f:
        session.save(f, sessions)


main()
