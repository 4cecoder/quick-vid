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

# This file with handle various analytics. Currently in LBRY Desktop
# or Odysee.com, the analytics are very basic, while they have a very
# rich SDK that allows to get all kinds of information about transactions.
# This transaction data is useful to get various Analytics.

from subprocess import *
import json
import time

from flbry import url
from flbry import settings
from flbry import markdown
from flbry import channel
from flbry.variables import *

def graph(data=[]):

    # This function will draw a graph. I wanted originally to make it a
    # part of variables.py, but I'm afraid it will be a huge function.
    # And it makes a lot of sense to put it here (in Analytics).

    # Concept art:

    # 2021-11-15  --------------------------------------> 2021-12-30
    #0 2 4 6 8 10 13 16 19 22 25 28 31 34 37 40 43 46 49 .... 100 104
    #
    #           #
    #           #
    #           #         #           #                 #            #
    #           #       ###    #      ##  #       #     #      #     #
    #  #       ##      ######  #     ####### #   ##    ###    ##   # #
    #  #  #    ### ########### ### # #########  ###   #####  ###  ####
    # #################################################### ###########
    # ################################################################

    if not data:
        center("No Data!", "bdrd")
        return {0:[]}
    if len(data) == 1:
        center("Only one entry! Cannot draw graph!", "bdrd")
        return {0:data}

    w, h = tsize()

    height = h - 7
    width = w - 16
    
    times = []
    values = []

    for i in data:
        times.append(i["timestamp"])
        try:
            values.append(float(i["amount"]))
        except:
            values.append(0)

    #for i in times:
    #    print(i)
    # Finding times
    import time
    startdate = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime( min(times)) )
    enddate  =  time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime( max(times)))

    center(startdate+" "+("-"*(width-(len(startdate)+len(enddate))-6))+"> "+enddate)

    
    # Times minus the amount of the first entry
    ctimes = []
    for i in times:
        ctimes.append(i-min(times))


    # LET'S START DRAWING


    p = []
    for i in ctimes:
        pix = round((width-1)/max(ctimes)*i)
        p.append(pix)

    ap = []
    ret_data = {}
    for i in range(width):
        count = 0
        for n, d in enumerate(p):
            if d == i:
                count = count + values[n]
                if d not in ret_data:
                    ret_data[d] = []
                ret_data[d].append(data[n])
        ap.append(count)

    choice = " ░▒▓█"
    if settings.get("graph_force_ASCII"):
        choice = " .~8#"

    for i in reversed(range(height)):

        va = max(ap) * ((i+1)/(height-1))

        s = clr["bdma"]+" "+clr["tbwh"]+wdth(va, 5)+" "


        for b in ap:
            x = ((height-1)/max(ap)*b)

            c = max(min(round((x - i)*4), 4), 0)

            y = choice[c]
            s = s +  clr["bdbu"]+clr["tbwh"]+y


        print("    "+s+clr["bdma"]+" "+clr["norm"])

    center(" ")
    # Here I want to print a sideways ruler
    ruler_sideways(width-1, 6)
    center(" ")

    return ret_data

def graph_loop(items):

    to_make = True
    while True:
        # parts of the graph's data indexed to the column on the graph
        parts = graph(items)
    
        # commands
        c = input(typing_dots("Type 'help' for graph commands.", to_make))
        to_make = False

        if not c:
            break

        # Showing minimum data ( similar to raw, but with a lot less stuff )
        elif c == "numbers":
            data_print = {"categories": ["Time", "Amount"],
                          "size":[2,1],
                          "data":[]}
            for i in parts:
                for b in parts[i]:
                    try:
                        amount = b["amount"]
                    except:
                        amount = "[NO AMOUNT]"
                    try:
                        import time
                        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(b["timestamp"])  )
                    except:
                        timestamp = "[NO TIME DATA]"
                    data_print["data"].append([timestamp, amount])

            print()
            table(data_print, False)
            center("")
            input()
            print()
        
        # Zooming in the Graph
        elif c.startswith("zoom"):
            try:
                if " " in c:
                    n = c[c.find(" ")+1:]
                else:
                    n = input(typing_dots("Number if a range?"))

                # if it's a range
                if " " in n:
                    nr = n.split()
                    nrange = []
                    
                    for i in nr:
                        nrange.append(int(i))

                    zoom_data = []    
                    for i in range(nrange[0], nrange[-1]+1):
                        if i in parts:
                            for d in parts[i]:
                                zoom_data.append(d)
                        
                    graph_loop(zoom_data)
                else:
                    try:
                        graph_loop(parts[int(n)])
                    except:
                        graph_loop([])
            except Exception as e:
                center("Error: "+str(e), "bdrd")

        # Printing the Raw data into the terminal
        elif c == "raw":

            size = [1,4]
            for i in range(len(parts[0][0].keys())-2):
                size.append(2)

            categories = list(parts[0][0].keys())
            
            data_print = {"categories": categories,
                          "size":size,
                          "data":[]}
            for i in parts:
                for b in parts[i]:
                    if list(b.keys()) != categories:
                        
                        print()
                        table(data_print, False)
                        center("")
                        
                        categories = list(b.keys())
                        size = [1,4]
                        for i in range(len(b.keys())-2):
                            size.append(2)
                        data_print = {"categories": categories,
                          "size":size,
                          "data":[]}
                        
                    ap = list(b.values())
                    if len(ap) < len(size):
                        for dif in range(len(size) - len(ap)):
                            ap.append(None)
                    data_print["data"].append(ap)
            print()
            table(data_print, False)
            center("")
            input()
            print()

        # Output a CSV file.
        elif c == "csv":

            def to_csv_string(data):
                ret = ""
                for n, i in enumerate(data):
                    if n == 0:
                        comma = ""
                    else:
                        comma = ","
                    if type(i) in [int,float,bool,str]:
                        ret = ret + comma + '"'+str(i).replace('"', '""')+'"'
                    else:
                        ret = ret + comma + '"[COMPLEX DATA]"'
                return ret
            
            text = to_csv_string(parts[0][0].keys())
            keys = text
            for i in parts:
                for b in parts[i]:
                    if to_csv_string(b.keys()) != keys:
                        keys = to_csv_string(b.keys())
                        text = text + "\n\n"+ keys
                    text = text + "\n" + to_csv_string(b.values())

            saving = open("/tmp/fast_lbry_csv_tempfile.csv", 'w')
            saving.write(text)
            saving.close()
            Popen(["xdg-open",
                        "/tmp/fast_lbry_csv_tempfile.csv"],
                                stdout=DEVNULL,
                                stderr=STDOUT)
        # Saving graph    
        elif c == "save":
            itemsjson = []
            for i in parts:
                for b in parts[i]:
                    itemsjson.append(b)
            filename = settings.get_settings_folder(flbry="flbry/graphs")
            from datetime import datetime
            now = datetime.now()
            filename = filename + "/" + str(now.strftime("%Y-%m-%d_%H:%M:%S")) + ".json"

            note = input(typing_dots("Note?"))
            savedata = {"note":note, "items":itemsjson}

            with open(filename, 'w') as f:
                json.dump(savedata, f, indent=4)
            
            center("Saved to :"+ filename)
            input()

            
        elif c == "help":
            
            markdown.draw("help/graph.md", "Graph Help")
                    
def get_data(claim_id="", total=0, mode="sales"):

    # This function will actually load data from
    # a given claim_id

    if not total:
        command = [flbry_globals["lbrynet"],
                        "txo", "list",
                   "--exclude_internal_transfers",
                   "--is_not_my_input",
                        "--page_size=1"]
        if mode == "sales":
            command.append("--type=purchase")
        if claim_id:
            command.append("--claim_id="+claim_id)
        txo = check_output(command)
        try:
            txo = json.loads(txo)
        except:
            center("Connect to LBRY first.")
            return
        total = txo["total_items"]
    
    cpage = 1
    items = []
    total_total = total
    print()
    while total > 0:

        progress_bar(total_total-total, total_total, "Getting "+mode+" data...")

        
        command = [flbry_globals["lbrynet"],
                        "txo", "list",
                   "--page_size=50",
                   "--exclude_internal_transfers",
                   "--is_not_my_input",
                   "--page="+str(cpage)]
        if mode == "sales":
            command.append("--type=purchase")
        if claim_id:
            command.append("--claim_id="+claim_id)
        txo = check_output(command)
        try:
            txo = json.loads(txo)
        except:
            center("Connect to LBRY first.")
            return
        cpage = cpage + 1
        for i in txo["items"]:
            items.append(i)
        total = total - 50

    progress_bar(total_total, total_total, "Done.")

    print()
    return items

        
def sales(mode="sales"):

    # This function will show sales of non-gratis publications.


    # First let's get the list of our channels
    out = check_output([flbry_globals["lbrynet"],
                         "channel", "list"])

    try:
        out = json.loads(out)
    except:
        center("Connect to LBRY first.")
        return
    channels = []
    for i in out["items"]:
        channels.append(i["claim_id"])

    page = 1
    cached = 0 # Page that was loaded last

    while True:

        w, h = tsize()

        page_size =  h - 5


        command = [flbry_globals["lbrynet"],
                   "claim", "search",
                   "--remove_duplicates",
                    '--order_by=release_time',
                   '--page='+str(page),
                   '--page_size='+str(page_size)]
        if mode == "sales":
            command.append('--fee_amount=>0')

        for i in channels:
            command.append("--channel_ids="+i)

        if page != cached:
            list_of_publications = check_output(command)
            try:
                list_of_publications = json.loads(list_of_publications)
            except:
                center("Connect to LBRY first.")
                return

            if mode == "sales":
                data_print = {"categories":["Publication", "Price", "Sold Copies"],
                          "size":[5,1,1],
                          "data":[]}
            else:
                data_print = {"categories":["Publication", "Supported Times"],
                          "size":[5,2],
                          "data":[]}
            print()
            for n, i in enumerate(list_of_publications["items"]):



                name = i["name"]
                try:
                    name = i["value"]["title"]
                except:
                    pass
                #print( name )

                price = 0
                try:
                    price = i["value"]["fee"]["amount"]
                except:
                    pass
                #print(price)

                progress_bar(n+1, len(list_of_publications["items"]), "Fetching: "+name)

                # Now lets get the amount of entries in txo
                command = [flbry_globals["lbrynet"],
                                "txo", "list",
                                "--claim_id="+i["claim_id"],
                           "--exclude_internal_transfers",
                           "--is_not_my_input",
                                "--page_size=1"]
                if mode == "sales":
                    command.append("--type=purchase")
                txo = check_output(command)
                try:
                    txo = json.loads(txo)
                except:
                    center("Connect to LBRY first.")
                    return

                sold = 0
                try:
                    sold = txo["total_items"]
                except:
                    pass
                #print(sold)
                if mode == "sales":
                    data_print["data"].append([name, price, sold])
                else:
                    data_print["data"].append([name, sold])

            print()
        table(data_print)
        cached = page
        center("---type 'more' to load more---")

        # Now the 'more' and such.

        c = input(typing_dots())
        if not c:
            break

        # TODO: Please test that this even works.
        if c == "more":
            page = page + 1

        else:
            try:
                c = int(c)
                total = data_print["data"][c][-1]
                i = list_of_publications["items"][c]
                try:
                    
                    items = get_data(i["claim_id"], total, mode)
                    graph_loop(items)
                except Exception as e:
                    print(e)

                print()
                
            except:
                pass

def load_graph_from_file():

    # This function will load cached graphs back into the terminal.

    folder = settings.get_settings_folder(flbry="flbry/graphs")
    while True:
        data_print = {"categories": ["Note", "Size", "Saving Time"],
                      "size":[4,1,2],
                      "data":[]}
        graphs = []
        for graph in os.listdir(folder):
            if graph.endswith(".json"):
                date = graph.replace(".json", "").replace("_", " ")

                with open(folder+"/"+graph) as f:
                    json_data= json.load(f)

                try:
                    note = json_data["note"]
                except:
                    note = ""

                try:
                    items = json_data["items"]
                except:
                    items = []
                graphs.append(items)
                data_print["data"].append([note,len(items), date])

        print()
        table(data_print)
        center("")
        print()

        c = input(typing_dots("Select graph number."))

        if not c:
            break

        try:
            graph_loop(graphs[int(c)])
        except:
            center("Something's wrong!", "bdrd")
            
            
    
