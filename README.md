# mpv-session

This lets you save videos into a session, then load them back later.

When you have multiple MPV players open and you want to "bookmark" them, you can save them into a session then load it back in the future.

There are 2 parts involved:

- [an MPV lua script for saving sessions](./script/save-session.lua)
- [a Python script for loading sessions](./mpv-session.py)

## Installing

[Install Python 3.10](https://www.python.org/) then [download/clone this repo](https://github.com/jamesWalker55/mpv-session/archive/refs/heads/main.zip).

Copy `save-session.lua` from the `script` folder to your MPV `scripts` folder.

Then add a keybinding to the `save-session` command in your MPV's `input.conf`, like this:

```bash
# Example: Use Ctrl+s to save the current player in a session
Ctrl+s script-message-to save_session save-session
```

Then everything should be set up.

## Usage

Here is how you use this:

1. You have multiple MPV players open
2. For each MPV player you want to save in a session, press `Ctrl+S` (or whatever keybinding you set) to save it to a session
   - Players that are saved within **2 minutes** of each other are considered as being in the same session
3. When you want to load your last session, run the `mpv-session.py` script with Python
