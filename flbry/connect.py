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

# This file will start the lbrynet sdk.

import subprocess
import json
import random
from flbry.variables import *

def start():

    if check():
        center("SDK is already running")
    else:
        retcode = subprocess.Popen([flbry_globals["lbrynet"], 'start'],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.STDOUT)
        progress_bar(0.2, 10, "Checking Wallet...")

        count = 0
        while not check():
            count = count + ((9 - count) / (5+random.random()))
            #if count > 5:
            #    count = 3
            progress_bar(count, 10, "Loading Wallet...")
        progress_bar(10, 10, "Connection established")
        print()

def stop():
    if check():
        retcode = subprocess.Popen([flbry_globals["lbrynet"], 'stop'],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.STDOUT)
        center("LBRY Connection Closed")
    else:
        center("SDK is not running")

def check():
    # This output true or false
    # whether the SDK is running

    try:
        out = subprocess.check_output([flbry_globals["lbrynet"],
                         "claim", "search", '--text="test"',
                         '--page=1',
                         '--page_size=1',
                            "--no_totals",
                            '--order_by=release_time'])
        out = json.loads(out)
        out["items"]
        return True
    except Exception as e:
        #print("ERROR = ", e)
        return False
