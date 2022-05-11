*This document will be a short manual of how to use the FastLBRY program. And how to contribute to it. It's not very hard to figure out the software yourself. The program provides `help` dialogues through out. This document is intended to ease your first experience with the program.*

# Installing

This program is not installed. It's simply unpacked and ready to go. We are doing it for multiple reasons. One is that it's easier to maintain this way. Second, it's easier to update for the user. And third it's easier for the user to make modifications to it.

In the main folder you can see the file called `run.py`. This is the main python file that you need to run. Open the terminal, navigate to this folder and type:

`python3 run.py`

This should launch the program. 

# Connecting to LBRY

As soon as you enter, you need to connect to LBRY. If you have an LBRY Desktop instance running. The LBRY is already connected on your system. So you don't need to do anything. You can type `help` to see currently available functions.

If you are not connected, type `connect` and wait for a little bit. You can type `search` and search for something on the LBRY network to check if the LBRY is ready. If not, it will tell you to wait a bit longer.

# Login

At the moment login features are not yet implemented. But you can log in. For this I will need to explain you how the lbrynet SDK thing works.

Usually in a folder `~/.config/lbry` you can find configuration files for the lbrynet SDK. They are configurable using the SDK or using LBRY Desktop. Basically any client that uses the official SDK will share it's configurations with any other such client.

So in order to log in you may use any other client ( using official SDK ) that has a function to log in. For example the LBRY Desktop. And then if you come back into FastLBRY. You will be logged in. 

As soon as I will implement login inside FastLBRY I gonna edit this section.

# Playing videos and other files

When you search for a publication either by `search` or in any other way. You can do a multitude of things with it. For example you can get the `https` link to the publication. Or send this `https` links directly to a program using `open <program_name>`. So for example `open vlc` will launch the video in VLC using the `https` link to it.

On the other hand you might want to use `play` or `save` to get the file downloaded. Play will also play the file. Note that the SDK does not wait till the file will be fully downloaded if it's a stream type file. It will save the file in the configured folder ( see Login ) and then simply launch it with the default player. It will keep downloading the file on the background until it's done downloading, or until you close the SDK.

Note: For play and save to work, your configuration ( see Login ) should allow files to be downloaded. If it's set not to download files, it will not work. You can use the `open` feature instead to stream the file without downloading it.

# Reporting bugs

The issues page for reporting bugs is:

https://notabug.org/jyamihud/FastLBRY-terminal/issues

You will need to have a notabug.org account. It takes only a few seconds to sign up. And the functionality to report a bug will not require confirming the email address ( as of now ). It's still worth making a full account with avatar and username configured properly. And I would recommend to migrate all your Github repositories to notabug.org since it's not controlled by Microsoft. And is just a better overall platform.

Alternatively you can complaint to the users / developers Matrix chat:

`#FastLBRY:matrix.org`

# Contributing

We need people to contribute to the project. Since I'm alone for now. And I can't just sit here all day hacking on the SDK. I have other projects that are not less important. And for a few last days, I was not doing them, since I was hacking this program together. 

The main file is the `run.py` file. And elements that are loaded separately to interact with the SDK are in the `flbry` folder. Also there is the `lbrynet` binary executable. The source code of which you can find here:

https://github.com/lbryio/lbry-sdk

You can navigate to the `flbry` folder from a separate terminal and use `./lbrynet --help` command to see what stuff you can input into it. This way I was able to put together the program so far. 

The outputs of the SDK are in JSON format. I capture them using `subprocess.check_output()` functions and then parse using `json`. It's quite simple. But sometimes it gives weird data that the script needs to handle somehow. 

Please read the scrips carefully before making modifications to them. 
