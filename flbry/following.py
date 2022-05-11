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

# Gets latest posts from subscriptions

from subprocess import *
import json
from flbry.variables import *
from flbry import url

def following():
    # Get the subscriptions
    following = check_output([flbry_globals["lbrynet"], "preference", "get"])
    try:
        following = json.loads(following)
    except:
        center("Connect to LBRY first.", "bdrd")
        return
    following = following["shared"]["value"]["subscriptions"]

    # Get enough results to fill the screen, then prompt user for more
    w, h = tsize()

    page_size = h - 5
    page = 1

    while True:
        command = [flbry_globals["lbrynet"], "claim", "search", "--page="+str(page), "--page_size="+str(page_size), "--order_by=release_time"]
        # Gets each channel's ID and add it to the command
        for i in following:
            i = i.split("#", 1)[1]
            command.append("--channel_ids="+i)

        out = check_output(command)
        out = json.loads(out)

        try:
            data_print = {"categories":["Type", "Channel", "Title"],
                            "size":[1,2,5],
                            "data":[]}

            # List what we found
            for n, i in enumerate(out["items"]):

                title = "---!Failed Loading Title---"
                ftype = "claim"
                channel = "[anonymous]"

                try:
                    try:
                        title = i["value"]["title"]
                    except:
                        title = i['name']

                    try:
                        ftype = what[i["value"]["stream_type"]]
                    except:
                        ftype = what[i["value_type"]]

                    try:
                        channel = i["signing_channel"]["value"]["title"]
                    except:
                        channel = i["signing_channel"]["normalized_name"]
                except:
                    pass


                data_print["data"].append([ftype, channel, title])

            table(data_print)
            # Tell the user that they might want to load more
            center("---type 'more' to load more---")
            page = page +1

        except Exception as e:
            if "code" in out:
                center("Error code: "+out["code"], "bdrd")
                if "message" in out:
                    center("Error: "+out["message"], "bdrd")
            else:
                center("Error: "+e, "bdrd")
            return

        while True:
            # Making sure that we stop every time a new page is reached
            c =  input(typing_dots())
            if c == "more":
                break

            try:
                c = int(c)
            except:
                return

            url.get(out["items"][c]["canonical_url"])

            # Print the list again
            table(data_print)
            center("---type 'more' to load more---")

def follow_channel(channel, name):
        # Get the shared preferences so they can be modified
        subscriptions = check_output([flbry_globals["lbrynet"], "preference", "get", "shared"])
        subscriptions = json.loads(subscriptions)["shared"]

        # If the channel is not in the subscriptions we add it
        if not channel in subscriptions["value"]["subscriptions"]:
            subscriptions["value"]["subscriptions"].append(channel)
            x = {"notificationsDisabled": True, "uri": channel}
            subscriptions["value"]["following"].append(x)

            x = check_output([flbry_globals["lbrynet"], "preference", "set", "shared", json.dumps(subscriptions)])

            center("Followed "+name, "bdgr")

        else:
            # Alert the user they're already subscribed
            center("Already following "+name, "bdrd")

def unfollow_channel(channel, name):
        # Get the shared preferences so they can be modified
        subscriptions = check_output([flbry_globals["lbrynet"], "preference", "get", "shared"])
        subscriptions = json.loads(subscriptions)["shared"]

        # If the channel is not in the subscriptions we add it
        if channel in subscriptions["value"]["subscriptions"]:
            subscriptions["value"]["subscriptions"].remove(channel)
            x = {"notificationsDisabled": True, "uri": channel}
            subscriptions["value"]["following"].remove(x)

            x = check_output([flbry_globals["lbrynet"], "preference", "set", "shared", json.dumps(subscriptions)])

            center("Unfollowed "+name, "bdgr")

        else:
            # Alert the user they're already subscribed
            center("Not following "+name, "bdrd")
