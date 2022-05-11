This is a **help** dialogue for changing the values of settings.

# Options

- `autoconnect` – whether to automatically connect to the lbrynet SDK or not – boolean value, defaults to False
- `default_opener` – the external program `open` uses to open URLs – string, defaults to "xdg-open"
- `markdown_reader` – the external program used to view markdown – string, defaults to None (use FastLBRY's build-in reader)
- `music_player` - the external program `music` uses to play publications – string, defaults to "xdg-open"
- `player` – the external program `play` uses to play publications – string, defaults to "xdg-open"
- `save_history` – whether to save the command history to a file on quit or not – boolean, defaults to False
- `theme` – the theme to use – string, defaults to "default"

# Special Python keywords and their JSON equivalents

Here are some JSON equivalents to a few special python keywords, useful if you want to edit the JSON manually. The JSON file is in either in `$XDG_DATA_HOME/flbry/config.json` or `~/.local/share/flbry/config.json`.

| Keyword | JSON equivalent |
| ------- | --------------- |
|  True   |       true      |
|  False  |      false      |
|  None   |       null      |
