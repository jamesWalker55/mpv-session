from lib.parse import PlayerInfo
import lib.parse as parse
import lib.serialize as serialize
from datetime import timedelta as delta

# maximum time gap between videos saved in the same session
SESSION_MAX_GAP = delta(minutes=2)


def from_players(players: list[PlayerInfo]) -> list[list[PlayerInfo]]:
    players = players.copy()
    players.sort(key=lambda p: p.saved_at)

    sessions = []

    for p in players:
        # if no sessions yet, create new session
        if len(sessions) == 0:
            sessions.append([p])
            continue

        last_p = sessions[-1][-1]

        # if saved way later than the last one, then create new session
        if p.saved_at - last_p.saved_at > SESSION_MAX_GAP:
            sessions.append([p])
            continue

        # otherwise, add to last session
        sessions[-1].append(p)

    return sessions


def to_players(sessions):
    return [player for session in sessions for player in session]


def load(f):
    players = parse.players(f.read())
    return from_players(players)


def save(f, sessions):
    players = to_players(sessions)
    text = serialize.players(players)

    f.write(text)

    if len(text) != 0:
        f.write("\n")
