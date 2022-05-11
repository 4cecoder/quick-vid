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

# This file will be dealing with handling extensions aka plugins.

import inspect
import hashlib
import json
import sys
import os
import re
import urllib.request

from flbry import settings
from flbry.variables import *
from flbry import markdown
from flbry import publish

from subprocess import *

def get_pluginignore():
    """Returns a list containing the parsed pluginignore file from the FastLBRY settings directory

    The pluginignore file is a list of regex strings for plugins that should be ignored.
    Lines beginning with a '#' are comments. To start a regex string with a '#', use '\#' instead.
    """

    # Read the pluginignore file if it exists
    plugin_ignore = settings.get_settings_folder() + "pluginignore"
    if os.path.exists(plugin_ignore):
        with open(plugin_ignore) as f:
            plig = f.readlines()

        # Remove comments and replace escaped number signs with unescaped ones
        plugin_ignore = []
        for expression in plig:
            expression = expression.strip()
            if not expression.startswith("#"):
                if expression.startswith("\#"):
                    expression = expression.replace("\#", "#", 1)

                plugin_ignore.append(expression)

    else:
        plugin_ignore = []

    return plugin_ignore

def ignore_plugin(plugin, plugin_ignore):
    """Return whether a plugin is in a list of regular expressions"""
    for expression in plugin_ignore:
        if re.fullmatch(expression, plugin):
            return True
    return False

def run(args=[], command=False, address=None, execute=True, run_only=None):

    # This function will pass arguments to the plugin function.
    # The plugin will edit those arguments and return them back.
    # This is when we return those arguments back to the function
    # from where the plugin.run() was called.

    # To make it so anybody could extend any part of the software
    # without adding new paths to things inside the software code,
    # we are going to use an address of the function.

    # So for example from 'flbry' you've imported 'markdown' and
    # now it runs the Open() function. If inside that function we
    # will add plugin.run(), the resulting function address will be
    # 'flbry.markdwon.Open'

    # This is how we get the address:
    if not address:
        address = inspect.stack()[1].filename
        address = address.replace(os.getcwd(), "").replace(".py", "")
        address = address.replace("/",".")[1:]
        address = address +"."+ inspect.stack()[1].function


    # Now we want to get files from the plugins folder.
    plugins_folder = settings.get_settings_folder("flbry/plugins/")
    sys.path.append(settings.get_settings_folder())

    # Before we import we need to make sure that __init__.py exists
    # this is an empty file that will tell python that this folder is
    # indeed a module.
    if not os.path.exists(plugins_folder+"__init__.py"):
        t = open(plugins_folder+"__init__.py", "w")
        t.close()

    plugin_ignore = get_pluginignore()

    # Now let's import the files from plugins
    for p in os.listdir(plugins_folder):
        m = p[:-3]

        # If only a certain plugin is to run
        if run_only and m != run_only:
            continue


        # Ignore the __init__.py
        if m == "__init__":
            continue

        if ignore_plugin(m, plugin_ignore):
            continue

        if p.endswith(".py") and enabled(m):

            exec("from plugins import "+m)

            # Let's get the plugin_data of the plugin
            try:
                plugin_data = eval(m+".plugin_data")
            except:
                continue

            # Now let's update the data of the plugin_data
            # into the info of the plugin settings.
            plugin_info = {}
            for i in plugin_data:
                if i != "functions":
                    plugin_info[i] = plugin_data[i]

            enabled(m, plugin_info=plugin_info)

            # Now that we have it let's compare it to the
            # address of the function from which it's running
            for func in plugin_data["functions"]:
                if address in func and not command and not func["command"] and execute:
                    args = func[address](args)
                elif address in func and command and command.startswith(func["command"]) and execute:
                    args = func[address](command, args)

                # Adding functions into completer
                if address in func and func["command"]:
                    complete([func["command"]], add=True)

        # If we run only one plugin and the plugin is disabled.
        elif run_only and run_only == m:
            center("Plugin '"+m+"' is disabled!", "bdrd")

    return args

def check_settings_exists():
    """Ensures that ~/.local/share/flbry/plugins.json exits"""

    if not os.path.exists(settings.get_settings_folder()+"plugins.json"):
        with open(settings.get_settings_folder()+"plugins.json", 'w') as f:
                json.dump({}, f, indent=4, sort_keys=True)



def enabled(plugin_name, full_report=False, flip=False, plugin_info={}):
    """Checks whether a plugin is enabled in plugin settings."""

    # Firs let's make sure that the file exist
    check_settings_exists()

    # Then let's open the file

    with open(settings.get_settings_folder()+"plugins.json") as f:
            data = json.load(f)


    # Adding a missing plugin
    default = {"active":False,
               "info":{"title":plugin_name,
                       "author":None,
                       "license":None,
                       "flbry":"terminal",
                       "description":None}}

    # Ignore plugins
    plugin_ignore = get_pluginignore()
    if ignore_plugin(plugin_name, plugin_ignore):
        return False

    if plugin_name not in data:
        data[plugin_name] = default

    # Overwriting
    if flip:
        data[plugin_name]["active"] = not data[plugin_name]["active"]

    # Updating info
    if plugin_info:
        data[plugin_name]["info"] = plugin_info

    # Saving plugins file
    with open(settings.get_settings_folder()+"plugins.json", 'w') as f:
                json.dump(data, f, indent=4, sort_keys=True)

    # Returning data
    if full_report:
        return data[plugin_name]
    else:
        return data[plugin_name]["active"]

def manager(search=""):
    """Gives a settings prompt to set various settings on plugins."""

    to_text = True

    plugins_commands = [
        "help",
        "read",
        "set",
        "publish",
        "description"

    ]

    while True:

        complete(plugins_commands)
        print()

        check_settings_exists()
        with open(settings.get_settings_folder()+"plugins.json") as f:
                data = json.load(f)

        data = run(data) # Updating the plugins

        d = {"categories":["Active", "Title", "Author", "License"],
             "size":[1, 3, 2, 2],
             "data":[]}

        plugin_ignore = get_pluginignore()

        for plugin in data:
            # Don't show ignored plugins
            if ignore_plugin(plugin, plugin_ignore):
                continue

            # Make sure you can get the nessesary data
            # even if it's somewhat corrupted.

            active = "[ ]"
            title = plugin
            description = ""
            LICENSE = ""
            author = ""
            try:
                active = data[plugin]["active"]
            except:
                pass
            try:
                if data[plugin]["info"]["title"]:
                    title = data[plugin]["info"]["title"]
            except:
                pass
            try:
                if data[plugin]["info"]["description"]:
                    description = data[plugin]["info"]["description"]
            except:
                pass
            try:
                if data[plugin]["info"]["license"]:
                    LICENSE = data[plugin]["info"]["license"]
            except:
                pass
            try:
                if data[plugin]["info"]["author"]:
                    author = data[plugin]["info"]["author"]
            except:
                pass

            # Make so the search works.
            if search and \
             search.lower() not in title.lower() \
             and search.lower() not in author.lower() \
             and search.lower() not in description.lower() \
             and search.lower() not in LICENSE.lower():
                continue

            # Let's add the plugin into the data
            d["data"].append([active, title, author, LICENSE])

        table(d)
        center("")

        # Now let's start the madness

        print()
        c = input(typing_dots("Type 'help' for more info.", to_text))
        to_text = False

        if not c:
            break

        try:
            c = int(c)
            enabled(list(data.keys())[c], flip=True)
            continue
        except:
            pass

        if c.startswith("description"):

            cn = get_cn(c, "Which plugin?")

            try:
                description = list(data.values())[cn]["info"]["description"]
                savedes = open("/tmp/fastlbrylastdescription.md", "w")
                savedes.write(description)
                savedes.close()
                markdown.draw("/tmp/fastlbrylastdescription.md", "Description")
            except:

                center("This plugin has no description.")

        elif c.startswith("read"):

            cn = get_cn(c, "Which plugin?")

            try:

                plugin_name = list(data.keys())[cn]
                plugin_file = settings.get_settings_folder("flbry/plugins/")+plugin_name+".py"
                markdown.draw(plugin_file, plugin_name+" Source Code", False)
            except:
                center("Plugin is deleted or corrupted", "bdrd")

        elif c.startswith("set"):

            cn = get_cn(c, "Which plugin?")

            run([None], address="settings", run_only=list(data.keys())[cn])

        elif c.startswith("publish"):

            cn = get_cn(c, "Which plugin?")

            try:
                plugin_name = list(data.keys())[cn]
                plugin_file = settings.get_settings_folder("flbry/plugins/")+plugin_name+".py"
                publish_plugin(plugin_file, list(data.values())[cn]["info"])
            except:
                center("Plugin is deleted or corrupted", "bdrd")

        elif c == "help":
            markdown.draw("help/plugins.md", "Plugins Help")

def publish_plugin(filename, info):
    """Helps the user publish a plugin"""

    print()

    # Check if the plugin has a license in the info and get the name and link to it
    # Getting the link only works if the license it a SPDX Lincense Identifier: https://spdx.org/licenses/
    if "license" in info:
        l = spdx_license(info["license"])
        if "link" in l:
            info["license_url"] = l["link"]
        info["license_name"] = l["name"]
        info.pop("license")

    info["file"] = filename

    if not "version" in info:
        info["version"] = 1.0

    if not "fee" in info:
        info["fee"] = 0

    to_text = True

    publish_commands = [
        "help",
        "file",
        "link",
        "title",
        "author",
        "license",
        "description",
        "publish",
        "fastlbry",
        "version",
        "fee",
        "publish_file"
    ]

    editor = settings.get("default_editor")

    while True:
        complete(publish_commands)

        if "license_name" in info:
            d_license = info["license_name"]
        elif "license" in info:
            d_license = info["license"]
        else:
            d_license = "[no license]"

        d = {"categories":[ "Title", "Version", "Fee", "Author", "License"],
             "size":[ 3, 1, 1, 2, 2],
             "data":[[
                 info["title"],
                 info["version"],
                 str(info["fee"]),
                 info["author"],
                 d_license
             ]]}

        table(d, False)

        if not "description" in info:
            info["description"] = ""

        d = {"categories": ["Description"],
                "size": [1],
                "data": [[info["description"]]]}

        table(d, False)

        d = {"categories": ["File or Link", "FastLBRY Variant"],
                "size": [3, 1],
                "data": [[info["file"], info["flbry"]]]}

        table(d, False)
        center("")

        c = input(typing_dots("Type 'help' for more info.", to_text, give_space=True))
        to_text = False

        if not c:
            break

        elif c == "publish_file":

            try:
                info["file"] = publish.configure(info["file"])['outputs'][0]['permanent_url']
            except Exception as e:
                center("Error: "+str(e), "bdrd")


        elif c.startswith(("file", "link")):
            if " " in c:
                info["file"] = c[c.find(" ")+1:]
            else:
                info["file"] = input(typing_dots("File or URL", give_space=True, to_add_dots=True))


        elif c.startswith("title"):
            if " " in c:
                info["title"] = c[c.find(" ")+1:]
            else:
                info["title"] = input(typing_dots("Plugin title", give_space=True, to_add_dots=True))

        elif c.startswith("author"):
            if " " in c:
                info["author"] = c[c.find(" ")+1:]
            else:
                info["author"] = input(typing_dots("Author", give_space=True, to_add_dots=True))

        elif c == "license":
            info.pop("license", None)
            info["license_name"], info["license_url"] = choose_license()

        elif c.startswith("description"):
            description = "Type the description here. Don't forget to save. Then return to FastLBRY."
            c = c + ' '
            a = c[c.find(" "):]
            if len(a) > 1:
                info["description"] = file_or_editor(a, description)
            else:
                if editor:
                    description = file_or_editor(args, desciption, editor)
                else:
                    info["description"] = input(typing_dots("Description", give_space=True, to_add_dots=True))

        elif c.startswith("version"):
            if " " in c:
                info["version"] = c[c.find(" ")+1:]
            else:
                info["version"] = input(typing_dots("Version number", give_space=True, to_add_dots=True))

        elif c.startswith("fee"):
            if " " in c:
                info["fee"] = c[c.find(" ")+1:]
            else:
                info["fee"] = input(typing_dots("Fee", give_space=True, to_add_dots=True))

        elif c.startswith("fastlbry"):
            if " " in c:
                info["flbry"] = c[c.find(" ")+1:]
            else:
                complete(["terminal", "gtk", "all"])
                info["flbry"] = input(typing_dots("FastLBRY variant", give_space=True, to_add_dots=True))

        elif c == "publish":
            try:
                x = publish_plugin_blob(info["file"], info)
                if x:
                    return
            except Exception as e:
                center("Error publishing plugin: "+str(e), "bdrd")

        elif c == "help":
            markdown.draw("help/publish_plugins.md", "Plugin Publishing Help")

def publish_plugin_blob(filename, info):
    """Creates and publishes blobs for FastLBRY plugins.

    Arguments:
    filename -- the filename of the work to be published. This can be an HTTP(S) or LBRY URL to the file.
    info -- a dictionary of info about the file including:
        file -- the filename of the work. Equivilent to filename.
        title -- the title of the work.
        license_name -- the name of the license the work can be copied under.
        license_url (optional) -- the URL of the license the work can be copied under.
        description (optional) -- a description of the work.
        fee (optional) -- the fee that will be charged for the work. This is ignored if the filename is a URL.
    """


    filename = os.path.expanduser(filename)

    # Just in case it does not have a fee
    if not "fee" in info:
        info["fee"] = 0

    # Try to open the file and if that fails treat it as a URL
    try:
        pf = open(filename, "rb")
    except FileNotFoundError:
        if filename.startswith("lbry://"):
            filename = filename.replace("lbry://", "https://spee.ch/")

        try:
            pf = urllib.request.urlopen(filename)
            if not info["fee"] in [0, "0"]:
                center("Plugin file is a link, fee will be ignored", "bdrd")
        except urllib.error.URLError:
            center("File is not a valid file or URL", "bdrd")
            return

    # We need a hash of the file for security reasons
    pf = pf.read()

    sha512 = hashlib.sha512(pf).hexdigest()
    info["sha512"] = sha512

    # Try to upload the plugin to LBRY
    info["file"] = publish.speech_upload(info["file"], name=sha512, fee=info["fee"], speech=False)

    # Saving it to json for publishing
    with open('/tmp/flbrypublishpluginblob.json', 'w') as f:
                json.dump(info, f, indent=4, sort_keys=True)

    data = {"name":info["title"],
            "bid":0.001,
            "file_path":'/tmp/flbrypublishpluginblob.json',
            "title":info["title"],
            "license":info["license_name"],
            "thumbnail_url":"",
            "channel_id":"",
            "channel_name":"",
            "fee_amount":0,
            "tags":["FastLBRY-terminal-plugin-blob-json-file"]
        }

    if "description" in info:
        data["description"] = info["description"]

    if "license_url" in info:
        data["license_url"] = info["license_url"],

    publish.configure('/tmp/flbrypublishpluginblob.json', data)
    return True

def get_plugin(search=""):

    """Searches and installs plugins."""
    # ^ I hate this syntax, but alright. :|

    w, h = tsize()

    page_size = h - 5
    page = 1

    while True:

        # Since it's plugins and we will need to read each of their
        # blob data file. It's gonna require a ratehr more combersome
        # way of dealing with it.

        # We will need to show a progress bar each time
        print()
        progress_bar(0, page_size, "Searching plugins...")

        args = [flbry_globals["lbrynet"], "claim", "search",
                "--any_tags=FastLBRY-terminal-plugin-blob-json-file", # Block tag.
                "--fee_amount=0", # Blobs should be gratis, since we will download them asap
                '--page='+str(page),
                '--page_size='+str(page_size),
                "--no_totals",
                '--order_by=release_time']
        if search:
            args.append('--text="'+search+'"')


        out = check_output(args)
        try:
            out = json.loads(out)["items"]
        except:
            center("Connect to LBRY first.", "bdrd")
            return


        # We gonna download the blob for each plugin and read it
        # right away.

        data_print = {"categories":["Author", "Plugin Name", "Version", "Price", "License"],
                          "size":[1,4,1,1,4],
                          "data":[]}

        for n, plugin in enumerate(out):
            name = plugin["name"]
            try:
                name = plugin["value"]["title"]
            except:
                pass
            progress_bar(n+1, len(out), "Loading "+name+"...")
            try:
                blob = check_output([flbry_globals["lbrynet"], "get", plugin["permanent_url"],
                                 "--file_name=flbrypluginblob.json", # How to call
                                 "--download_directory=/tmp"])       # Where to save
                with open("/tmp/flbrypluginblob.json") as f:
                    blob = json.load(f)
            except:
                continue

            # Now that we have the blob, let's show the data

            author = "[no author]"
            try:
                author = blob["author"]
            except:
                pass
            title = "[no title]"
            try:
                title = blob["title"]
            except:
                pass
            version = 0.0
            try:
                version = blob["version"]
            except:
                pass
            fee = "Gratis"
            try:
                # The problem is, the fee should be of a file, not of
                # what ever is in the blob.
                fee = blob["fee"]
            except:
                pass
            license_is = False
            try:
                license_is = blob["license_name"]
            except:
                pass

            data_print["data"].append([author, title, version, fee, license_is])

            # TODO: Make it work. I'm tired and I don't understand what to come next.

        print()
        table(data_print)
        center("")
        return
