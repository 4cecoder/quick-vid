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

import os
from flbry.variables import *
from subprocess import *
from flbry import settings
from flbry import plugin
from flbry import url


################################################################################

# Markdown. Or .md file format is an easy way to give your simple text documents
# a bit of flare. Stuff like links, images and quotes are supported. Also bold
# an italic characters.



def Open(filename):


    # This function will parse a Markdown (.md) file into a readable python
    # dictionary object. That you can use for various things.

    try:
            md = open(filename)
            md = md.read()

    except:

        center("Failed to load the article!!!", "bdrd")
        return

    # After we read the file, we gonna call for all plugins
    # that will do something with the file data.
    filename, md = plugin.run([filename, md])

    # Spliting it for the read.
    md = md.split("\n")

    # First thing is I was to read the headings and convert it into a tree.


    tree = []
    indent = 1
    c = []

    skip = 0

    for n,line in enumerate(md):

        if skip > n:
            continue

        ty = "text"
        te = line

        # Here I want to simply get a type of each line. Later we going to parse
        # the links and other things. But first. Let's parse stuff based on
        # lines.

        if line.startswith("```"):

            # THREE ``` aka code block

            # This tag will block any other tags
            # untill it's untagged

            code = ""

            for l in md[n+1:]:
                if not l.startswith("```"):
                    code = code + l + "\n"

                else:
                    skip = n + code.count("\n") + 2
                    break

            tree.append(["text_c", code+"\n"])
            te = ""

        elif line.startswith("#"):
            # The titles of the chapter. The Headers are usually written similar
            # to how here in python you write comments. It's a # , space, and the
            # text.

            # The amount of hashes. ## or ### gives different sized text. Officialy
            # it should support up to 6 hashes. ######. But why not make it more
            # just in case.

            ty = line.count("#") # This might give bugs

        elif line.startswith(">"):

            # The > sign in the Markdown language is used for quatations.

            ty = "text_c"

        tree.append([ty, te+"\n"])

    # Now the stage 0 is over and we parsed the basic things. Now is the hard
    # part to parse out all the images and stuff inside them. It's going to be
    # done per part. And we are going to use the same technique I used for the
    # conversion of the legacy projects. See : studio/story.py ( in VCStudio )

    # We are going to itterate over each letter. And decide what to do by that

    newtree = []

    for block in tree:

        if block[0] == "text_c":
            newtree.append(block)
            continue

        part = ""
        skip = 0

        for n, l in enumerate(block[-1]):

            if skip > n:
                continue

            part = part + l

            # Here we are going to do something if a give condition is met.
            # Usually I gonna do something if [part] ends with a given markdown
            # thing. I don't have a manual of markdown on me. So please make it
            # more supported. I guess. I might forget things I rarely use.

            # Links are made with [stuff you click on](https://example.com)
            # but similar to it. Images are done ![Tooltip](Image.png)
            # and even weirder you can put one into the other. Like
            # [![Tooltip](Image.png)](https://example.com)
            # Which going to give you a clickable image.

            # For this version what we are going to do is next.
            # If we got [![ then it's a clickable image
            # If we got ![ then it's just image
            # and if we got [ then it's a link.

            if part.endswith("[!["):

                # IMAGE LINK
                newtree.append([block[0], part[:-3]])

                tooltip = ""
                imageurl = ""
                url = ""
                t = False
                iu = False
                skip = n
                for le in block[-1][n:]: # For letters in the rest of text

                    skip = skip + 1

                    if le == "]":
                        t = True
                    elif le == ")" and t and not iu:
                        iu = True
                    elif le == ")" and t and iu:
                        break
                    elif not t:
                        tooltip = tooltip +le
                    elif t and not iu:
                        imageurl = imageurl + le
                    else:
                        url = url+le

                tooltip = tooltip[tooltip.find("[")+1:]
                imageurl = imageurl[imageurl.find("(")+1:]
                url = url[url.find("(")+1:]

                apnd = ["image", "[IMAGE_", imageurl]

                newtree.append(apnd)

                apnd = ["link", "_LINK]", url]

                newtree.append(apnd)

                part = ""


            elif part.endswith("!["):

                # IMAGE

                newtree.append([block[0], part[:-2]])

                tooltip = ""
                url = ""
                t = False
                skip = n
                for le in block[-1][n:]: # For letters in the rest of text

                    skip = skip + 1

                    if le == "]":
                        t = True
                    elif le == ")" and t:
                        break
                    elif not t:
                        tooltip = tooltip +le
                    else:
                        url = url+le

                tooltip = tooltip[tooltip.find("[")+1:]
                url = url[url.find("(")+1:]

                apnd = ["image", "[IMAGE]", url]
                newtree.append(apnd)

                part = ""


            elif part.endswith("[") and not block[-1][n:].startswith('[!['):

                # LINK
                newtree.append([block[0], part[:-1]])


                tooltip = ""
                url = ""
                t = False
                skip = n
                for le in block[-1][n:]: # For letters in the rest of text

                    skip = skip + 1

                    if le == "]":
                        t = True
                    elif le == ")" and t:
                        break
                    elif not t:
                        tooltip = tooltip +le
                    else:
                        url = url+le

                tooltip = tooltip[tooltip.find("[")+1:]
                url = url[url.find("(")+1:]

                apnd = ["link", tooltip, url]
                newtree.append(apnd)

                part = ""



            # Now I want to deal with `, *, ** and ***. If you want to help me you
            # can implement other types. Such as _, __, ___ and so on. Markdown is
            # a very rich language. I'm going to use the cut down version I see other
            # people use.

            # BTW this is the time. Feb 28. When I switched from Gedit to GNU Emacs.
            # Interesting feeling using this programm. I kind a love it even tho
            # so many stuff in not intuitive. Like saving is not Ctrl - S but
            # Ctrl - X -> Ctrl - S.

            # Things like Alt-; to comment multiple lines at ones is HUGE. Also it
            # was built by programmers for programmers. So it's a very good tool.

            elif part.endswith("**") and not block[-1][n+2:].startswith('*'):

                # DOUBLE **

                newtree.append([block[0], part[:-2]])

                if block[0] == "text":
                    block[0] = "text_b"
                else:
                    block[0] = "text"

                part = ""

            elif part.endswith("*") and not block[-1][n+1:].startswith('*'):

                # SINGLE *

                newtree.append([block[0], part[:-1]])

                if block[0] == "text":
                    block[0] = "text_i"
                else:
                    block[0] = "text"

                part = ""


            elif part.endswith("`"):

                # SINGLE `

                newtree.append([block[0], part[:-1]])

                tmpart = block[-1][n+1:]
                tmpart = tmpart[:tmpart.find("`")]

                newtree.append(["text_c", tmpart])

                skip = n+len(tmpart)+2
                
                block[0] = "text"

                part = ""

        newtree.append([block[0], part])

    w,h = tsize()
    newtree.append(["text", "\n"*h])
    tree = newtree

    return(tree)

def search_convert(s):

    # This function convers a chapter name into a link
    # such links are use in notabug.org to link to chapters
    # for example example.com/file.md#chapter-name
    # With this url it will load the example.com/file.md and
    # then skip to the "Chapter Name" chapter.

    # This function transforms "Chapter Name" into "chapter-name"

    l = " ./\|[]{}()?!@#$%^&*`~:;'\"=,<>"
    s = s.lower().replace(" ","-")
    r = ""
    for i in s:
        if i not in l:
            r = r + i
    return r

def draw(filename, title, convert=True):
    # Write the file to a temporary file so plugins can modify it
    with open(filename) as f:
        md = f.read()

    filename, md = plugin.run([filename, md])

    filename = "/tmp/fastlbrymarkdownreader.md"
    with open(filename, "w") as f:
        f.write(md)

    if settings.get("markdown_reader"):
        os.system(settings.get("markdown_reader") + " " + filename)
    else:
        draw_default(filename, title, convert)

def draw_default(filename, title, convert=True):
    ###########

    # THE FOLLOWING CODE IS VERY DIRTY. I WAS RUNNING OUT OF TIME WHILE IMPLEMENTING
    # IT. PLEASE SEE WHAT CAN BE DONE ABOUT IT. I THINK SOMEBODY NEEDS TO HACK
    # COMMENTS TO IT. SINCE IT COULD BE CONFUSING AS HELL...

    ##########

    # Getting size of the terminal
    try:
        import os
        w, l = os.get_terminal_size()
        if not w % 2: # to solve the tearing when it's a weird amount
            w = w - 1
        l = l - 5
        w = w - 8

    except:
        w = 89 # The width of the frame
        l = 20 # Total lines amount possible.


    # First we want to parse the article
    if convert:
        md = Open(filename)
    else:
        mdf = open(filename)
        mdf = mdf.read()
        mdf = mdf.split("\n")
        md = []
        for i in mdf:
            md.append(["text", i+"\n"])
        md.append(["text", "\n"*l])

    # Now we want to print what we have

    # Top banner thingy. Purple with the name of the article.


    # Title line
    center(title)

    pline = ""
    lenis = 0
    linen = 0

    colors = {
        "text":clr["norm"]+clr["tbwh"]+clr["bdbu"],
        "text_b":clr["norm"]+clr["bold"]+clr["tbwh"]+clr["bdbu"],
        "text_i":clr["norm"]+clr["ital"]+clr["tbwh"]+clr["bdbu"],
        "text_c":clr["norm"]+clr["tbwh"]+clr["bdgr"],
        "link":clr["norm"]+clr["tbwh"]+clr["bdma"],
        "image":clr["norm"]+clr["tbwh"]+clr["bdcy"]
    }

    # Let's store all the links that the user might want to use

    links = []
    linkn = 0
    linkw = False

    for part in md:
        if part[0] in [1,2,3,4,5,6,7]: # Header, similar to <h1> or <h2> in html
             center(part[1].replace("\n", "").replace("#", ""), "bdcy")
             linen = linen + 1

        elif part[1].startswith("---") or part[1].startswith("___"): # The <hr> horrizontal line
             center("═"*(w-12), "bdbu")
             linen = linen + 1

        elif part[0] in ["text", "text_b", "text_c", "text_i", "link", "image"]: # Text that must be wrapped


            if linkw:
                # The number of the link
                pline = pline  + clr["bbma"] + wdth(linkn, 4) + " "
                linkn = linkn + 1
                lenis = lenis + 5
                linkw = False

            pline = pline + colors[part[0]]

            for num, letter in enumerate(part[1]):
              br = False
              rest = part[1][num:] # all the rest of the part
              if letter not in [" ", "\n"]:
                  pline = pline +  letter
                  lenis = lenis + 1

                  if part[0] in ["link", "image"] and part[2] not in links:
                      links.append(part[2])
                      linkw = True

              # TODO: There has to be a break when there is a too-large string
              # With freaquant spaces it looks right. But it doesn't break for
              # words that are larger then the frame.
                      
              elif letter == " ": # At a brake

                  # This code seems reasonable for text with small enough words
                  if not lenis > w - 20 - len(rest[:rest.replace(" ","_",1).find(" ")]):
                      pline = pline + " "
                      lenis = lenis + 1
                  else:
                      br = True
              elif letter == "\n":
                  br = True


              if br: # At line-brake
                  print("    "+clr["bdbu"]+"      "+pline+clr["bdbu"]+wdth("", w-lenis-6)+clr["norm"])
                  pline = colors[part[0]]
                  lenis = 0
                  linen = linen + 1

                  # If reached the line number

                  # TODO: To remove the dependancy on 20+ new lines the following code should be done
                  # as a function. And run in two places. Here and after the end of the loop.
                  
                  if linen >= l:
                      center("---type 'more' to continue reading it--- ")

                      complete(["more"])

                      while True:
                          plugin.run(execute=False)
                          c = input(typing_dots())
                          if not c:
                              return

                          if c != "more":
                              try:
                                  c = int(c)
                              except:
                                  pass

                              if type(c) == type(10):
                                  # Pass the link to the link parser
                                  link_open(links[c], filename)

                              else:
                                  md, links, filename, title = plugin.run([md, links, filename, title], command=c)

                          elif c == "more":
                              links = []
                              linkn = 0
                              linkw = False
                              linen = 0
                              center(title)

                              break

def link_open(link, start_from=""):

    # This function will decide what to do with links.

    ####### TRY TO LOAD A LOCAL FILE FIRST #######


    local_link = link

    if not link.startswith("/"):
        start_from = start_from.replace(os.getcwd(), "")
        if not link.startswith("../"):
            local_link = os.getcwd()+"/"+start_from[:start_from.rfind("/")+1]+link
        else:
            local_link = os.getcwd()+"/"+start_from
            for i in range(link.count("../")+1):
                local_link = local_link[:local_link.rfind("/")-1]
            local_link = local_link + '/' + link.replace("../", "")

    if os.path.exists(local_link):
        try:
            # Testing if it's a text
            open(local_link)
            if local_link.endswith(".md"):
                draw(local_link, local_link)
            else:
                draw(local_link, local_link , False)
        except Exception as e:
            #print(e)
            Popen(['xdg-open',
                   local_link],
                  stdout=DEVNULL,
                  stderr=STDOUT)
        return

    ########## TRY TO LOAD AN LBRY LINK ##############

    # TODO : This part confuses me. Something is wrong. Some good
    #        links just break the url.get() function and I don't
    #        understand what the hell is going on.

    try:
        if url.get(link, False): # If it fails, it will return the error message
            print("    "+link)
    except:
        print("    "+link)
