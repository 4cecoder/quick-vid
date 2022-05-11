#####################################################################
#                                                                   #
#  THIS IS A SOURCE CODE FILE FROM A PROGRAM TO INTERACT WITH THE   #
# LBRY PROTOCOL ( lbry.com ). IT WILL USE THE LBRY SDK ( lbrynet )  #
# FROM THEIR REPOSITORY ( https://github.com/lbryio/lbry-sdk )      #
# WHICH I GONNA PRESENT TO YOU AS A BINARY. SINCE I DID NOT DEVELOP #
# IT AND I'M LAZY TO INTEGRATE IN A MORE SMART WAY. THE SOURCE CODE #
# OF THE SDK IS AVAILABLE IN THE REPOSITORY MENTIONED ABOVE.        #
#                                                                   #
#      ALL THE CODE IN THIS REPOSITORY INCLUDING THIS FILE IS       #
# (C) J.Y.Amihud and Other Contributors 2021. EXCEPT THE LBRY SDK.  #
# YOU CAN USE THIS FILE AND ANY OTHER FILE IN THIS REPOSITORY UNDER #
# THE TERMS OF GNU GENERAL PUBLIC LICENSE VERSION 3 OR ANY LATER    #
# VERSION. TO FIND THE FULL TEXT OF THE LICENSE GO TO THE GNU.ORG   #
# WEBSITE AT ( https://www.gnu.org/licenses/gpl-3.0.html ).         #
#                                                                   #
# THE LBRY SDK IS UNFORTUNATELY UNDER THE MIT LICENSE. IF YOU ARE   #
# NOT INTENDING TO USE MY CODE AND JUST THE SDK. YOU CAN FIND IT ON #
# THEIR OFFICIAL REPOSITORY ABOVE. THEIR LICENSE CHOICE DOES NOT    #
# SPREAD ONTO THIS PROJECT. DON'T GET A FALSE ASSUMPTION THAT SINCE #
# THEY USE A PUSH-OVER LICENSE, I GONNA DO THE SAME. I'M NOT.       #
#                                                                   #
# THE LICENSE CHOSEN FOR THIS PROJECT WILL PROTECT THE 4 ESSENTIAL  #
# FREEDOMS OF THE USER FURTHER, BY NOT ALLOWING ANY WHO TO CHANGE   #
# THE LICENSE AT WILL. SO NO PROPRIETARY SOFTWARE DEVELOPER COULD   #
# TAKE THIS CODE AND MAKE THEIR USER-SUBJUGATING SOFTWARE FROM IT.  #
#                                                                   #
#####################################################################

import os
import json
from flbry.variables import *
import ast
from flbry import markdown
from flbry import connect
from flbry import donate
import readline

# This file will manage settings / installation and stuff like this.

default_key_value_pairs = {
        "theme":"default",
        "markdown_reader":None,
        "save_history":False,
        "default_opener":"xdg-open",
        "autoconnect":False,
        "player":"xdg-open",
        "music_player":"xdg-open",
        "default_tip":0.01,
        "dev_mode":False,
        "graph_force_ASCII":False,
        "ignore_width_forcing":False,
        "lbrynet_binary":"flbry/lbrynet",
        "default_editor":None,
        "librarian_instance": "https://librarian.bcow.xyz/",
        "auth_token":"",
        "comment_api": "https://comments.odysee.com/api/v2",
}

def get_settings_folder(flbry="flbry/"):

    try:
        data_dir = os.environ["XDG_DATA_HOME"] + "/" + flbry
    except:
        data_dir = os.path.expanduser("~/.local/share/"+flbry)

    try:
        os.makedirs(data_dir)
    except:
        pass

    return data_dir

def get_all_settings():
    with open(get_settings_folder()+"config.json") as f:
        settings_cache = json.load(f)

    return settings_cache

def check_config():

    # This function checks whether config exists. If not makes a
    # default setting.

    default = default_key_value_pairs

    if not os.path.exists(get_settings_folder()+"config.json"):
        with open(get_settings_folder()+"config.json", 'w') as f:
                json.dump(default, f, indent=4, sort_keys=True)

def get(key):

    # This function gets a setting from settings.

    data = get_all_settings()

    try:
        return data[key]
    except:
        return None

def save(key, value):

    # This function will save a value into the settings file.

    data = get_all_settings()

    data[key] = value

    with open(get_settings_folder()+"config.json", 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)


def set_theme(theme):

    # This will set a global theme


    user_themes = get_settings_folder()+"themes/"
    default_themes = "themes/"

    # First let's see if user has a theme folder in settings.
    try:
        os.makedirs(user_themes)
    except:
        pass

    # Trying to load the theme from user themes first
    try:
        with open(user_themes+theme+".json") as f:
            data = json.load(f)
    except Exception as e:

        try:
            with open(default_themes+theme+".json") as f:
                data = json.load(f)
        except Exception as e:

            return

    # Now let's actually apply the theme
    from flbry import variables

    for i in data:
        if data[i] in variables.clr:
            variables.clr[i] = clr[data[i]]
        else:
            variables.clr[i] = "\033["+data[i]+"m"



def install_desktop(force=True):

    # This function will generate a .desktop file. And put it in
    # ~/.local/

    if force:
        EXEC = "sh force_terminal.sh"
        TERM = "false"
    else:
        EXEC = "python3 run.py"
        TERM = "true"

    desktop = """[Desktop Entry]
Name=FastLBRY Terminal
GenericName=LBRY client
Path="""+os.getcwd()+"""
Exec="""+EXEC+"""
Icon="""+os.getcwd()+"""/icon.png
Terminal="""+TERM+"""
Type=Application
Categories=Network;AudioVideo"""

    # Now we need to get and place it in the right place

    desktop_file = get_settings_folder("applications/")+"FastLRBY-terminal.desktop"

    try:
        o = open(desktop_file, "w")
        o.write(desktop)
        o.close()
        center("Installed in Applications Menu", "bdgr")
    except:
        center("Installing in Applications Menu failed", "bdrd")

def theme_ui():

    # This is the ui for setting up themes.

    themes = []
    for i in os.listdir("themes"):
        if i.endswith(".json"):
            themes.append(i.replace(".json", ""))
    for i in os.listdir(get_settings_folder()+"themes"):
        if i.endswith(".json") and i.replace(".json", "") not in themes:
            themes.append(i.replace(".json", ""))

    d = {"categories":["Theme"],
         "size":[1],
         "data":[]}
    for i in themes:
        d["data"].append([i])
    table(d)
    center("Select Theme")

    # User selects a theme
    c = input(typing_dots())
    try:
        save("theme", themes[int(c)])
    except:
        save("theme", "default")

    center("Theme set to: "+get("theme"), "bdgr")
    set_theme(get("theme"))


def ui():

    # This will be the user interface for setting up setting.



    # user inputs the number
    to_text = True
    while True:

        with open(get_settings_folder()+"config.json") as f:
            data = json.load(f)

        d = {"categories":["name","value"],
             "size":[1,1],
             "data":[]}

        for i in data:
            d["data"].append([i, data[i]])
        table(d)

        center("")


        c = input(typing_dots("Type 'help' for more info", to_text))
        to_text = False
        if c == "help":
            markdown.draw("help/settings.md", "Settings help")
            c = input(typing_dots())

        try:
            c = int(c)
        except:
            break



        # If editing theme
        if list(data.keys())[c] == "theme":
            theme_ui()

        elif type(data[list(data.keys())[c]]) == bool:
            save(list(data.keys())[c], not data[list(data.keys())[c]])


        else:

            value = input(typing_dots("New Value for '"+list(data.keys())[c]+"'", to_add_dots=True))

            # If the user inputs a special python value like True or None we want to treat it as that value, not as a string
            try:
                value = ast.literal_eval(value)
            except:
                pass

            try:
                save(list(data.keys())[c], value)
            except Exception as e:
                center("Error saving setting: "+str(e), "bdrd")

def check_missing_keys():
    default = default_key_value_pairs

    for i in default:
        if not get(i):
            save(i, default[i])

def initial_settings_stuff(hist_file):
    settings_cache = get_all_settings()

    set_theme(settings_cache["theme"])

    if settings_cache["save_history"]:
        try:
            readline.read_history_file(hist_file)
        except:
            file = open(hist_file, "a")
            file.close()

    if settings_cache["autoconnect"]:
        connect.start()

    # A reminder for the devs to check to devs file
    if settings_cache["dev_mode"]:
        donate.check_devs_file()
