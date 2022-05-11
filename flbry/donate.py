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

# This file will handle donations and things related to it.

import os
import json
import math
from flbry.variables import *
from flbry import channel
from subprocess import *

def check_devs_file(save_changes=False, user_check=False, diff=False):

    # This will check the devs file for being up to date
    # It will notify the developers ( and also users ) about
    # the need to update the file.

    # Getting data about commits from git
    try:
        git_response = check_output(["git", "shortlog", "-sn", "--no-merges", "--max-count=100", "-e"])
        git_response = git_response.decode("utf-8")
        git_response = git_response.split("\n")
    except:
        center("Git is not installed.", "bdrd")
        return

    # Getting the file for those who have not installed git
    try:
        with open("devs.json") as f:
            devs_data = json.load(f)
    except:
        center("'devs.json' is missing!", "bdrd")
        return


    # Parsing the git response and comparing it to devs.json
    changed = False
    devs = {}
    for i in git_response:
        s = i.split("\t")
        if s[0]:
            commits = int(s[0])
            devname = s[1]
            if "<" in devname: # if user allows email address
                devname = devname[devname.find("<")+1:devname.find(">")]

            if devname not in devs:
                devs[devname] = commits
            else:
                devs[devname] += commits

    for devname in devs:
        commits = devs[devname]
        if devname in devs_data:
            if commits != devs_data[devname]["commits"]:
                if diff:
                    center(devname+" new commits "+str(commits - devs_data[devname]["commits"]))
                devs_data[devname]["commits"] = commits
                changed = True

        else:
            lbry = ""
            if save_changes:
                center("New Developer Found '"+devname+"'")
                lbry = input(typing_dots("Developers LBRY link", give_space=True))
            if diff:
                center("New Developer Found '"+devname+"'")
            devs_data[devname] = {"commits":commits, "lbry":lbry}

    # Filtering out zeros
    for i in devs_data:
        if i not in devs and devs_data[i]["commits"]:
            changed = True
            if diff:
                center(i+" no recent commits")
            devs_data[i]["commits"] = 0

    # Output if changed
    if not save_changes and changed:
        if not diff:
            center("Developers Donation Data 'devs.json' is outdated!", "bdrd")
    elif user_check:
        center("Developers Donation Data 'devs.json' is alright!", "bdgr")

    # Save
    elif save_changes:
        with open("devs.json", 'w') as f:
                json.dump(devs_data, f, indent=4, sort_keys=True)
        if changed:
            center("Developers Donation Data 'devs.json' is updated!", "bdgr")
        else:
            center("Developers Donation Data 'devs.json' didn't need updating.", "bdgr")

def add():

    # This function will add a new user into the devs.json

    try:
        with open("devs.json") as f:
            devs_data = json.load(f)
    except:
        raise()
        center("'devs.json' is missing!", "bdrd")
        return

    devname = input(typing_dots("Git Email"), give_space=True)
    commits = 0
    lbrylink = input(typing_dots("LBRY Link to Transfer Support", give_space=True))

    devs_data[devname] = {"commits":commits, "lbry":lbrylink}

    with open("devs.json", 'w') as f:
                json.dump(devs_data, f, indent=4, sort_keys=True)
    center("Developers Donation Data 'devs.json' is updated!", "bdgr")

def donate():

    # This is going to be the funtiona to auto-donate fractions
    # of your wealth to the people that contribute to the project.

    # First we need to show the user the amount he has.
    balance = check_output([flbry_globals["lbrynet"],
                         "wallet", "balance"])
    try:
        balance = json.loads(balance)
    except:
        center("Connect to LBRY first.", "bdrd")
        return


    available = float(balance["available"])

    center("You have "+str(available)+" LBC available to Donate.")

    # Now let's ask the user how mush they want to donate.
    amount = input(typing_dots("How much to donate?"))
    try:
        amount = float(amount)
    except:
        center("Amount should be a number!", "bdrd")
        return

    if amount > available:
        center("You don't have so much available!", "bdrd")
        return

    # Now let's get out data
    check_devs_file()

    try:
        with open("devs.json") as f:
            devs_data = json.load(f)
    except:
        raise()
        center("'devs.json' is missing!", "bdrd")
        return

    # Now let's make the math
    predevs = []
    sumoflogs = 0
    for devname in devs_data:
        if devs_data[devname]["lbry"] and devs_data[devname]["commits"]:
            devs_log = math.log1p(devs_data[devname]["commits"])
            sumoflogs = sumoflogs + devs_log
            predevs.append([devs_data[devname]["lbry"].replace("lbry://", ""), devs_log])
    devs = []
    for dev in predevs:
        devs.append([dev[0], round(amount/sumoflogs*dev[1], 8)])

    while True:
        d = {"categories":["Developer's Address", "Sending LBC"],
             "size":[2,1],
             "data":devs}
        table(d)

        center("Type 'donate' to proceed, or select a number to modify.")


        c = input(typing_dots())
        if not c:
            return
        elif c == "donate":
            break

        try:
            c = int(c)
            devs[c]
        except:
            return

        new_amount = input(typing_dots("New Donate Amount for "+devs[c][0]))
        try:
            new_amount = float(new_amount)
        except:
            new_amount = 0
        if new_amount:
            devs[c] = [devs[c][0], new_amount]


    # Ask the user for a channel
    post_as, from_channel = channel.select("Donate as:", claim_id=True, anonymous=True)

    # If the user gets to here it's donation time.
    print()
    progress_bar(0, len(devs)+1, "Resolving Donation Urls...")

    resolve = [flbry_globals["lbrynet"],"resolve"]
    for dev in devs:
        resolve.append(dev[0])

    resolve = check_output(resolve)
    try:
        resolve = json.loads(resolve)
    except:
        return

    errors = []
    for n, dev in enumerate(devs):
        progress_bar(n+1, len(devs)+2, "Sending "+str(dev[1])+" to "+dev[0])

        try:
            claim_id = resolve[dev[0]]["claim_id"]
            support_command = [flbry_globals["lbrynet"],
                     "support",
                     "create",
                     "--claim_id="+claim_id,
                     "--amount="+str(dev[1]),
                          "--tip"]
            if from_channel:
                support_command.append("--channel_id="+from_channel)
            test = check_output(support_command)
            #print(test)
        except Exception as e:
            errors.append([dev[0],str(e)])

    # Reporting donation to the team ( aka sending a comment to @FastLBRY:f )
    if post_as:
        progress_bar(len(devs)+1, len(devs)+2, "Commenting on @FastLBRY:f about this...")
        text = "Just **donated** "+str(amount)+" LBC to FastLBRY contributors by typing `donate` in [FastLBRY - Terminal](https://notabug.org/jyamihud/FastLBRY-terminal).\n"
        for dev in devs:
            text = text + "\n - **"+str(dev[0]).replace("lbry://", "")+"** got `"+str(dev[1])+"` LBC from me."

        post_comment = [flbry_globals["lbrynet"],
                             "comment", "create",
                            text,
                            '--claim_id=fb4db67b2a79396f4ba0a52a12e503d0a736f307']
        post_comment.append('--channel_name='+post_as)

        check_output(post_comment)

    # Finishing
    progress_bar(len(devs)+2, len(devs)+2, "Done!")
    print()

    if errors:
        center("","bdrd")
        d = {"categories":["Developer's Address", "Error"],
             "size":[1,1],
             "data":errors}
        table(d)
        center("","bdrd")
