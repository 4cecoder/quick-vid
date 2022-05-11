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

# This file will fetch an LBRY URL directly and print out various
# options that the user may do with the publication.

from subprocess import *
import time
import json
import os
from flbry.variables import *
from flbry import markdown
from flbry import channel
from flbry import search
from flbry import comments
import urllib.request
from flbry import following
from flbry import settings
from flbry import wallet
from flbry import plugin
from flbry import channel
from flbry import analytics
import urllib.parse

def print_url_info(url, out):
    """Prints some information about the URL"""

    ##### NAME URL INFORMATION #####

    center("Publication Information")
    d = {"categories":["lbry url", "title"],
         "size":[1,1],
         "data":[[url]]}
    try:
        # This prints out the title
        d["data"][0].append(out["value"]["title"])
    except:
        d["data"][0] = [url]
        d["data"][0].append("[no title]")

    table(d, False)

    #### LICENSE ####

    try:
        dateis = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(int(out["value"]["release_time"])))
    except:
        dateis = "[Failed to load release date]"

    try:
        licenseis = out["value"]["license"]
    except:
        licenseis = "[Failed to load License]"

    d = {"categories":["License", "Release Date"],
         "size":[1,1],
         "data":[[licenseis, dateis]]}
    table(d, False)

    #### TAGS #####

    d = {"categories":[],
         "size":[],
         "data":[[]]}
    try:
        for tag in out["value"]["tags"]:
                    d["categories"].append(" ")
                    d["size"].append(1)
                    d["data"][0].append(tag)
    except:
        d = {"categories":[" "],
         "size":[1],
         "data":[["[no tags found]"]]}

    table(d, False)

    #### FILE INFO #####

    d = {"categories":["Value Type", "File Type", "File Size", "Duration"],
         "size":[1,1,1, 1],
         "data":[[]]}
    try:
         d["data"][0].append(what[out["value_type"]])
    except:
         d["data"][0].append("[no value type]")
    try:
         d["data"][0].append(out["value"]["source"]["media_type"])
    except:
         d["data"][0].append("[no file type]")
    try:
         d["data"][0].append(csize(out["value"]["source"]["size"]))
    except:
         d["data"][0].append("[no file size]")
    try:
         d["data"][0].append(timestring(float(out["value"]["video"]["duration"])))
    except:
         d["data"][0].append("[no duration]")


    table(d, False)

    ##### CHANNEL INFORMATION ####

    center("Channel Information")
    d = {"categories":["lbry url", "title"],
         "size":[1,1],
         "data":[[]]}

    try:
        # This prints out the title
        d["data"][0].append(out["signing_channel"]["name"])
        title = "[no title]"
        try:
            title = out["signing_channel"]["value"]["title"]
        except:
            pass
        d["data"][0].append(title)
    except:
        d["data"][0] = []
        d["data"][0].append("[no url]")
        d["data"][0].append("[anonymous publisher]")

    table(d, False)


    #### LBC INFORMATION ####

    center("LBRY Coin ( LBC ) Information")
    d = {"categories":["combined", "at upload", "support"],
         "size":[1,1,1],
         "data":[[]]}

    try:
        fullamount = float(out["amount"]) + float(out["meta"]["support_amount"])
        # This prints out the title
        d["data"][0].append(fullamount)
        d["data"][0].append(out["amount"])
        d["data"][0].append(out["meta"]["support_amount"])

    except:
        d["data"][0] = []
        d["data"][0].append("[no data]")
        d["data"][0].append("[no data]")
        d["data"][0].append("[no data]")

    table(d, False)

    #### PRICE ####

    try:
        # Print the prince of this publication in LBC
        center("PRICE: "+out["value"]["fee"]["amount"]+" "+out["value"]["fee"]["currency"], "bdrd", blink=True)

    except:
        pass



    # Some things are too big to output like this in the terminal
    # so for them I want the user to type a command.

    center("--- for publication commands list type 'help' --- ")

def get(url="", do_search=True):
    """Allows user to interact with the given URL"""

    # The user might type the word url and nothing else.

    if not url:
        url = input(typing_dots("LBRY url", give_space=True, to_add_dots=True))

    # Decode the URL to turn percent encoding into normal characters
    # Example: "%C3%A9" turns into "é"
    url = urllib.parse.unquote(url)

    ##### Converting an HTTPS domain ( of any website ) into lbry url ###

    # Any variation of this:
    # https://odysee.com/@blenderdumbass:f/hacking-fastlbry-live-with-you:6
    # customlbry.com/@blenderdumbass:f/hacking-fastlbry-live-with-you:6

    # Should become this:
    # lbry://@blenderdumbass:f/hacking-fastlbry-live-with-you:6

    if "/" in url and not url.startswith("@") and not url.startswith("lbry://"):
        if "@" in url:
            url = url[url.find("@"):]
        else:
            url = url[text.rfind("/")-1:]

        # Some web interfaces pass data through URLs using a '?'.
        # This is not valid for a LBRY URL, so we remove everything
        # after it to avoid errors.
        url = url.split("?")[0]

        url = "lbry://"+url


    # If a url looks like it might be a claim id, try to get the claim from it
    if len(url) == 40 and not url.startswith("lbry://"):
        x = check_output([flbry_globals["lbrynet"], "claim", "search", "--claim_id="+url])
        try:
            x = json.loads(x)
        except:
            center("Connect to LBRY first.", "bdrd")
            return

        if len(x["items"]) == 1:
            # If "items" has something in it we know it was a claim id
            out = x["items"][0]
            url = out["canonical_url"]

    else:
        # Let's fetch the url from our beloved SDK.

        out = check_output([flbry_globals["lbrynet"],
                            "resolve", url])

        # Now we want to parse the json

        try:
            out = json.loads(out)
        except:
            center("Connect to LBRY first.", "bdrd")
            return
        out = out[url]

    # In case there are plugins that want to modify resolved data.
    out = plugin.run(out)

    ### REPOST ####

    # Sometimes a user wants to select a repost. This will not
    # load anything of a value. A repost is an empty blob that
    # links to another blob. So I want to automatically load
    # the actuall publication it self here.

    if "value_type" in out and out["value_type"] == "repost":
        get(out["reposted_claim"]["canonical_url"])
        return

    #### FORCE SEARCH ###

    # Sometimes user might type something that is not a url
    # in this case ["value_type"] will not be loaded. And in
    # this case we can load search instead.

    if "value_type" not in out and do_search:
        search.simple(url)
        return out
    elif "value_type" not in out:
        return out

    # Now that we know that don't search for it. We can make
    # one thing less broken. Sometimes a user might type a
    # urls that's going to be resolved but that doesn't have
    # the lbry:// in the beginning of it. Like typing
    # @blenderdumbass instead of lbry://@blenderdumbass

    # I want to add the lbry:// to it anyway. So none of the
    # stuff later will break.

    if not url.startswith("lbry://"):
        url = "lbry://" + url

    print_url_info(url, out)

    # So we are going to start a new while loop here. IK crazy.
    # this one will handle all the commands associated with the
    # currently selected publication.

    # Completer thingy
    url_commands = [
        "help",
        "link",
        "id",
        "web",
        "description",
        "read",
        "channel",
        "comments",
        "reply",
        "open",
        "play",
        "music",
        "save",
        "rss",
        "thumbnail",
        "follow",
        "unfollow",
        "boost",
        "tip",
        "repost",
        "analytics",
        "sales"
    ]

    complete(url_commands)

    settings_cache = settings.get_all_settings()

    while True:
        plugin.run(execute=False)
        c =  input(typing_dots())

        # Some strings are only one line, so it's a waste to reprint the info.
        reprint = True

        # Some commands were changing url, which we don't want, so now
        # it uses a temporary variable instead.
        tmpurl = ""

        if not c:
            break

        elif c == "help":
            markdown.draw("help/url.md", "Publication Help")

        elif c == "web":
            print_web_instance(url)

        elif c == "link":
            center(url)
            reprint = False

        elif c == "id":
            center(out["claim_id"])
            reprint = False

        elif c.startswith("open"):

            # If open has an argument (like `open mpv`) it opens it in that
            # Next it tries to open it with the default opener
            # If neither of those find an opener, it prompts the user.
            if len(c) > 5:
                    p = c[5:]
            elif settings_cache["default_opener"]:
                    p = settings_cache["default_opener"]
            else:
                    p = input(typing_dots("Open in"))

            p = p.split()

            Popen([*p,
                   url.replace("lbry://", "https://spee.ch/").replace("#", ":").replace("(", "%28").replace(")", "%29")],
                              stdout=DEVNULL,
                              stderr=STDOUT)

        elif c == "description":
            # Here I want to print out the description of the publication.
            # but since, they are most likely in the markdown format I
            # need to implement a simple markdown parser. Oh wait.... I
            # have one. For the article read function. How about using it
            # here?

            # First we need to save the description into a file. Let's use
            # /tmp/ since there files are automatically cleaned up by the
            # system.

            try:
                savedes = open("/tmp/fastlbrylastdescription.md", "w")
                savedes.write(out["value"]["description"])
                savedes.close()
            except:
                savedes = open("/tmp/fastlbrylastdescription.md", "w")
                savedes.write("This file has no description.")
                savedes.close()

            # Now let's just simply load the markdown on this file.
            markdown.draw("/tmp/fastlbrylastdescription.md", "Description")


        elif c.startswith("play"):

            # Then we want to tell the SDK to start downloading.
            playout = check_output([flbry_globals["lbrynet"],
                                    "get", url, "--save_file=True"])
            # Parsing the JSON
            playout = json.loads(playout)

            # Same thing as in open
            if len(c) > 5:
                    p = c[5:]
            elif settings_cache["player"]:
                    p = settings_cache["player"]
            else:
                    p = input(typing_dots("Play in"))

            p = p.split()

            # Then we want to launch the player
            Popen([*p,
                   playout['download_path']],
                              stdout=DEVNULL,
                              stderr=STDOUT)

        elif c.startswith("music"):

            # Then we want to tell the SDK to start downloading.
            playout = check_output([flbry_globals["lbrynet"],
                                    "get", url])
            # Parsing the Json
            playout = json.loads(playout)

            # And again for music player
            if len(c) > 6:
                    p = c[6:]
            elif settings_cache["music_player"]:
                    p = settings_cache["music_player"]
            else:
                    p = input(typing_dots("Play in"))

            p = p.split()

            # Then we want to launch the player
            Popen([*p,
                   playout['download_path']],
                              stdout=DEVNULL,
                              stderr=STDOUT)

        elif c == "save":

            # Then we want to tell the SDK to start downloading.
            playout = check_output([flbry_globals["lbrynet"],
                                    "get", url, "--save_file=True"])
            # Parsing the Json
            playout = json.loads(playout)

            center("Saved to "+playout['download_path'])
            reprint = False

        elif c == "read":
            # Then we want to tell the SDK to start downloading.
            playout = check_output([flbry_globals["lbrynet"],
                                    "get", url, "--save_file=True"])
            # Parsing the Json
            playout = json.loads(playout)

            # Present the article to the user.
            markdown.draw(playout['download_path'], out["value"]["title"])

        elif c == "channel":

            # This a weird one. If the publication is a channel we
            # want it to list the publications by that channel.
            # If a publication is a publication. We want it to list
            # publications by the channel that made the publication.

            if out["value_type"] == "channel":
                channel.simple(url)
            else:
                try:
                    channel.simple(out["signing_channel"]["canonical_url"].replace("lbry://",""))
                except:
                    center("Publication is anonymous", "bdrd")

        elif c == "comments":
            comments.list(out["claim_id"], url)

        elif c.startswith("reply"):
            c = c + ' '
            comments.post(out["claim_id"], c[c.find(" "):])

        elif c == "rss":
            if out["value_type"] == "channel":
                tmpurl = out["short_url"].replace("#", ":")
                if tmpurl.startswith("lbry://"):
                    tmpurl = url.split("lbry://", 1)[1]
                center("https://odysee.com/$/rss/"+tmpurl)
            else:
                try:
                    tmpurl = out["signing_channel"]["short_url"].replace("#", ":")
                    tmpurl = tmpurl.split("lbry://", 1)[1]
                    center("https://odysee.com/$/rss/"+tmpurl)
                except:
                    center("Publication is anonymous!", "bdrd")

            reprint = False

        elif c == "thumbnail":
            try:
                thumb_url = out["value"]["thumbnail"]["url"]
                urllib.request.urlretrieve(thumb_url, "/tmp/fastlbrythumbnail")
                Popen(["xdg-open",
                        "/tmp/fastlbrythumbnail"],
                                stdout=DEVNULL,
                                stderr=STDOUT)
            except:
                center("Publication does not have a thumbnail", "bdrd")

        elif c == "follow":
            if out["value_type"] == "channel":
                try:
                    name = out["value"]["title"]
                except:
                    name = out["normalized_name"]

                tmpurl = out["permanent_url"]

                following.follow_channel(tmpurl, name)

            else:
                try:
                    try:
                        name = out["signing_channel"]["value"]["title"]
                    except:
                        name = out["signing_channel"]["normalized_name"]

                    tmpurl = out["signing_channel"]["permanent_url"]

                    following.follow_channel(tmpurl, name)
                except:
                    center("Publication is anonymous.", "bdrd")

        elif c == "unfollow":
            if out["value_type"] == "channel":
                try:
                    name = out["value"]["title"]
                except:
                    name = out["normalized_name"]

                tmpurl = out["permanent_url"]

                following.unfollow_channel(tmpurl, name)

            else:
                try:
                    try:
                        name = out["signing_channel"]["value"]["title"]
                    except:
                        name = out["signing_channel"]["normalized_name"]

                    tmpurl = out["signing_channel"]["permanent_url"]

                    following.unfollow_channel(tmpurl, name)
                except:
                    center("Publication is anonymous.", "bdrd")

        elif c.startswith("boost"):
            if " " in c:
                wallet.support(out["claim_id"], amount=c[c.find(" ")+1:])
            else:
                wallet.support(out["claim_id"])

        elif c.startswith("tip"):
            if " " in c:
                wallet.support(out["claim_id"], amount=c[c.find(" ")+1:], tip=True)
            else:
                wallet.support(out["claim_id"], tip=True)

        elif c.startswith("repost"):

            name = input(typing_dots("Name (enter for name of publication)", give_space=True))
            if not name:
                name = out["normalized_name"]

            a = c.split()
            try:
                bid = a[1]
            except:
                bid = input(typing_dots("Bid"))

            claim_id = out["claim_id"]
            ch, chid = channel.select("Channel to repost to:", True)

            repost_out = check_output([flbry_globals["lbrynet"], "stream", "repost", "--name="+name, "--bid="+bid, "--claim_id="+claim_id, "--channel_id="+chid])
            repost_out = json.loads(repost_out)


            if "message" in repost_out:
                center("Error reposting: "+repost_out["message"], "bdrd")
            else:
                center("Successfully reposted to "+ch, "bdgr")

        elif c == "sales":
            items = analytics.get_data(out["claim_id"])
            try:
                analytics.graph_loop(items)
            except Exception as e:
                print(e)

            print()

        elif c == "analytics":
            items = analytics.get_data(out["claim_id"], mode="analytics")
            try:
                analytics.graph_loop(items)
            except Exception as e:
                print(e)

            print()

        elif c:
            out = plugin.run(out, command=c)

        complete(url_commands)

        # Print the publication information again
        if reprint:
            print()
            print_url_info(url, out)
