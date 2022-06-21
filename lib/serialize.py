from lib.parse import PlayerInfo, DATETIME_FORMAT


def datetime(dt):
    return dt.strftime(DATETIME_FORMAT)


def seconds(s):
    h = s // 3600
    s = s % 3600
    m = s // 60
    s = s % 60

    return f"{h:d}:{m:02d}:{s:02d}"


def player(p: PlayerInfo):
    lines = []

    header = (
        f"[{datetime(p.saved_at)}] Pos={seconds(p.playback_pos)}, Idx={p.playlist_idx}"
    )
    lines.append(header)

    for item in p.playlist:
        lines.append(f"  {item}")

    return "\n".join(lines)


def players(ps: list[PlayerInfo]):
    return "\n".join(player(p) for p in ps)
