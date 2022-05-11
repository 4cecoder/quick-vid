This is the **HELP** dialogue for practical users of the software. This help dialogue is for the main menu. Not for all dialogues. Some dialogues will tell you that they have their own **help** pages.

To resolve an `lbry://` url you can just type it as a command. It will be automatically resolved. If it will fail to resolve the url, it will automatically search for it. It is advised though, to use **search** instead of searching this way. Since a lot of words already are taken as resolvable `lbry://` urls.

# Help & Contribution

**help**

Returns this help page. In other places in the program, you may find separate **help** dialogues. If you have only 1 : in the input line. It means you are in the start of the program. In it's main menu, so to speak. If you see :: or ::: or more, it means you are deeper. And each level might have it's own **help** dialog. 

*To move back one layer, like from ::: to :: you can simply press Enter without typing anything.*

**exit**

Exit the program. And also disconnect the currently running LBRY SDK. **NOTE: This will disconnect all other instances of the SDK. Like for example, if you have LBRY Desktop running. It will close it's connection too.** 

**quit**

Similar to Exit, but with one difference. Quit will not close the LBRY SDK connection. Meaning keeping everything running.

**osinfo**

This will give you a document outlining current support for various operating systems. The recommended operating system to use is a variant of GNU / Linux. But the software might work just fine else where too. Type **osinfo** to learn more about it.

**matrix**

Gives the official Matrix Room link.

**repository**

Gives the git repository url for contributors.

**report**

Gives the url of the issue tracker. So you could report bugs.

**license**

Returns the legal code of the license.

**clear**

Clears the screen.

# Simple LBRY Commands

**connect**

If the SDK is not running. You will need to **connect**. But don't connect all the time. Do this only if the SDK is not running. If you **exit** after using the program. The SDK will **disconnect**. But you can use **quit** instead, and then if you enter again, you will not need to **connect**, since it will be already connected. 

The SDK is a separate program running on the background. **connect** starts this program. But you need to start it if it's already running.

**disconnect**

This will stop the SDK from running without quitting the FastLBRY client. **NOTE: This will disconnect all other instances of the SDK. Like for example, if you have LBRY Desktop running. It will close it's connection too.**

**search**

To use this feature type the word **search**, then a space bar and then the search query. 

Example:
 : search moria's race

It will perform a search on the LBRY network for the search query and give you a list of publications, that the SDK found using this query.

**channel**

Similar to the **search** command. Used in the same way. But gives a list of publications by a channel. The query should be the channel's LBRY URL. *Note: Not the Odysee link to the channel. But the canonical LBRY:// url.

Example:
 : channel @blenderdumbass

**trending**

Will show you a list of trending publications.

**articles**

Will show you currently trending readable articles.

**following** or **subscriptions**

Will show the latest publications from the channels you are following.

**settings**

Change the program settings

# Account Related Commands

**login**

Will login to your LBRY account.

**donate**

Will open a donation dialog for you to donate to development of FastLBRY. Read more about how it works in [help/donate.md](help/donate.md).

**donations_test**

Test whether donation information is up to date.

**donations_diff**

See differences between the up to date donation data and the current one.

**donations_update**

Make the donation data up to date.

**donations_add**

Add a new developer into donations data.

**wallet**

Will give you your transaction history

**balance**

Will give you your wallet's balance.

**uploads**

Will give you your uploads history

**history**

Will give you your downloads history

**inbox**

Gives a history of comments done on your publications. You can use a variety of arguments with the command. Like for example **inbox all** will load and cache all of the comment history on your account. That might take a few hours if it's big. **inbox cache** will not fetch any new comments. And use only those already loaded. And you can add any number after **inbox** to load any number of publications. **inbox 20** will load comments only from the last 20 publications.

**publish**

Publish a file to the LBRY network.

**create-channel**

Create a new channel.

**analytics**

Will let you access beautiful graphs of support for all of your publications. LBRY SDK does not have access to Odysee views. And it's not sure that they have views history. But we can access the history of support. From which we can draw a graph.

**sales**

Similar to **analytics** but showing only sales of non-gratis publications.

**total_analytics**

Show a graph with the entire support history. Might load for a long time.

**total_sales**

Show a graph with the entire history of sales.

**load_graph**

Load a graph from memory, those saved using **save** in the graph itself.
