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
import readline

from flbry import variables
from flbry.variables import *

# Make sure the config file exists and is up to date
from flbry import settings
settings.check_config()
settings.check_missing_keys()

# Do some things with the settings
hist_file = settings.get_settings_folder()+"terminal-history"
settings.initial_settings_stuff(hist_file)

# A welcome logo.
logo()

# Here I want to make a simple check for an operating system
# The software is built to work on GNU / Linux so I need to
# check whether the user runs it on a proper system. If not
# give them a warning message.

import platform
if platform.system() != "Linux": # IK It should be GNU / Linux
    center("OS "+platform.system().upper()+" NOT SUPPORTED!", "bdrd", True)
    center("Type 'osinfo' to learn more.", "bdrd")


# Importing all kinds of other things needed for the operations
from flbry import connect
from flbry import search
from flbry import channel
from flbry import wallet
from flbry import uploads
from flbry import list_files
from flbry import following
from flbry import markdown
from flbry import trending
from flbry import url
from flbry import publish
from flbry import comments
from flbry import donate
from flbry import plugin
from flbry import analytics

# Now we gonna start the main loop. It will give the user to input
# any function. And when the function is executed, it will give it
# again. Forever. Until the user exits.

# List of commands for autocomplete feature.

main_commands = [
    "exit",
    "quit",
    "help",
    "osinfo",
    "matrix",
    "clear",
    "repository",
    "report",
    "license",
    "connect",
    "disconnect",
    "publish",
    "history",
    "search",
    "channels",
    "channel",
    "trending",
    "articles",
    "login",
    "wallet",
    "balance",
    "inbox",
    "uploads",
    "following",
    "subscriptions",
    "install",
    "install_force",
    "settings",
    "addresses",
    "send",
    "donations_test",
    "donations_diff",
    "donations_update",
    "donations_add",
    "donate",
    "create-channel",
    "plugins",
    "get_plugin",
    "sales",
    "analytics",
    "readme",
    "total_sales",
    "total_analytics",
    "load_graph"
]

complete(main_commands)


def main():
    to_text = True
    while True:
        # Set the global variables
        variables.flbry_globals["lbrynet"] = settings.get("lbrynet_binary")
        variables.flbry_globals["comment_api"] = settings.get("comment_api")

        plugin.run(address="main") # adding all the commands from plugins
        command = input(typing_dots("Type 'help' for more info.", to_text)) # the : will be the presented function
        to_text = False

        if command == "exit":
            connect.stop()
            break # breaks the while True: loop

        elif command == "quit":
            center("Quit does not disconnect the SDK!", "bdrd")
            center("To disconnect use 'exit' or 'disconnect'.")
            break

        elif command == "help":
            markdown.draw("help/main.md", "Help")

        elif command == "readme":
            markdown.draw("README.md", "Readme")

        elif command == "osinfo":
            markdown.draw("help/os.md", "Operating System Information")


        # HELP AND CONTRIBUTION FUNCTIONS

        elif command == "matrix":
            center("#FastLBRY:matrix.org")

        elif command == "clear":
            os.system("clear")

        elif command == "repository":
            center("https://notabug.org/jyamihud/FastLBRY-terminal")

        elif command == "report":
            try_getting_git_commit()
            center("Report issues here: https://notabug.org/jyamihud/FastLBRY-terminal/issues")

        elif command == "license":
           markdown.draw("LICENSE.md", "License (GPLv3 or later)")

        # LBRY COMMANDS

        elif command == "connect":
            connect.start()

        elif command == "disconnect":
            connect.stop()

        elif command.startswith("publish"):
            if " " in command:
                publish.configure(command[command.find(" ")+1:])
            else:
                publish.configure()

        elif command == "history":
            list_files.downloaded()

        elif command.startswith("search"):
            if " " in command:
                search.simple(command[command.find(" ")+1:])
            else:
                search.simple()

        elif command == "channels":
            channel.simple(channel.select())

        elif command.startswith("channel"):
            if " " in command:
                channel.simple(command[command.find(" ")+1:])
            else:
                channel.simple()

        elif command.startswith("trending"):
            trending.simple()

        elif command.startswith("articles"):
            trending.simple(articles=True)
        elif command in ("following", "subscriptions"):
            following.following()

        ###### WALLET ######

        elif command == "login":
            markdown.draw("help/login.md", "Login Help")

        elif command == "wallet":
            wallet.history()

        elif command == "balance":
            wallet.balance()

        elif command.startswith("inbox"):
            if " " in command:
                comments.inbox(command[command.find(" ")+1:])
            else:
                comments.inbox()

        elif command == "uploads":
            uploads.simple()

        elif command == "install":
            settings.install_desktop(False)

        elif command == "install_force":
            settings.install_desktop(True)

        elif command == "settings":
            settings.ui()

        elif command == "addresses":
            wallet.addresses()

        elif command == "send":
            wallet.address_send()

        elif command == "donations_update":
            donate.check_devs_file(save_changes=True)

        elif command == "donations_test":
            donate.check_devs_file(user_check=True)

        elif command == "donations_diff":
            donate.check_devs_file(user_check=True, diff=True)

        elif command == "donations_add":
            donate.add()

        elif command == "donate":
            donate.donate()

        elif command == "sales":
            analytics.sales()

        elif command == "analytics":
            analytics.sales("analytics")

        elif command.startswith("create-channel"):
            if " " in command:
                channel.create(command[command.find(" ")+1:])
            else:
                channel.create()

        elif command.startswith("plugins"):
            if " " in command:
                plugin.manager(command[command.find(" ")+1:])
            else:
                plugin.manager()

        elif command.startswith("get_plugin"):
            if " " in command:
                plugin.get_plugin(command[command.find(" ")+1:])
            else:
                plugin.get_plugin()

        elif command == "total_sales":
            items = analytics.get_data()
            try:
                analytics.graph_loop(items)
            except Exception as e:
                print(e)

            print()

        elif command == "total_analytics":
            items = analytics.get_data(mode="analytics")
            try:
                analytics.graph_loop(items)
            except Exception as e:
                print(e)

            print()
        elif command == "load_graph":
            analytics.load_graph_from_file()
        
        # If a user types anything ELSE, except just simply pressing
        # Enter. So if any text is in the command, but non of the
        # above were activated.

        # Here I want to just run the URL module and try to resolve
        # the url. The Url module will need to be able to handle a
        # lot of it.

        elif command:
            command = plugin.run(command, command, "main")

            if command:
                url.get(command)

        # Restore the commands completion
        complete(main_commands)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        center("Ctrl-C does not disconnect the SDK!", "bdrd")
        center("To disconnect use 'exit' or 'disconnect'.")
    finally:
        # Save history on exit
        if settings.get("save_history"):
            try:
                readline.write_history_file(hist_file)
            except Exception as e:
                center("Error writing history: "+str(e), "bdrd")

