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
import json
import urllib.request

from flbry import url
from flbry.variables import *
from flbry import markdown
from flbry import channel
from flbry import settings

def list(claim_id: str, link: str, comment_id: str = ""):
    """
    Lists comments in a short form, truncating some if needed. Comments can be selected for further actions.

    Keyword arguments:
    claim_id -- ID of the claim to get comments from
    link -- LBRY URL of the claim, used for display
    comment_id -- Comment ID to get sub-comments of, optional
    """
    w, h = tsize()

    page_size = h - 5
    page = 1

    while True:
        # Printing the search query and page number
        center("COMMENTS OF: "+link+" PAGE : "+str(page))

        params = {
            "claim_id": claim_id,
            "page": page,
            "page_size": page_size,
            "sort_by": 3,
            "top_level": True,
        }

        if comment_id:
            params["parent_id"] = comment_id
            params["top_level"] = False

        out = comment_request("comment.List", params)
        if not out:
            return
        out = out["result"]

        if not "items" in out:
            center("Publication has no comments", "bdrd")
            return

        d = {"categories":["Tip LBC", "Comments", "Channel",  "Preview"],
                          "size":[1,1,2,5],
                          "data":[]}

        try:


            # List what we found
            for n, i in enumerate(out["items"]):


                preview = "---!Failed Loading comment---"
                support = 0
                replies = 0
                bywho = "[anonymous]"

                try:
                    comment = i["comment"]
                    preview = comment.replace("\n", " ")
                    support = i["support_amount"]
                    bywho = i["channel_name"]
                    replies = i["replies"]
                except:
                    pass

                d["data"].append([support, replies, bywho, preview])

            table(d)

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

        while True:
            # Making sure that we stop every time a new page is reached
            c =  input(typing_dots())
            if c == "more":
                break

            try:
                c = int(c)
            except:
                return

            view(out["items"][c])

            # Print the list again
            table(d)
            center("---type 'more' to load more---")

def show_view_info(i, derived):
    comment = derived[0]
    preview = derived[1]
    support = derived[2]
    bywho   = derived[3]
    replies = derived[4]

    # TIP LBC     # COMMENTS ( REPLIES ) # CHANNEL
    d = {"categories":["Tip LBC", "Comments",  "Channel"],
                        "size":[1,1,3],
                        "data":[[support, replies, bywho]]}
    table(d, False)

    # Preview
    d = {"categories":["Preview"],
                        "size":[1],
                        "data":[[preview]]}
    table(d, False)

    # The help thing
    center("--- for comment commands list type 'help' --- ")

def view(i):
    """Allows the user to interact with and/or read a given comment"""

    preview = "---!Failed Loading comment---"
    comment = ""
    support = 0
    bywho = "[unknown]"
    replies = 0

    try:
        comment = i["comment"]
        preview = comment.replace("\n", " ")
        support = i["support_amount"]
        bywho = i["channel_name"]
        replies = i["replies"]
    except:
        pass

    derived = [comment, preview, support, bywho, replies]

     # List of commands for autocomplete feature.
    complete([
        "help",
        "read",
        "channel",
        "comments",
        "reply",
        "delete",
        "edit"
    ])

    # let's implement commands
    while True:
        show_view_info(i, derived)
        c =  input(typing_dots())

        if not c:
            break

        elif c == "help":
            markdown.draw("help/comments.md", "Comments Help")

        elif c == "read":

            savedes = open("/tmp/fastlbrylastcomment.md", "w")
            savedes.write(comment)
            savedes.close()

            markdown.draw("/tmp/fastlbrylastcomment.md", "Full Text Of a Comment")

        elif c == "channel":
            channel.simple(i["channel_url"])

        elif c == "comments":
            list(i["claim_id"], " ", i["comment_id"],)

        elif c.startswith("reply"):
            c = c + ' '
            post(i["claim_id"], c[c.find(" "):], i["comment_id"])

        elif c == "delete":
            delete(i["comment_id"], bywho)

        elif c.startswith("edit"):
            c = c + ' '
            update(i, c[c.find(" "):])

def post(claim_id, args,  parent_id=""):

    # This will post a comment under either a publication or a
    # comment as a reply.
    editor = settings.get("default_editor")
    text = "Type your reply here. Don't forget to save. Then return to FastLBRY."

    if len(args) > 1:
        text = file_or_editor(args, text)
    else:
        if editor:
            text = file_or_editor(args, text, editor)
        else:
            text = input(typing_dots("Comment text", give_space=True))

    post_as, post_as_id = channel.select("Reply as who? Select Channel.", True)

    if not post_as.startswith("@"):
        post_as = "@"+post_as

    sigs = channel.sign(text, post_as)
    if not sigs:
        return

    params = {
        "channel_id": post_as_id,
        "channel_name": post_as,
        "claim_id": claim_id,
        "comment": text,
        **sigs
    }

    if parent_id:
        params["parent_id"] = parent_id

    out = comment_request("comment.Create", params)
    if not out:
        return

    if "error" in out:
        center("Error: "+out["error"]["message"], "bdrd")
    else:
        center("Comment is sent.", "bdgr")

def inbox(opt=10):

    # This function will return the latest comments from the latest
    # publications. Similar to an email inbox. But with a limitation.

    # There is no system in the SDK to implement a history of comments
    # seamlessly. So then I need to cash a large file of comments. Or
    # do something clever. I think there will be a few options.

    # You noticed the opt=10 preset on the top. It's the default value.
    # Basically the user might type one of 4 things.

    #    inbox
    #    inbox 40     (or any number what so ever)
    #    inbox all
    #    inbox cashed

    # Each will run a slightly different algorithm to get the inbox
    # comments.

    #    inbox

    # This will use the predefined 10 and read last 10 publications
    # comments to add. It will combine them with the pre-cashed ones
    # for the user to view. As you may imagine, giving it a number as
    # in:

    #    inbox 40
    #    inbox 2
    #    inbox 50

    # Will load this number of publications. To update with them the
    # cash and then present it to the user.

    #    inbox all

    # This one will take longest. But might be useful for some users.
    # This will go through all publications and cash comments from all
    # of them.

    #    inbox cashed

    # This one is the fastest of them. It will only read the cash file
    # and present it to the user. So for instance you want to quickly
    # go back to the inbox without loading anything at all.


    try:
        opt = int(opt)
        reached = opt
        goal = opt
    except:
        goal = 0
        if opt == "all":
            reached = True
        else:
            reached = False

    # Updating the cash file ( inbox.json )
    page = 0
    items_total = 0
    current_item = 0



    try:
        with open(settings.get_settings_folder()+'inbox.json') as json_file:
            comments_cache = json.load(json_file)
    except:
        comments_cache = []

    checked_publications = []

    while reached > 0:

        if type(reached) == int:
            reached = reached - 50

        page = page + 1
        page_size = 50

        # Getting data about publications.


        if page != 1:
            out = check_output([flbry_globals["lbrynet"],
                         "stream", "list",
                         '--page='+str(page),
                         '--page_size='+str(page_size),
                            "--no_totals"])
            out2 = check_output([flbry_globals["lbrynet"],
                         "channel", "list",
                         '--page='+str(page),
                         '--page_size='+str(page_size),
                            "--no_totals"])
        else:
            out = check_output([flbry_globals["lbrynet"],
                         "stream", "list",
                         '--page='+str(page),
                                '--page_size='+str(page_size)])
            out2 = check_output([flbry_globals["lbrynet"],
                         "channel", "list",
                         '--page='+str(page),
                                '--page_size='+str(page_size)])



        # Now we want to parse the json
        items = []
        try:
            out = json.loads(out)
            out2 = json.loads(out2)
            items = out["items"]
            try:
                items = items[:int(opt)]
            except:
                pass
            for i in out2["items"]:
                items.append(i)
        except:
            break

        if not items:
            break

        if page == 1:
            # Getting Totals to calculate the progress bar
            if reached == True:
                items_total = out["total_items"] + out2["total_items"]
            else:
                try:
                    items_total = int(opt) + out2["total_items"]
                except:
                    items_total = 0

        # Reading items from the items

        for publication in items:

            # skip dublicate publications. ( like when you edited
            # a publication )

            if publication["name"] in checked_publications:
                continue
            checked_publications.append(publication["name"])

            current_item = current_item + 1

            # If above the requested amount.
            #if current_item > items_total:
                #break

            # Draw progress bar
            progress_bar(current_item, items_total, publication["name"])

            # let's now get all the comments
            claim_id = publication["claim_id"]

            comment_page = 0

            while True:

                comment_page = comment_page + 1

                params = {
                    "claim_id": claim_id,
                    "page": comment_page,
                    "page_size": 50,
                    "sort_by": 3,
                    "top_level": False,
                }

                out = comment_request("comment.List", params)
                if not out:
                    return
                cout = out["result"]

                # TODO: For now I'm stopping on first page when ever I'm
                #       loading channel's comments ( community disscussion ).
                #       This is obviously not going to work with "inbox all",
                #       so please make the logic a bit smarter, so it will work.

                if "items" not in cout or publication["value_type"] == "channel":
                    break

                for i in cout["items"]:

                    # I want to add a few things into the comment data
                    i["publication_url"] = publication["permanent_url"]
                    i["publication_name"] = publication["name"]
                    try:
                        i["publication_title"] =  publication["value"]["title"]
                    except:
                        i["publication_title"] =  publication["name"]

                    
                    if i not in comments_cache:
                        comments_cache.append(i)


    print()

    # Let's sort the comments based on the time they were sent
    comments_cache = sorted(comments_cache, key=lambda k: k['timestamp'], reverse=True)

    # Let's remove duplicate comments
    tmp = []
    tmp_ids = []
    for comment in comments_cache:
        if comment["comment_id"] not in tmp_ids:
            tmp_ids.append(comment["comment_id"])
            tmp.append(comment)
    comments_cache = tmp
    
    with open(settings.get_settings_folder()+'inbox.json', 'w') as fp:
            json.dump(comments_cache, fp , indent=4)



    # Now that we have comments cached and ready. I can start actually showing
    # them.

    w, h = tsize()
    page_size = (h-5)
    page = 0

    while True:

        d = {"categories":["Tip LBC", "Comments", "Publication",  "Channel",  "Preview"],
                          "size":[1,1,4,2,4],
                          "data":[]}

        items = []

        for n, i in enumerate(comments_cache):

            startfrom = int( page * page_size )
            endat     = int( startfrom + page_size )

            if n in range(startfrom, endat):

                items.append(i)

                preview = "---!Failed Loading comment---"
                support = 0
                replies = 0
                where = "[some publication]"
                bywho = "[anonymous]"

                try:
                    comment = i["comment"]
                    preview = comment.replace("\n", " ")
                    where = i["publication_title"]
                    support = i["support_amount"]
                    bywho = i["channel_name"]
                    replies = i["replies"]

                except:
                    pass

                d["data"].append([support, replies, where, bywho, preview])
        table(d)

        # Tell the user that they might want to load more
        center("---type 'more' to load more---")


        # Making sure that we stop every time a new page is reached
        c =  input(typing_dots())
        if c == "more":
            page = page +1
            continue

        try:
            c = int(c)
        except:
            return

        view(items[c])
        c = input(typing_dots())

def update(i, args):
    comment = i["comment"]
    comment_id = i["comment_id"]
    commenter = i["channel_name"]
    editor = settings.get("default_editor")

    if len(args) > 1:
        text = file_or_editor(args, comment)
    else:
        if editor:
            text = file_or_editor(args, comment, editor)
        else:
            print("Comment: "+comment)
            text = input(typing_dots("Edited comment", give_space=True))


    sigs = channel.sign(text, commenter)
    if not sigs:
        return

    params = {
        "comment": text,
        "comment_id": comment_id,
        **sigs
    }

    out = comment_request("comment.Edit", params)

    if "error" in out:
        center("Error updating comment: " + out["error"]["message"], "bdrd")
        center("Make sure you are editing a comment you posted.", "bdrd")
    elif "result" in out:
        center("Comment edited!", "bdgr")

def delete(comment_id: str, commenter: str):
    """
    Deletes a comment you posted by its comment ID
    """
    sigs = channel.sign(comment_id, commenter)
    if not sigs:
        return

    params = {
        "comment_id": comment_id,
        **sigs
    }

    out = comment_request("comment.Abandon", params)
    if "result" in out:
        center("Comment deleted!", "bdgr")
    elif "error" in out:
        center("Error deleting comment: " + out["error"]["message"], "bdrd")
        center("Make sure you posted this comment.", "bdrd")

def comment_request(method: str, params: dict):
    """
    Sends a request to the comment API
    """
    data = {
        "method": method,
        "id": 1,
        "jsonrpc":"2.0",
        "params": params
    }
    data = json.dumps(data).encode()

    headers = {
        "Content-Type": "application/json"
    }

    try:
        req = urllib.request.Request(flbry_globals["comment_api"], data, headers)
        res = urllib.request.urlopen(req)
        out = res.read().decode()
        return json.loads(out)
    except Exception as e:
        center("Comment Error: "+str(e))
        return
