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
from flbry import settings
from flbry import markdown
from flbry import channel
from flbry.variables import *

def history():

    # This function will output wallet history.

    # So instead we are going to request only the first 20 and let
    # the user load more.

    w, h = tsize()

    page_size = h - 6
    page = 1

    balance = check_output([flbry_globals["lbrynet"],
                         "wallet", "balance"])
    try:
        balance = json.loads(balance)
    except:
        center("Connect to LBRY first.", "bdrd")
        return

    balance = balance["available"]

    while True:

        # Printing the search query and page number
        center("WALLET HISTORY. PAGE: "+str(page))
        center("AVAILABLE BALANCE: "+balance+" LBC")

        out = check_output([flbry_globals["lbrynet"],
                         "transaction", "list",
                         '--page='+str(page),
                         '--page_size='+str(page_size)])

        # Now we want to parse the json

        try:
            out = json.loads(out)
        except:
            center("Connect to LBRY first.", "bdrd")
            return


        d = {"categories":["CONFORMATIONS", "AMOUNT", "IS TIP", "PUBLICATION"],
                          "size":[1,1,1,3],
                          "data":[]}

        try:


            # List what we found
            for n, i in enumerate(out["items"]):

                confirm = i["confirmations"]
                amount = i["value"]
                tip = " "
                publication = " "
                try:
                    if i["support_info"][0]["is_tip"]:
                        if i["support_info"][0]["is_spent"]:
                            tip = "[v]"
                        else:
                            tip = "[ ]"
                    publication = i["support_info"][0]["claim_name"]
                except:
                    tip = " "
                    publication = " "


                d["data"].append([confirm, amount, tip, publication])

            table(d)
            # Tell the user that they might want to load more
            center(" ---type 'more' to load more---")
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

            try:
                url.get(out["items"][c]["support_info"][0]["claim_name"]+"#"+out["items"][c]["support_info"][0]["claim_id"])
            except:
                pass

            # Print the list again
            table(d)
            center("---type 'more' to load more---")

def balance():
    # Prints all wallet balance information
    balance = check_output([flbry_globals["lbrynet"],
                         "wallet", "balance"])
    try:
        balance = json.loads(balance)
    except:
        center("Connect to LBRY first.", "bdrd")
        return

    # Get the variables
    total = balance["total"]
    available = balance["available"]
    reserved = balance["reserved"]
    claims = balance["reserved_subtotals"]["claims"]
    supports = balance["reserved_subtotals"]["supports"]
    tips = balance["reserved_subtotals"]["tips"]

    # Show the total, available, and reserved amounts in a table
    center("Balance Information")
    d = {"categories":["total", "available", "reserved"],
            "size":[1,1,1],
            "data":[]}
    d["data"].append([total, available, reserved])
    table(d, False)

    # Show the sources of the reserved balance in a table
    center("Reserved Balance Information")
    d = {"categories":["claims", "supports", "tips"],
            "size":[1,1,1],
            "data":[]}
    d["data"].append([claims, supports, tips])
    table(d, False)

    # Here because it looks out of place without it
    center("--- for wallet transaction history type 'wallet' ---")

def support(claim_id, amount="", tip=False):
    # Dialog to send support or tip to claim_id

    d = {"categories": ["Amount", "Channel", "Comment"],
                        "size": [1,3,5],
                        "data": []}
    amount = float(settings.get("default_tip"))
    channel_name = "[anonymous]"
    channel_id = ""
    comment = None

    complete([
        "amount",
        "channel",
        "send",
        "comment"
    ])

    if tip:
        support_strs = ["Tipped", "tip"]
    else:
        support_strs = ["Boosted", "boost"]

    while True:
        # Just setting data directly wasn't working, so we clear it then append to it
        d["data"] = []
        # f'amount:.5f}' shows the amount in decimal notation with 5 places after the decimal
        d["data"].append([f'{amount:.5f}', channel_name, str(comment)])

        table(d, False)
        center("---type 'help' for support commands---")

        c = input(typing_dots())
        if not c:
            break

        if c == "amount":
            am = ""
            # while am is not a float
            while type(am) != type(5.0):
                am = input(typing_dots("Amount"))

                # If the user types nothing just keep the amount the same
                if not am:
                    break

                try:
                    amount = float(am)
                    am = amount
                except:
                    pass

        elif c == "channel":
            channel_name, channel_id = channel.select("Select the signing channel.", claim_id=True)

        elif c == "help":
            markdown.draw("help/support.md", "Support Help")

        elif c.startswith("comment"):
            c = c + ' '
            a = c[c.find(" "):]
            if len(a) > 1:
                comment = file_or_editor(a, "Type the comment here. Don't forget to save. Then return to FastLBRY.")
            else:
                comment = input(typing_dots("Comment", give_space=True))

        elif c == "send":
            args = [
                    flbry_globals["lbrynet"],
                    "support", "create",
                    "--claim_id="+claim_id,
                    "--amount="+f'{amount:.5f}'
            ]

            if channel_id:
                args.append("--channel_id="+channel_id)

            if comment:
                args.append("--comment="+comment)

            if tip:
                args.append("--tip")

            try:
                x = check_output(args)
                center(support_strs[0]+" with "+f'{amount:.5f}'+" LBC", "bdgr")
            except Exception as e:
                center("Error sending "+support_strs[1]+": "+str(e), "bdrd")

            break

def addresses():
    w, h = tsize()
    page_size = h - 5
    # TODO: At the time of writing, pagination in this command is not working, so we only get the first page.
    # When this gets fixed, please add pagination here.
    out = check_output([flbry_globals["lbrynet"],
                        "address", "list",
                        "--page_size="+str(page_size)])

    out = json.loads(out)

    try:

        data_print = {"categories":["Address"],
                        "size":[1],
                        "data":[]}

        # List what we found
        for n, i in enumerate(out["items"]):
            data_print["data"].append([i["address"]])

        table(data_print)
        center("")

    # Error messages
    except Exception as e:
        if "code" in out:
            center("Error code: "+out["code"], "bdrd")
            if "message" in out:
                center("Error: "+out["message"], "bdrd")
        else:
            center("Error: "+e, "bdrd")
        return

def address_send(amount="", address=""):
    if not amount:
        amount = input(typing_dots(("Amount to send")))

    # Making sure it's actually a number
    try:
        float(amount)
    except:
        center("Amount cannot be '"+amount+"'", "bdrd")
        return
        
    # Making sure that it's a float
    if "." not in str(amount):
        amount = str(amount)+".0"

    if not address:
        address = input(typing_dots("Address to send to", give_space=True))

    out = check_output([flbry_globals["lbrynet"],
                        "wallet",
                        "send",
                        str(amount),
                        address])

    out = json.loads(out)

    if "message" in out:
        center("Error sending to address: "+out["message"], "bdrd")
    else:
        center("Successfully sent "+str(amount)+" to "+address, "bdgr")
