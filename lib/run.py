import subprocess


MPV_PATH = "mpv"


def set_mpv_path(path):
    global MPV_PATH
    MPV_PATH = path


def mpv(playlist_items, playlist_start, playback_pos):
    args = [
        MPV_PATH,
        *playlist_items,
        "--pause",
        f"--playlist-start={playlist_start}",
        f"--script-opts=initial-seek={playback_pos}",
    ]

    return subprocess.Popen(args, creationflags=subprocess.CREATE_NO_WINDOW)
