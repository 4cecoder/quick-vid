This document will explain some decisions made while making this application and the result it had on support for certain operating systems. Probably, since you are reading this document, you have an issue of not being able to use certain function on your operating system.

When I announced this project to the public I said:

> For those who complaint about this program not being portable enough. This is intentional. I am intentionally trying to make it NOT WORK on anything but GNU / Linux. The source code is available. So you can fork it and make it work for you. I'm not going to do this myself. Thanks...

This decision was made primarily as a response to some proprietary software developers trying to lock users into their ecosystem. So I want to act like a douche-bag and do the exact opposite. I will make the software editable ( [Free Software](https://notabug.org/jyamihud/VCStudio/src/master/wiki/extra/FreeSoftware.md) ) so people could potentially use it on systems that I don't like. But in the same time, I personally will not make it work. Though if you will pull request me with a modification that allows this program to run on more platforms. I will not disregard it immediately.

# GNU / Linux

This software should work just fine on a variant of GNU / Linux. If you have hardware that is not supported by a [100% free operating system](https://gnu.org/distros), you may still take a first step and use something like *GNU/*[LinuxMint](https://linuxmint.com/), or [Pop!_OS](https://pop.system76.com/). But keep in mind that it's just a first step. The ultimate goal is 100% user freedom.

# BSD

I was told that on BSD type systems the application (FastLBRY) runs just fine. But I can't tell you for sure, since it's a slightly different design of an operating system and it uses a different kernel. Please report bugs if you use BSD and I broke something for you. I have nothing against BSD since it's Free Software as well.

# Windows

This program will probably hate Windows the most. Since the architecture of Windows is very different from the architecture of a normal operating system. For instance the LBRY SDK that we are using is built for GNU / Linux. You will probably need to swap it with the Windows version of it to make it work. And then also swap all it's mentions in the code to the name of your SDK (adding the ".exe" thing in the end).

# MacOS / iOS

People think that MacOS is better than Windows since at least it's not Windows. But unfortunately MacOS is worse than Windows. Apple is the most Freedom disrespecting tech company out there. They don't even allow you to repair your own devices.

People think that MacOS is somehow good because it shares some of the source code with BSD which is Free Software. But unfortunately BSD decided not to copyleft it. Thus allowing Apple to take their source code, make fully proprietary MacOS from it and continue disrespecting users freedom.

About whether the software works on MacOS, since it does work on BSD, I don't know. Apple probably have done a bunch of changes to the operating system. Including changes that probably broke some comparability with the software on some level. I still never had a single person telling me about their experience with it on MacOS.

# Other Systems

The world is full of interesting operating systems. Like Serenity OS, Temple OS, Haiku, ReactOS, CP/M, DOS, UNIX, Chrome OS and more. Some of them are more free while others disrespect you by including non free software. And I cannot predict how the software will react to those operating systems. So you are probably on your own there.

# Don't be sad.

If you can't, for some reason to free yourself just yet. You may find a person knowledgeable about this software enough, to modify it for your system on our matrix chat `FastLBRY:matrix.org`. Go there and ask. 

Alternatively you can modify the software yourself. Don't be afraid to read the source code. And don't be afraid to make changes in it. Finally you can just re-download the repository if you make too many bad modifications.
