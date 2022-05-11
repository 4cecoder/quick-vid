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

# This file will publish a selected file into LBRY Network.
from subprocess import *
import json
import os
import random
from flbry import url
from flbry import channel
from flbry import markdown
from flbry.variables import *
from flbry import settings
from flbry import plugin

def upload(data):

    data = plugin.run(data)

    # This function actually will upload the file.
    # reference:
    #           --name          | lbry:// url to publish to
    #           --bid           | LBC to use while publishing
    #           --fee_amount    | How much does one need to pay for the publication
    #           --file_path     | The path to a file that's going to be uploaded
    #           --title         | Title of the publication on the LBRY network
    #           --license       | License of the publication
    #           --license_url   | Link to the license
    #           --thumbnail_url | Link to a thumbnail image
    #           --description   | A string of text describing the publication
    #           --tags          | List of tags.
    #           --channel_name  | Name of a channel to which to upload
    #                                  ( without it will be anonymous)

    #  More commands to upload function you can see at:
    #           https://lbry.tech/api/sdk#publish

    # An example of a working publish command:
    #    ./lbrynet publish --name="testing_upload_via_sdk_v2" --bid=0.01
    #    --file_path="/home/vcs/Desktop/upload_test_file.md"
    #    --title="Testing Uploading Directly from the LBRY SDK v2"
    #    --license="CC-BY-SA" --channel_name="@blenderdumbass"

    p = [flbry_globals["lbrynet"], "publish", "--name="+data["name"],
         "--bid="+str(data["bid"]), "--file_path="+data["file_path"]]

    data["thumbnail_url"] = speech_upload(data["thumbnail_url"])

    for i in ["title", "license", "license_url", "thumbnail_url", "description", "channel_name", "fee_amount"]:
        if i in data:
            if data[i]:
                p.append("--"+i+"="+str(data[i]))

    if data["fee_amount"]:
        p.append("--fee_currency=LBC")

    if "tags" in data:
        if data["tags"]:
            for i in data["tags"]:
                p.append("--tags="+i) # THIS IS STUPID IK. BUT IT WORKS



    out = check_output(p)
    try:
        out = json.loads(out)
    except:
        center("Connect to LBRY first.", "bdrd")
        return

    return out

def view_data(data):

    # this function will print the data

    # LBRY URL
    d = {"categories": ["LBRY URL"],
         "size":[1],
         "data":[["lbry://"+data["name"]]]}
    table(d, False)

    # FILE PATH
    d = {"categories": ["File Path"],
         "size":[1],
         "data":[[data["file_path"]]]}
    table(d, False)

    # CHANNEL, BID AND PRICE
    if not data["channel_name"]:
        channel = "[anonymous]"
    else:
        channel = data["channel_name"]

    if not data["fee_amount"]:
        price = "Gratis"
    else:
        price = str(data["fee_amount"])+" LBC"

    d = {"categories": ["Channel ID", "LBC BID", "Price"],
         "size":[1, 1, 1],
         "data":[[channel, str(data["bid"])+" LBC", price]]}
    table(d, False)

    # TITLE AND THUMBNAIL
    if not data["thumbnail_url"]:
        thumb = "[no thumbnail]"
    else:
        thumb = data["thumbnail_url"]

    if not data["title"]:
        title = "[no title]"
    else:
        title = data["title"]

    d = {"categories": ["Thumbnail", "Title"],
         "size":[2, 3],
         "data":[[thumb, title]]}
    table(d, False)

    # LICENSING INFORMATION
    if not data["license"]:
        license = "[no license]"
    else:
        license = data["license"]

    if not data["license_url"]:
        lurl = "[no license url]"
    else:
        lurl = data["license_url"]

    d = {"categories": ["License", "URL"],
         "size":[3, 2],
         "data":[[license, lurl]]}
    table(d, False)

    # DESCRIPTION PREVIEW
    d = {"categories": ["DESCRIPTION PREVIEW"],
         "size":[1],
         "data":[[data["description"].replace("\n", " ")]]}
    table(d, False)

    # Tags PREVIEW
    d = {"categories": ["TAGS"],
         "size":[1],
         "data":[[data["tags"]]]}
    table(d, False)

def configure(file_path="", data=None):

    # This function will prepare the publication data, before sending it
    # to the upload() function above.

    # So it doesn't say "File not found" if you put nothing
    if not file_path:
        file_path = input(typing_dots("File path", give_space=True))

    file_path = os.path.expanduser(file_path)
    while not os.path.exists(file_path):
        center("File '"+file_path+"' not found", "bdrd")
        file_path = input(typing_dots("File path", give_space=True))
        file_path = os.path.expanduser(file_path)

    lbryname = ""
    good = "qwertyuiopasdfghjklzxcvbnm-_QWERTYUIOPASDFGHJKLZXCVBNM1234567890"
    for i in range(70):
        lbryname = lbryname + random.choice(good)


    center("Upload Manager of FastLBRY")

    if not data:
        data = {"name":lbryname,
                "bid":0.001,
                "file_path":file_path,
                "title":"",
                "license":"",
                "license_url":"",
                "thumbnail_url":"",
                "channel_id":"",
                "channel_name":"",
                "description":"",
                "fee_amount":0,
                "tags":[]
        }

    # Completer thingy
    complete([
        "file",
        "bid",
        "price",
        "url",
        "title",
        "license",
        "channel",
        "tags",
        "description",
        "help",
        "save",
        "load",
        "publish",
        "thumbnail"
    ])

    while True:
        # preview the data
        view_data(data)
        center("---type 'help' to read how it works---")

        plugin.run(execute=False)
        # input
        c = input(typing_dots())

        if not c:
            break

        # Update file_path
        elif c.startswith("file"):
            if " " in c:
                file_path = c[c.find(" ")+1:]
            else:
                file_path = input(typing_dots("File path", give_space=True))

            while not os.path.exists(file_path):
                center("File '"+file_path+"' not found", "bdrd")
                file_path = input(typing_dots("File path", give_space=True))
            data["file_path"] = file_path

        # Update the bid info
        elif c.startswith("bid"):
            if " " in c:
                bid = c[c.find(" ")+1:]
            else:
                bid = input(typing_dots("Bid", to_add_dots=True))
            while True:
                try:
                    bid = float(bid)
                    if not bid > 0.00001:
                        1 / 0 # Fail switch
                    break
                except:
                    center("Bid cannot be: "+str(bid), "bdrd")
                    bid = input(typing_dots("Bid", to_add_dots=True))
            data["bid"] = bid

        # Setup a price
        elif c.startswith("price"):
            if " " in c:
                price = c[c.find(" ")+1:]
            else:
                price = input(typing_dots("Price", to_add_dots=True))
            while True:
                try:
                    price = float(price)
                    if price < 0:
                        1 / 0 # Fail switch
                    break
                except:
                    center("Price cannot be: "+str(price), "bdrd")
                    price = input(typing_dots("Price", to_add_dots=True))
            data["fee_amount"] = price

        # URL for the publication
        elif c.startswith("url"):
            if " " in c:
                url = c[c.find(" ")+1:]
            else:
                url = input(typing_dots("LBRY URL", give_space=True, to_add_dots=True))
            name = ""
            for i in url:
                if i in good:
                    name = name + i
                else:
                    name = name + "-"
            data["name"] = name

        # Title
        elif c.startswith("title"):
            if " " in c:
                title = c[c.find(" ")+1:]
            else:
                title = input(typing_dots("Title", give_space=True, to_add_dots=True))
            data["title"] = title

        # License setting
        elif c == "license":
            data["license"], data["license_url"] = choose_license()

        # Channel
        elif c == "channel":
            ch, chid = channel.select("Select from where to publish.", claim_id=True)
            data["channel_id"] = chid
            data["channel_name"] = ch

        # Tags
        elif c.startswith("tags"):
            if " " in c:
                th = c[c.find(" ")+1:]
            else:
                th = input(typing_dots("Tags separated by , ", give_space=True, to_add_dots=True))
            data["tags"] = th.split(",")

        elif c.startswith("thumbnail"):
            if " " in c:
                th = c[c.find(" ")+1:]
            else:
                th = input(typing_dots("Thumbnail url", give_space=True, to_add_dots=True))
            data["thumbnail_url"] = th

        # Description

        elif c.startswith("description"):
            if " " in c:
                df = c[c.find(" ")+1:]
                try:
                    text = open(df, "r")
                    text = text.read()
                except:
                    text = open("/tmp/fastlbrydescriptiontwriter.txt", "w")
                    text.write("Type your description here. Don't forget to save. Then return to FastLBRY.")
                    text.close()

                    os.system(df+" /tmp/fastlbrydescriptiontwriter.txt")
                    center("Press Enter when the file is ready and saved.")
                    input()
                    text = open("/tmp/fastlbrydescriptiontwriter.txt", "r")
                    text = text.read()
            else:
                text = input(typing_dots("Description", give_space=True, to_add_dots=True))

            data["description"] = text

        elif c == "help":
            markdown.draw("help/publish.md", "Publishing Help")

        # SAVE / LOAD OPTIONS

        elif c.startswith("save"):
            if " " in c:
                pn = c[c.find(" ")+1:]
            else:
                pn = input(typing_dots("Preset's name", to_add_dots=True))

            # Create the preset folder is it's not there

            try:
                os.mkdir(settings.get_settings_folder()+"presets")
            except:
                pass

            # Write the json file
            with open(settings.get_settings_folder()+"presets/"+pn+'.json', 'w') as f:
                json.dump(data, f, indent=4, sort_keys=True)

        elif c.startswith("load"):
            if " " in c:
                pn = c[c.find(" ")+1:]
            else:
                pn = input(typing_dots("Preset's name", to_add_dots=True))

            # loading the json file
            try:
                name = data["name"]
                file_path = data["file_path"]

                with open(settings.get_settings_folder()+"presets/"+pn+'.json') as f:
                    data = json.load(f)

                data["file_path"] = file_path
                data["name"] = name

            except:
                center("There is no '"+pn+"' preset!", "bdrd")


        # PUBLISHING

        elif c == "publish":
            out = upload(data)
            try:
                center("LBRY URL FULL TEXT:")
                print(out['outputs'][0]['permanent_url'])
                center("HTTPS URL FULL TEXT:")
                print(out['outputs'][0]['permanent_url'].replace("lbry://","https://spee.ch/"))
                center("Publishing is done successfully!", "bdgr")
                center("Confirming publication... It may take a few minutes.")
            except:
                center("Failed", "bdrd")
                center("================= ERROR! ================", "bdrd")
                try:
                    for line in out["message"].split("\n"):
                        center(line, "bdrd")
                except:
                    print(out)
                center("=========================================", "bdrd")

            return out

        elif c:
            c = plugin.run(data, command=c)

def speech_upload(file, name="", fee=0, speech=True):
    file = os.path.expanduser(file)

    if os.path.isfile(file):
        center("Uploading '"+file+"' to LBRY")

        if not name:
            rndname = ""
        else:
            rndname = name + "_"

        length = 70 - len(rndname)

        good = "qwertyuiopasdfghjklzxcvbnm-_QWERTYUIOPASDFGHJKLZXCVBNM1234567890"
        for i in range(length):
            rndname = rndname + random.choice(good)

        try:
            out = upload({"name":rndname,
                "bid":0.001,
                "file_path":file,
                "title":"",
                "license":"",
                "license_url":"",
                "thumbnail_url":"",
                "channel_id":"",
                "channel_name":"",
                "description":"",
                "fee_amount":fee,
                "tags":[]
            })
            if speech:
                return out['outputs'][0]['permanent_url'].replace("lbry://","https://spee.ch/")
            else:
                return out['outputs'][0]['permanent_url']
        except:
            return ""
            center("Failed uploading file", "bdrd")

    else:
        return file
