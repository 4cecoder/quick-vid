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

# This file will perform a simple search on the LBRY network.

from subprocess import *
import os
import json

from flbry import url
from flbry import following
from flbry import wallet
from flbry import markdown
from flbry import publish
from flbry import settings
from flbry import search
from flbry.variables import *

def simple(args=""):
    """Lists the publications of the given channel. If no channel is given it will prompt for this channel name"""

    # The user might write the search argument right in the same
    # line as the work search.
    #
    # : channel blenderdumbass
    #
    # Or they can type nothing. And be confused of what happened.
    # So I want to provide a catcher here. If they type nothing it
    # will ask them to provide a search query.

    if not args:
        args = input(typing_dots("Channel url"))
    if not args.startswith("@") and not args.startswith("lbry://@"):
        args = "@"+args

    # So we want to request a query to the SDK to search what ever
    # the user wants. The problem is it can be a very large output.
    # For example the "blender dumbass" query returns 1000 claims
    # on the LBRY network. And people will wait for a very long time
    # on something that might have a million claims.

    # So instead we are going to request only the first 20 and let
    # the user load more.

    w, h = tsize()

    page_size = h - 5
    page = 1

    while True:

        # Printing the search query and page number
        center("CHANNEL: "+args+" PAGE:"+str(page))


        out = check_output([flbry_globals["lbrynet"],
                         "claim", "search", '--channel='+args,
                         '--page='+str(page),
                         '--page_size='+str(page_size),
                            "--no_totals",
                            '--order_by=release_time'])

        # Now we want to parse the json

        try:
            out = json.loads(out)
        except:
            center("Connect to LBRY first.", "bdrd")
            return



        try:

            data_print = {"categories":["Type", "Title"],
                          "size":[1,5],
                          "data":[]}

            # List what we found
            for n, i in enumerate(out["items"]):

                title = "---!Failed Loading Title---"
                ftype = "claim"

                try:
                    try:
                        title = i["value"]["title"]
                    except:
                        title = i['name']

                    try:
                        ftype = what[i["value"]["stream_type"]]
                    except:
                        ftype = what[i["value_type"]]
                except:
                    pass


                data_print["data"].append([ftype, title])

            table(data_print)
            # Tell the user that they might want to load more
            center("---type 'more' to load more---")
            page = page +1

        # Error messages
        except Exception as e:
            if "code" in out:
                center("Error code: "+out["code"], "bdrd")
                if "message" in out:
                    center("Error: "+out["message"], "bdrd")
            else:
                center("Error: "+e, "bdrd")
            return

        channel_commands = [
            "rss",
            "follow",
            "unfollow",
            "more",
            "boost",
            "tip",
            "search"
        ]

        complete(channel_commands)

        try:
            signing_channel = out["items"][0]["signing_channel"]
        except:
            center("Channel '"+args+"' is not found.", "bdrd")
            return

        # Making sure that we stop every time a new page is reached
        while True:
            c =  input(typing_dots())
            reshow = False

            if c == "rss":
                rss = signing_channel["short_url"]
                rss = rss.replace("#", ":")
                rss = rss.split("lbry://", 1)[1]

                center("https://odysee.com/$/rss/"+rss)

            elif c == "follow":
                channel = signing_channel["permanent_url"]
                try:
                    name = signing_channel["value"]["title"]
                except:
                    name = signing_channel["signing_channel"]["normalized_name"]

                following.follow_channel(channel, name)

            elif c == "unfollow":
                channel = signing_channel["permanent_url"]
                try:
                    name = signing_channel["value"]["title"]
                except:
                    name = signing_channel["normalized_name"]

                following.unfollow_channel(channel, name)

            elif c.startswith("boost"):
                if " " in c:
                    wallet.support(signing_channel["claim_id"], amount=c[c.find(" ")+1:])
                else:
                    wallet.support(signing_channel["claim_id"])

                reshow = True

            elif c.startswith("tip"):
                if " " in c:
                    wallet.support(signing_channel["claim_id"], amount=c[c.find(" ")+1:], tip=True)
                else:
                    wallet.support(signing_channel["claim_id"], tip=True)

                reshow = True

            elif c.startswith("search"):
                channel = signing_channel["permanent_url"]

                if " " in c:
                    search.simple(c[c.find(" ")+1:], channel)
                else:
                    search.simple(channel=channel)

                reshow = True


            else:
                break

            complete(channel_commands)

            if reshow:
                table(data_print)
                center("---type 'more' to load more---")

        while True:
            # Making sure that we stop every time a new page is reached
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

            c =  input(typing_dots())

def select(message="", claim_id=False, anonymous=False):

    # This fucntion will give users to select one of their channels.
    center(message)

    out = check_output([flbry_globals["lbrynet"],
                         "channel", "list"])

    # Now we want to parse the json

    try:
        out = json.loads(out)
    except:
        center("Connect to LBRY first.", "bdrd")
        return

    d = {"categories":["lbry url", "title"],
         "size":[1,2],
         "data":[]}

    for n, i in enumerate(out["items"]):
        name = "[no name]"
        title = "[no title]"
        try:
            name = i["name"]
            title = i["value"]["title"]
        except:
            pass

        d["data"].append([name, title])


    if anonymous:
       d["data"].append(["[anonymous]", "[no title]"])
    table(d)
    center("select a channel by typing it's number")

    select = input(typing_dots())
    if not select:
        select = "0"
    try:
        select = int(select)
        if select > len(out["items"])-1 and anonymous:
            if claim_id:
                return None, None
            return None
        if claim_id:
            return out["items"][select]["name"], out["items"][select]["claim_id"]
        return out["items"][select]["name"]
    except:
        raise()
        if claim_id:
            return out["items"][0]["name"], out["items"][0]["claim_id"]
        return out["items"][0]["name"]

def show_data(data):
    # This will show the data for create()

    # If a value is not set, we set it to a default value
    if not "title" in data:
        title = "[no title]"
    else:
        title = data["title"]
    if not "description" in data:
        description = "[no description]"
    else:
        description = data["description"]

    d = {"categories": ["Name", "Bid", "Title", "Description"],
                        "size": [2,1,3,6],
                        "data": [[data["name"], data["bid"], title, description]]}

    table(d, False)

    if not "email" in data:
        email = "[no email]"
    else:
        email = data["email"]
    if not "website_url" in data:
        web_url = "[no website]"
    else:
        web_url = data["website_url"]

    d = {"categories": ["Email", "Website URL"],
                         "size": [1,1],
                         "data": [[email, web_url]]}

    table(d, False)

    if not "thumbnail_url" in data:
        thumb_url = "[no thumbnail]"
    else:
        thumb_url = data["thumbnail_url"]
    if not "cover_url" in data:
        cover_url = "[no cover image]"
    else:
        cover_url = data["cover_url"]

    d = {"categories": ["Thumbnail URL", "Cover Image URL"],
                         "size": [1,1],
                         "data": [[thumb_url, cover_url]]}

    table(d, False)

    if not "tags" in data:
        tags = "[no tags]"
    else:
        tags = data["tags"]

    d = {"categories":["Tags"],
            "size": [1],
            "data": [[tags]]}

    table(d, False)

    if not "languages" in data:
        langs = "[no languages]"
    else:
        langs = data["languages"]

    d = {"categories": ["Languages"],
            "size": [1],
            "data": [[langs]]}

    table(d, False)

    center("--- for commands type 'help' ---")

def create(name=""):
    """Creates a new channel on the LBRY network"""

    # Get the name for the channel, since it's required.
    # If the user just presses enter without typing anything, it will prompt again.
    while not name:
        name = input(typing_dots("Name"))

    if not name.startswith("@"):
        name = "@" + name

    # This is the data dictionary we will use
    data = {
        "bid": 0.001,
        "name": name
    }

    complete([
        "name",
        "bid",
        "title",
        "description",
        "email",
        "website",
        "thumbnail",
        "cover",
        "tags",
        "languages",
        "help",
        "save",
        "load",
        "create"
    ])

    editor = settings.get("default_editor")

    while True:
        show_data(data)

        c = input(typing_dots())
        if not c:
            return

        elif c.startswith("name"):
            if " " in c:
                name = c[c.find(" ")+1:]
            else:
                name = input(typing_dots("Name"))

            if not name.startswith("@"):
                name = "@" + name

            data["name"] = name

        elif c.startswith("bid"):
            # Get the bid
            if " " in c:
                bid = c[c.find(" ")+1:]
            else:
                bid = input(typing_dots("Bid"))

            # Try to convert it a float
            try:
                bid = float(bid)
            except:
                pass

            # while bid is not a float, repeat until it is
            while type(bid) != type(10.0):
                center("Bid is not a number, try again", "bdrd")
                bid = input(typing_dots("Bid"))
                try:
                    bid = float(bid)
                except:
                    pass

            data["bid"] = bid

        elif c.startswith("title"):
            if " " in c:
                title = c[c.find(" ")+1:]
            else:
                title = input(typing_dots("Title"))

            data["title"] = title

        elif c.startswith("description"):
            description = "Type the description here. Don't forget to save. Then return to FastLBRY."
            c = c + ' '
            a = c[c.find(" "):]
            if len(a) > 1:
                description = file_or_editor(a, description)
            else:
                if editor:
                    description = file_or_editor(a, description, editor)
                else:
                    description = input(typing_dots("Description"))

            data["description"] = description

        elif c.startswith("email"):
            if " " in c:
                email = c[c.find(" ")+1:]
            else:
                email = input(typing_dots("Email"))

            data["email"] = email

        elif c.startswith("website"):
            if " " in c:
                web_url = c[c.find(" ")+1:]
            else:
                web_url = input(typing_dots("Website URL"))

            data["website_url"] = web_url

        elif c.startswith("thumbnail"):
            if " " in c:
                thumb_url = c[c.find(" ")+1:]
            else:
                thumb_url = input(typing_dots("Thumbnail URL"))

            data["thumbnail_url"] = thumb_url

        elif c.startswith("cover"):
            if " " in c:
                cover_url = c[c.find(" ")+1:]
            else:
                cover_url = input(typing_dots("Cover URL"))

            data["cover_url"] = cover_url

        elif c.startswith("tags"):
            if " " in c:
                tags = c[c.find(" ")+1:]
            else:
                tags = input(typing_dots("Enter the tags, separated by commas", give_space=True))

            tags = tags.split(",")
            # Stip each tag, so if the user types "tag1, tag2, tag3"
            # Resulting list would be: ["tag1", "tag2", "tag3"]
            for n, tag in enumerate(tags):
                tags[n] = tag.strip()

            data["tags"] = tags

        elif c.startswith("languages"):
            if " " in c:
                langs = c[c.find(" ")+1:]
            else:
                langs = input(typing_dots("Enter the languages, separated by commas", give_space=True))

            langs = langs.split(",")
            for n, lang in enumerate(langs):
                langs[n] = lang.strip()

            data["languages"] = langs

        elif c == "help":
            markdown.draw("help/create-channel.md", "Create Channel Help")

        elif c.startswith("save"):
            if " " in c:
                pn = c[c.find(" ")+1:]
            else:
                pn = input(typing_dots("Preset Name"))

            # Create the preset folder is it's not there
            try:
                os.makedirs(settings.get_settings_folder()+"presets/channel")
            except:
                pass

            # Write the json file
            with open(settings.get_settings_folder()+"presets/channel/"+pn+'.json', 'w') as f:
                json.dump(data, f, indent=4, sort_keys=True)

        elif c.startswith("load"):
            if " " in c:
                pn = c[c.find(" ")+1:]
            else:
                pn = input(typing_dots("Preset Name"))

            # loading the json file
            try:
                name = data["name"]

                with open(settings.get_settings_folder()+"presets/channel/"+pn+'.json') as f:
                    data = json.load(f)

                data["name"] = name

            except:
                center("There is no '"+pn+"' preset!", "bdrd")

        elif c == "create":
            command = [flbry_globals["lbrynet"], "channel", "create", "--name="+data["name"], "--bid="+str(data["bid"])]

            for i in ["title", "description", "email", "website_url", "thumbnail_urL", "cover_url"]:
                if i in data:
                    command.append("--"+i+"="+str(data[i]))

            for i in ["tags", "languages"]:
                if i in data:
                    for j in data[i]:
                        command.append("--"+i+"="+str(j))

            out = check_output(command)
            out = json.loads(out)

            if "message" in out:
                center("Error creating channel: "+out["message"], "bdrd")
            else:
                center("Successfully created "+name, "bdgr")

            return

def sign(data: str = "", channel: str = "", message: str = "Channel to sign data with:", hexdata: str = ""):
    """
    Sign a string or hexdata and return the signatures

    Keyword arguments:
    data -- a string to sign
    channel -- channel name to sign with (e.g. "@example"). Will prompt for one if not given.
    message -- message to give when selecting a channel. Please pass this if not passing channel.
    hexdata -- direct hexadecimal data to sign
    """
    if (not data and not hexdata) or (data and hexdata):
        raise ValueError("Must give either data or hexdata")
    elif data:
        hexdata = data.encode().hex()

    if not channel:
        channel = select(message)

    if not channel.startswith("@"):
        channel = "@" + channel

    try:
        sigs = check_output([flbry_globals["lbrynet"],
                             "channel", "sign",
                             "--channel_name=" + channel,
                             "--hexdata=" + hexdata])
        sigs = json.loads(sigs)
        return sigs
    except:
        center("Connect to LBRY first.", "bdrd")
        return
