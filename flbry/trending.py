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

from flbry import url
from flbry.variables import *

def simple(articles=False):


    # This will give out the information about trending publictions
    # Either

    # So we want to request a query to the SDK to search what ever
    # the user wants. The problem is it can be a very large output.
    # For example the "blender dumbass" query returns 1000 claims
    # on the LBRY network. And people will wait for a very long time
    # on something that might have a million claims.

    # So instead we are going to request only the first 20 and let
    # the user load more.

    # If could be articles
    text =     ""
    if articles:
        text = " ARTICLES"

    w, h = tsize()

    page_size = h - 5
    page = 1

    while True:

        # Printing the search query and page number
        center("TRENDING"+text+" PAGE :"+str(page))

        if not articles:
            out = check_output([flbry_globals["lbrynet"],
                         "claim", "search",
                         '--page='+str(page),
                         '--page_size='+str(page_size),
                            "--no_totals",
                            "--order_by=trending_mixed"])
        else:
            out = check_output([flbry_globals["lbrynet"],
                         "claim", "search",
                         '--page='+str(page),
                         '--page_size='+str(page_size),
                            "--no_totals",
                                "--order_by=trending_mixed",
                                '--media_types=text/markdown'])

        # Now we want to parse the json
        try:
            out = json.loads(out)
        except:
            center("Connect to LBRY first.", "bdrd")
            return

        d = {"categories":["Type", "Channel",  "Title"],
                          "size":[1,1,5],
                          "data":[]}

        try:


            # List what we found
            for n, i in enumerate(out["items"]):

                title = "---!Failed Loading Title---"
                ftype = "claim"
                bywho = "[anonymous]"

                try:
                    try:
                        title = i["value"]["title"]
                    except:
                        title = i['name']
                    try:
                        ftype = what[i["value"]["stream_type"]]
                    except:
                        ftype = what[i["value_type"]]
                    bywho = i["signing_channel"]["name"]
                except:
                    pass

                d["data"].append([ftype, bywho, title])

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

            url.get(out["items"][c]["canonical_url"])

            # Print the list again
            table(d)
            center("---type 'more' to load more---")
