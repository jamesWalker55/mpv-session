import lib.session as session
import lib.run as run
from lib.config import Config

MAXIMUM_SESSIONS_COUNT = 30

config = Config("config.json")


def get_sessions_path():
    try:
        assert isinstance(config.data, dict)
        path = config.data["sessions-path"]
        assert isinstance(path, str)
        return path
    except:
        return None


def set_sessions_path(path):
    if not isinstance(config.data, dict):
        config.data = {}

    config.data["sessions-path"] = str(path)
    config.save()


def main():
    sessions_path = get_sessions_path()

    if sessions_path is None:
        print("No session file configured.")
        print("Please enter the path of the file you want to load sessions from:")

        while True:
            sessions_path = input("  > ")

            if len(sessions_path.strip()) == 0:
                print("Please enter a path.")
                continue

            break

        set_sessions_path(sessions_path)

        print(f"Settings saved to: {config.get_config_path()}")

    with open(sessions_path, "r", encoding="utf8") as f:
        sessions = session.load(f)

    print(f"{len(sessions)} sessions loaded from {sessions_path}.")

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

    with open(sessions_path, "w", encoding="utf8") as f:
        session.save(f, sessions)


main()
