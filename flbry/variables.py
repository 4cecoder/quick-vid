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

# This file is a set of variables used by different files. It's needed
# so I will not need to hard code the values each time. Stuff like
# basic translations of the LBRY data into human language. And a more
# complex functions like translating size in bytes into something more
# readable.

import os
import json
import inspect



# Colors are used to make the
clr = {
    "norm":"\033[00m", # Reset to normal
    "bold":"\033[01m", # Bold Text
    "ital":"\033[03m", # Italic Text
    "undr":"\033[04m", # Underlined
    "blnk":"\033[05m", # Blinking

    # Text
    "tdbl":"\033[30m", # Dark Black
    "tdrd":"\033[31m", # Dark Red
    "tdgr":"\033[32m", # Dark Green
    "tdyl":"\033[33m", # Dark Yellow
    "tdbu":"\033[34m", # Dark Blue
    "tdma":"\033[35m", # Dark Magenta
    "tdcy":"\033[36m", # Dark Cyan
    "tdwh":"\033[37m", # Dark White

    "tbbl":"\033[90m", # Bright Black
    "tbrd":"\033[91m", # Bright Red
    "tbgr":"\033[92m", # Bright Green
    "tbyl":"\033[93m", # Bright Yellow
    "tbbu":"\033[94m", # Bright Blue
    "tbma":"\033[95m", # Bright Magenta
    "tbcy":"\033[96m", # Bright Cyan
    "tbwh":"\033[97m", # Bright White
    # Background
    "bdbl":"\033[40m", # Dark Black
    "bdrd":"\033[41m", # Dark Red
    "bdgr":"\033[42m", # Dark Green
    "bdyl":"\033[43m", # Dark Yellow
    "bdbu":"\033[44m", # Dark Blue
    "bdma":"\033[45m", # Dark Magenta
    "bdcy":"\033[46m", # Dark Cyan
    "bdwh":"\033[47m", # Dark White

    "bbbl":"\033[100m", # Bright Black
    "bbrd":"\033[101m", # Bright Red
    "bbgr":"\033[102m", # Bright Green
    "bbyl":"\033[103m", # Bright Yellow
    "bbbu":"\033[104m", # Bright Blue
    "bbma":"\033[105m", # Bright Magenta
    "bbcy":"\033[106m", # Bright Cyan
    "bbwh":"\033[108m"  # Bright White
}

# A function that turns emogi into emocons
def emote(text, ASCII=True):

    # TODO: Add more emogis to the lists.
    #      Odysee.com just added a bunch of weird ass
    #      stickers with codes for each one. They need
    #      to work in FastLBRY.

    emojis = {
        ":smile:"           :"☺️",
        ":grin:"            :"😃",
        ":frowning_face:"   :"☹️",
        ":sob:"             :"😭",
        ":open_mouth:"      :"😮",
        ":kissing:"         :"😗",
        ":wink:"            :"😉",
        ":stuck_out_tongue:":"😛",
        ":confused:"        :"😕",
        ":neutral_face:"    :"😐",
        ":expressionless:"  :"😑",
    }
    emocons = {
        "☺️":":)",
        "😃":":D",
        "☹️":":(",
        "😭":":,(",
        "😮":":o",
        "😗":":*",
        "😉":";)",
        "😛":":p",
        "😕":":/",
        "😐":":|",
        "😑":"(-_-)"
    }

    # The actual function lol
    for i in emojis:
        text = text.replace(i, emojis[i])
    if ASCII:
        for i in emocons:
            text = text.replace(i, emocons[i])
    return text

# A function that insures a specific width of the printed part
def wdth(x, n):

    # Convert Data to String
    mode = "normal"
    if type(x) == bool and x == True:
        x = "V"
        mode = "bdgr"
    elif type(x) == bool and x == False:
        x = "X"
        mode = "bdrd"
    else:
        x = str(x)

    # Turn emogis
    x = emote(x)

    # Some characters are too wide. They do not obey the
    # monospace of the terminal, thus making it not pretty.

    # This is the string of characters which are checked to
    good = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'’()*+,-./:;<=>?@[\]^_`{|}~ йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮёЁ"

    # let's filter the string
    y = x
    from flbry import settings
    if not settings.get("ignore_width_forcing"):
        x = ""
        for i in y:
            if i in good:
                x = x + i
            else:
                x = x + "▓"

    # Now let's print what we've got.
    if len(y) < n:
        fac = n-len(y)
        fac1 = int(round(fac/2))
        fac2 = fac1
        while fac1 + fac2 > fac:
            fac2 -=1
        while fac1 + fac2 < fac:
            fac2 +=1
        x = (" "*fac1)+x+(" "*fac2)
    elif len(y) > n:
        if n > 10:
            x = x[:n-3]+"..."
        else:
            x = x[:n]
    if mode == "normal":
        return x
    else:
        return clr[mode]+clr["bold"]+x+clr["norm"]

# A dictionary for translations of things from the SDK into
# readable thing

what = {
    "stream":"FILE",
    "repost":"SHARED",
    "channel": "CHANNEL",
    "collection": "PLAYLIST",
    "video":"VIDEO",
    "audio":"SOUND",
    "document":"TEXT",
    "binary":"FILE",
    "image":"PICTURE"
}

# This function will take a list and present in a pretty
# way.

def tgz(x):

    # Just in case
    if type(x) != list:
        x = x.split()

    y = ""
    for i in x:
        y = y + i + ", "

    return y[:-2]

# This function will convert bites into readable data making sense

def csize(x):

    x = float(x)

    l = ["B","KB", "MB", "GB", "TB"]

    for i in range(5):
        if x > 1024:
            x = x / 1024
        else:
            return str(round(x, 2))+" "+l[i]
    return str(round(x, 2))+" "+l[i]

# This next function will select the amount of ::: for a given
# input.

def typing_dots(text="", to_text=True, to_add_dots=False,  give_space=False):


    depth = len(inspect.stack()) # This is the depth of the stack

    # since this function call adds 1 to the stack we need
    # to decrease the number by one

    depth -= 1
    if not text or not to_add_dots:
        depth -= 1

    # Now I want to select a sequence of colors.

    x = ["bdma","bdbu", "bdrd", "bdgr", "bdcy", "bdyl"]

    ret = " "+clr["bold"]
    for i in reversed(range(depth)):
        ret = ret + clr["tbwh"] + clr[x[i % len(x)]] + ":"
    ret = ret + clr["norm"]+" "

    w, h = tsize()
    if text and to_text:
        side_string = clr["tbwh"]+" < "+text+" "

        put_at = w-len(side_string)-1

        if not give_space:
            put_at = int(w/2)-int(len(side_string)/2)

        print(wdth("", put_at)+clr["bdma"]+clr["bold"]+side_string+clr["norm"], end="")
        ret = "\r"+ret
    return ret


def tsize():

    # This funtion will get the size of the terminal and
    # return it to the variables provided width, height

    # On some systems this may not work. So there is a
    # try function.

    try:
        # Getting the size of the terminal
        import os
        w, h = os.get_terminal_size()

        # Sometimes when the terminal width is either
        # even or odd. It breaks code for some other
        # thing written differenly. For example:

        # You may have an even width ( like 84 ) when
        # writing a function. And then it works on different
        # widths as well like 62 and 80 and 48. All of them
        # are still even. Then you scale the terminal to be
        # something off like 63 and the function breaks. You
        # have one character too much or one character too little.

        # This is why I do not want to have a difference. And
        # force width to be one less, if it's not divisible by 2.

        if not w % 2:
            w = w - 1

        return w, h

    except:

        # If, by any reason the terminal can't get it's size.
        # We want to return some size regardless.

        w = 60
        h = 20

        return w, h



def logo():

    # This function will draw a pretty FastLBRY logo to the user
    # at startup.

    # Getting terminal size
    w, h = tsize()

    if w > 50:

        l = []

        l.append( "█▓▓█▓▓▓▓▓▓█▓██▓▓▓▓▓▓▓█▓▓▓▓▓▓█▓▓▓▓██▓▓▓▓█▓▓▓▓█" )
        l.append( "▓▒▒▒▒▒▒▒▓▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▓▒▒▒▒▒▒▒▒▒▓▒▒▒▒▓▒▓" )
        l.append( "██░░░▒░░░░░░▒░░░░░░░▒░░░░░░░░░▒░░▒░░░░░░░░▒▓▓" )
        l.append( "▓▓░ ░          ░             ░    ■     ■░░▒▓" )
        l.append( "▓▒▒ ╔════════■   ░  ╔════╗ ╔════╗ ║  ░  ║ ░▓█" )
        l.append( "▓▒░ ║ ░      ║      ║    ║ ║    ║ ║     ║ ░▒▓" )
        l.append( "█▓░░║        ║      ╠════╣ ╠═╦══╝ ╚══╦══╝ ▒▒▓" )
        l.append( "▓▒▒ ╠══ AST ■║      ║    ║ ║ ╚══╗    ║   ░░▒█" )
        l.append( "█▒░ ║        ║      ║    ║ ║    ║    ║    ░▓▓" )
        l.append( "▓▓░ ║    ░   ╚═════■╚════╝ ■    ■ ░  ║ ░  ░▒▓" )
        l.append( "▓▒░░║ ░       THE TERMINAL CLIENT    ║    ▒▒█" )
        l.append( "█▒▒ ■      ░                  ░      ■ ▒░ ░▓▓" )
        l.append( "▓▒░░░░░░░▒░░░░▓░░░░░▒░░░░░░░░░▒░░░░▒░░░░░░░▒█" )
        l.append( "▓▓▒▒▒▒▓▒▒▒▒▒▓▒▒▒▒▓▒▒▓▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▓▒▒▒▒▒▓▓▓" )
        l.append( "█▓▓█▓▓▓▓▓████▓▓▓▓█▓▓▓▓█▓▓▓▓██▓▓▓█▓▓▓▓▓█▓▓▓▓██" )

        print("    "+clr["bdma"]+(" "*(w-8))+clr["norm"])

        # I want to fill the width of the terminal around the logo
        # with a texture. But since it's text based I will need to
        # code a texture into it. I can use the blocks seen below
        # and select randomly between them.

        # You can see I included multiple of darkest block and
        # almost non bright blocks. This will increase the
        # probability of the dark blocks.

        block = "████████▓▓▓▒" #for the random to choose
        import random

        # Now let's output

        for i in l:
            f = "" # Texture fill string.

            # Fill the f string with random blocks
            for g in range(int(w/2-27)):
                f = f + random.choice(block)

            # Print a line with random filler and the line it self.
            print ("    "+clr["bdma"]+" "+clr["norm"]+f+i+f+clr["bdma"]+" "+clr["norm"])



    else:
        center( "FastLBRY")
        center( "terminal")

    center("")
    print()

def table(data, number=True):

    # This function will present data in a pretty table thing.

    # So let's first of all get the size of the terminal
    w, h = tsize()

    if number:
        w = w - 4

    # Then let's draw the categories for this we need to extract
    # it's sizes. If there is no 'size' variable the sizes of
    # each category will be spread equally.

    size = [] # Here the size will go as pure character value.

    if "size" in data:
        for i in data["size"]:
            size.append(int(( w - 10 ) / sum(data["size"]) * i))

    while sum(size) < w - 10:
        size[-1] += 1

    # printing categories
    nb = ""
    if number:
        nb = "    "
    s = "    "+clr["bdma"]+" "+clr["tbwh"]+nb

    for n, item in enumerate(data["categories"]):
        s = s + wdth(item.upper(), size[n])
    print(s+clr["bdma"]+" "+clr["norm"])

    size[-1] += 1

    # printing items
    for b, i in enumerate(data["data"]):

        # dark bright sequence thingy
        if b % 2:
            d = "b"
        else:
            d = "d"
        nb = ""
        if number:
            nb = clr["tbwh"]+wdth(b,4)
        s = "    "+clr["bdma"]+" "+nb+clr["norm"]+clr["b"+d+"bu"]#+clr["tbwh"]
        for n, item in enumerate(i):
            s = s +clr["b"+d+"bu"]+ clr["tbwh"]+wdth(item, size[n]-1)+clr["bdma"]+" "
        print(s+clr["norm"])

def center(line, c="bdma", blink=False):

    # This funtiocn will bring a given string of text
    # in the center of the terminal with a nice backgroud
    # around it.


    w, h = tsize()

    if blink:
        blink = clr["blnk"]
    else:
        blink = ""

    if len(line) % 2:
        line = line + " "

    if len(line) < w - 11:
        print("    "+clr[c],
          wdth(" ", int((w-10)/2 - (len(line)/2))),
          clr["bold"]+clr["tbwh"]+blink+line,
          wdth(" ", int((w-10)/2 - (len(line)/2))-1),
          clr["norm"])
    else:
        print("    "+clr[c],
              clr["bold"]+clr["tbwh"]+blink+wdth(line,w-10),
          clr["norm"])


def timestring(tleft):

    # This crazy function will convert the microsecond into something
    # a bit more usefull. Like 03:20:90.06 Kind a thing.

    tleftX = tleft

    tleft = int(tleftX)

    addend = tleftX - tleft


    valt = str(tleft)

    if tleft > 60 :
        le = tleft
        tleft = int(tleft / 60)
        le = le - int(tleft * 60)

        stleft = "0"*(2-len(str(tleft)))+str(tleft)
        sle = "0"*(2-len(str(le)))+str(le)

        valt = stleft+":"+ sle

        if tleft > 60 :
            lele = le
            le = tleft
            tleft = int(tleft / 60)
            le = le - int(tleft * 60)
            lele = (lele - le)
            if lele < 0:
                lele = int(lele * -1)

            stleft = "0"*(2-len(str(tleft)))+str(tleft)
            sle = "0"*(2-len(str(le)))+str(le)
            slele = "0"*(2-len(str(lele)))+str(lele)

            valt = stleft+":"+ sle + ":" + slele

            if tleft > 24 :
                le = tleft
                tleft = int(tleft / 24)
                le = le - int(tleft * 24)
                valt = str(tleft)+" DAYS AND "+ str(le) + " HRS"
    return valt + "." + str(int(addend*100))

# This a list of known licenses, info a and links
licenses = [
    # NAME , URL , COMMENT
    ["GNU General Public License Version 3 (or later)",
     "https://www.gnu.org/licenses/gpl-3.0.html",
     "Strong Copyleft. Recommended for Software."],
    ["GNU General Public License Version 3 (only)",
     "https://www.gnu.org/licenses/gpl-3.0.html",
     "Strong Copyleft."],
    ["GNU Free Documentation License",
     "https://www.gnu.org/licenses/fdl-1.3.html",
     "Strong Copyleft. Recommended for books."],
    ["Creative Commons Attribution-ShareAlike 4.0 International",
     "https://creativecommons.org/licenses/by-sa/4.0/",
     "Copylefted, Recommended for Art."],
    ["Creative Commons Attribution 4.0 International",
     "https://creativecommons.org/licenses/by/4.0/",
     "Non Copylefted, Free License."],
    ["Creative Commons Zero 1.0 International",
     "https://creativecommons.org/publicdomain/zero/1.0/",
     "Public Domain"],
    ["Creative Commons Attribution-NoDerivatives 4.0 International",
     "https://creativecommons.org/licenses/by-nd/4.0/",
     "Does not allow changes. Recommended for opinion pieces."]
]

def progress_bar(now, total, name=""):

    # This function will draw a pretty progress bar that fills up
    # one problem. It requires an empty print line after it. Or it
    # will start printing whatever in the same line as the progress
    # bar.

    # dimensions
    w, h = tsize()
    fullw = w - 8

    # string
    string = " "+str(int(round(now/total*100)))+"% "+str(now)+" / "+str(total)+" "+name
    #string = string+" "*(fullw-len(string))
    string = wdth(string, fullw)


    howfar = int(round(fullw / total * now))

    pstring = clr["tbwh"]+clr["bold"]+clr["bdcy"]+string[:howfar]+clr["bdma"]+string[howfar:]


    print("\r    "+pstring, end=clr["norm"])

# We need a system of auto-filling commands. As well as a history type thing.
# so people could come back to a previous command by pressing the up arrow.

# Now all systems will have readline since it's a GNU package

complete_commands = []
def complete(commands, add=False):

    # This will make sure that we can add commands to
    # the completer after it's set.
    global complete_commands
    if not add:
        complete_commands = commands
    else:
        for i in commands:
            complete_commands.append(i)
    commands = complete_commands

    try:
        import readline

        # Then we need to specify a function for completion
        def completer(text, state):
            options = [i for i in commands if i.startswith(text)]
            if state < len(options):
                return options[state]
            else:
                return None

        # And we need to setup the completer
        readline.parse_and_bind("tab: complete")
        readline.set_completer(completer)

    except Exception as e:
        center("Auto-completer error: "+str(e), "bdrd")

def print_web_instance(url):
    from flbry import settings

    web_instances = [
        # NAME     URL                    MAINTAINER   INTERFACE
        ["Odysee", "https://odysee.com/", "LBRY Inc.", "JavaScript"],
        ["Madiator", "https://madiator.com/", "Madiator2011", "JavaScript"],
        ["Spee.ch", "https://spee.ch/", "LBRY Inc.", "Direct Files"]
    ]

    # If the "librarian_instance" setting is set, use that as the URL
    librarian_instance = ["Librarian", "https://librarian.bcow.xyz/", "imabritishcow", "Invidous-like web interface"]
    libinstance = settings.get("librarian_instance")
    if libinstance:
        librarian_instance[1] = libinstance
        librarian_instance[2] = "Depends on instance"
    web_instances.append(librarian_instance)

    d = {"categories":["Name", "URL", "Maintainer", "Interface"],
         "size":[1,2,1,1],
         "data":web_instances}
    table(d)
    center("")

    # Choose an instance
    which = input(typing_dots())
    # Some web clients don't work with '#' in the URL
    web = url.replace("#", ":")
    try:
        center(web.replace("lbry://", web_instances[int(which)][1]))
    except:
        center(web.replace("lbry://", web_instances[0][1]))

def file_or_editor(args, comment, editor=None):
    # We gonna check if the user added anything after the command

    #    reply emacs
    #    reply gedit
    #    reply vim

    # Or something like

    #    reply /home/username/filename.txt
    #    reply /home/username/filename.md

    # That might be useful to input multiline text.
    import subprocess
    import os

    if editor:
        a = editor
    else:
        a = args

    a = os.path.expanduser(a)

    try:
        text = open(a, "r")
        text = text.read()
    except:
        a = a.split()
        text = open("/tmp/fastlbrycommentwriter.txt", "w")
        text.write(comment)
        text.close()

        subprocess.run([*a, "/tmp/fastlbrycommentwriter.txt"])

        center("Press Enter when the file is ready and saved.")
        input()

        text = open("/tmp/fastlbrycommentwriter.txt", "r")
        text = text.read()

    return text.rstrip()

def get_cn(c, prompt=""):

    # This gets a number from a command

    if " " in c:
        try:
            cn = int(c[c.find(" ")+1:])

        except:
            return 0
    else:
        cn = input(typing_dots(prompt))
        try:
            cn = int(cn)
        except:
            return 0
    return cn

def choose_license():
    lsnzs = []
    for i in licenses:
        lsnzs.append([i[0],i[2]])

    d = {"categories":["Name","Comment"],
            "size":[1,1],
            "data":lsnzs}
    table(d)
    center("---choose a license or press enter for custom---")
    lc = input(typing_dots())

    try:
        lselect = licenses[int(lc)]
        lname = lselect[0]
        llink = lselect[1]
    except:
        lname = input(typing_dots("License Name", give_space=True, to_add_dots=True))
        llink = input(typing_dots("License Link", give_space=True, to_add_dots=True))

    return lname, llink

def spdx_license(identifier):
    """Takes a string and returns the name and url of the license if it is in the SPDX license list, else it returns the identifier"""

    with open("flbry/licenses.json") as f:
        licenses = json.load(f)
    licenses = licenses["licenses"]

    for i, l in enumerate(licenses):
        if l["licenseId"] == identifier:
            lname = l["name"]
            llink = l["seeAlso"][0]

            # Warn the user if the license identifier is nonfree or not FSF libre
            if not "isFsfLibre" in l:
                if not l["isOsiApproved"]:
                    center("License is not free or open source", "bdrd")
                else:
                    center("License is OSI-approved but is not considered free by the FSF")

            return {"name": lname, "link": llink}

    return {"name": identifier}

flbry_globals = {
    "lbrynet": "flbry/lbrynet",
    "comment_api": "https://comments.odysee.com/api/v2",
}

def try_getting_git_commit():
    import subprocess

    try:
        ghash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().rstrip()
        center("Git commit hash: "+ghash)
    except Exception as e:
        # Git isn't installed
        center("Error getting commit hash: "+str(e), "bdrd")
        pass

def ruler_sideways(width, offset=0):

    w, h = tsize() # For reference, the 'width' value will be
                   # The actual width of the ruler. 'w' is used
                   # For rendering.


    # This one prints a sideways ruler giving each next column
    # a line number, skiping one space between the numbers like:

    # 0 2 4 6 8 10 13 16 19 21

    # First raw of the printout will be a simple rythmic pattern
    # similar to : |---------|---------|--------|--------|---------|

    pattern = "    "+clr["bdma"]+(" "*offset)+" "+clr["tbwh"]
    for i in range(width+1):
        a = " "
        if i % 10 == 0:
            a = "▒"
        elif i % 2 == 0:
            a = "░"
        pattern = pattern + a

    print(pattern+" "+clr["norm"])

    ret = " "*offset
    skipto = 0

    for i in range(width):
        if i == skipto:
            ret = ret + str(i) + " "
            skipto = i + len(str(i)) + 1

    ret = wdth(ret,w-10-len(str(width))-1)
    ret = ret + " " + str(width)


    print("    "+clr["bdma"],
          clr["bold"]+clr["tbwh"]+ret,
          clr["norm"])
