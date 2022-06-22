-- This is a pairing script to be put in:
-- (MPV_PATH)/script

-- Add a keybinding like:
-- Ctrl+s script-message-to save_session save-session

local SESSION_FILENAME = 'session.txt'

local function get_config_dir()
  local config_path = mp.find_config_file("mpv.conf")
  return config_path:match([[(.+[\/])]])
end

local function get_session_path()
  return get_config_dir() .. SESSION_FILENAME
end

local function write_to_path(path, text)
  f = io.open(path, "a") -- open in append mode, file should be created automatically
  if f == nil then return nil, "Error opening file for writing" end

  f:write(text, "\n")

  if not f:close() then return nil, "Unknown IO error" end

  return true
end

-- get the paths of the videos in the playlist
local function get_playlist_paths()
  local count = tonumber(mp.get_property("playlist-count"))
  local paths = {}

  for i = 1, count do
    paths[i] = mp.get_property("playlist/" .. i - 1 .. "/filename")
  end

  return paths
end

-- index of current video in playlist
-- 1-indexed
local function get_playlist_idx()
  return tonumber(mp.get_property("playlist-playing-pos")) + 1
end

local function get_datetime()
  return os.date('%Y-%m-%d %X')
end

local function get_playback_time()
  local seconds = mp.get_property("time-pos")
  if seconds == nil then return end

  local hours = math.floor(seconds / 3600)
  seconds = seconds % 3600

  local minutes = math.floor(seconds / 60)
  seconds = seconds % 60

  return hours, minutes, seconds
end

local function get_play_time()
  local h, m, s = get_playback_time()
  if h == nil then
    return nil, "Can't get current playback time, is the video loaded?"
  end

  return string.format("%d:%02d:%02d", h, m, s)
end

local function generate_player_info()
  local play_time, error = get_play_time()
  if play_time == nil then return nil, error end

  local header = "[" .. get_datetime() .. "] Pos=" .. play_time .. ", Idx=" .. get_playlist_idx()
  local lines = { header }

  local paths = get_playlist_paths()
  -- add 2 spaces in front of each path
  for i = 1, #paths do
    lines[#lines + 1] = "  " .. paths[i]
  end

  local session = table.concat(lines, "\n")
  return session
end

local function save_session()
  local session = generate_player_info()
  local path = get_session_path()

  write_to_path(path, session)
  mp.osd_message("Saved video session to: " .. path)
end

mp.register_script_message("save-session", save_session)
