Plugins and Extensions are good ways for users to modify software without necessarily knowing how. They will get a plugin and install it on the software. This document explains how to install / built plugins for FastLBRY Terminal.

# Command for plugins dialog

To simply switch plugins on and off, type the number of the plugin.

**help**

Returns this file.

**read**

Shows Source Code of a given plugin.

Example :: read 1

**set**

Runs a settings function with in the plugin if it has such a function.

Example :: set 1

**publish**

Helps you publish the plugin to LBRY using the [plugin publishing system.](../help/publish_plugins.md)

Example :: publish 1

**description**

Shows description for a given plugin.

Example :: description 1

# Install Plugins

Until there will be ways to install them in a more natural way ( maybe using a plugin installer plugin ) you will have to do this manually. And knowing how to do that manually is important. You don't know what kinds of things can happen to you. So any knowledge is good.

Plugins are stored in your settings directory. Usually it's at:
`~/.local/share/flbry/plugins/`. The plugin could be one or many python scripts that you will need to copy into that folder. If the folder is not there yet, make one.

As soon as it's there, it will start functioning. Whether adding commands to existing prompts, or editing some data passed around the software.

# Ignoring plugins

A list or regular expressions for plugins to be ignored, seperated by newlines, can be put into the `pluginignore` file in the FastLBRY settings directory (usually `~/.local/share/flbry/pluginignore`).
To ignore a certain expression (commenting it out), start the line with a `#`. To start a regular expression with a `#`, start the line with `\#` instead.
The regular expressions should match the name of the plugin file you want to ignore without the `.py` at the end. That is, if you want to ignore the file `example.py`, use the expression `example`.

Here is an example `pluginignore` file, with comments showing what each line does:
```
# Matches plugins titled one or more 'a's
# E.g. "a", "aa", "aaa", and so on
a+

# Matches plugin names that start with one or more or either 'b' or 'c'
# E.g. "b", "bb", "bba", "c", "cc", "cca", and so on
[bc]+.*

# Matches plugin names that start with "example"
# E.g. "example", "examplea", "exampleb", and so on
example.*

# Matches the plugin named "template", and nothing else
template

# Matches plugin names beginning with "#"
\#.*
```

# Making plugins

To make plugins you will need a template. Here is one:

```
# This is a Test Plugin for FastLBRY Terminal.
# (c) J.Y.Amihud 2021 - under GNU GPLv3 or any later version.

import time
from flbry.variables import *

def filter_function(args):

    # This function will replace every instance of "Help" with
    # the words "Test Change" in all markdown files.
    
    args[1] = args[1].replace("Help", "Test Change")
    return args

def added_function(command, args):

    # This is a function will print some progress bar

    print()
    for i in range(10):
        progress_bar(i, 10, "Test Plugin")
        time.sleep(1)
    progress_bar(10, 10, "Test done!")
    print()

# This is the data that the plugin module reads. 
plugin_data = {
    "title":"Test Plugin",
    "author":"J.Y.Amihud",
    "license":"GNU GPLv3 or later",
    "flbry":"terminal",
    "functions":[
        {   "command":False,
            "flbry.markdown.Open":filter_function},
        {   "command":"Test_Plugin",
            "main":added_function}]}

```

It's very important to have a dictionary object with the name of `plugin_data` as shown above. Reading this variable, FastLBRY plugin system will know what plugins to run where. And whether they have added some new commands to the existing prompts.

# Publishing Plugins

You can publish them manually or use the [plugin publishing system.](../help/publish_plugins.md)

# Plugin API

As you can see in the top example, it does some weird things. For example `filter_function` is assigned to `flbry.markdown.Open`. This is the address. Through out the software there will be multiple places where such addresses will be added. 

The format in which the data is received should be kept and returned in the same order. Your plugin can modify the data and returned modified version. or do something else with this data. But returning of the data should be done regardless.

Let's look at the list of those implemented already:

**main** *not command*

Running on very return to main. Has no arguments.


**main** *command*

```
command : str
```

If the user inputted a command that does not exist in FastLBRY yet, it will look for plugins that have this command. The example plugin shows how to use `main` address very well.

**settings** *not command*

This function is called for a specific file when the user wants to set it up. It has no arguments. The settings system should be developed by the plugin developer. This is just a short cut where the user will look for settings.

**flbry.markdown.Open** *not command*

```
filename      : str
raw_file_text : str
```

This is running inside the markdown parses as soon as it opened the file. So you could edit any of the raw file data before parsing it. It will be done on each file. Unless your plugin will handle some exceptions.

*This only works with the default markdown reader. You most likely want to use flbry.markdown.draw so it works in all markdown readers.*

**flbry.markdown.draw** *not command*

```
filename      : str
raw_file_text : str
```

This has the same functionality as **flbry.markdown.Open**, except it runs before anything reads the file. This allows it to work with custom markdown readers as well as the default markdown reader integrated into the program. Using this is preferable to using **flbry.markdown.Open**.

**flbry.markdown.draw_default** *command*

```
md       : list
links    : list
filename : str
title    : str
```

Adds a command to the default markdown reader. It gives the full parsed markdown of the file, the links in the file, the filename, and the title of the file.

**flbry.url.get** *not command*

```
out : dict
```

This one is running right after the resolve of the url. And it's giving you the resolved dictionary data as revieced from the LBRY SDK.

**flbry.url.get** *command*

```
out : dict
```

This one is adding a command into url commands. It has a slightly different 'out' dictionary. The 'resolve' in the SDK can resolve more then one LBRY address in the same time. And thus it gives you a list of addresses. But since it's url, we just give the first ( and only ) address data.

**flbry.publish.configure** *command*

```
data : dict
```

This is adding a function into publishing dialog when you edit things like title and thumbnail for a new publication. The 'data' is the configuration thus far.

**flbry.publish.upload** *not command*

```
data : dict
```

This runs at publish on every publish. The data is the configuration of the publish.

*Please if you see missing API addresses, add them here.*
