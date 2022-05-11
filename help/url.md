This is a **help** dialogue for publications them selves. Not related with the main **help** dialogue, as you can see by the level of : in the input. All the following commands are exclusively for the publications them selves. If you want to go back a level, like from ::: to :: press enter without typing anything.

**help**

Prints this **help** dialogue.

# Main functions

**play**

Plays the publication. First initializes the download of the file, and then plays it. *Note: If the file is large, the file will start playing before it's fully downloaded.*

**NOTE: If a publication has a PRICE on it. This command will automatically buy it as well.**

**save**

Initialize the download, similar to **play**, but without playing the file.

**NOTE: If a publication has a PRICE on it. This command will automatically buy it as well.**

# Web functions

**https**

Converts the lbry:// link into spee.ch/ link. Giving you a direct link to the file that you can send to people without the LBRY SDK. It will open the link in the default browser. 

**open**

Usage: type **open**, then a space bar, then a name of an application.

Example:
 ::: open vlc
 
Uses the spee.ch link and opens it in a program of choice. If you have a media player that supports streaming video from the internet, you can watch the videos like this without downloading them.

**web**

Gives a web link that you can share with somebody that doesn't have an LBRY client. You will have a little selection dialog from where you can choose any of the known LBRY web instances for this.

**link**

Gives the LBRY link.

**id**

Gives LBRY claim id. Useful for some operations with the LBRY SDK.

# Additional functions

**description**

Read the description of the publication.

**read**

If the publication is an article ( odysee calls them posts ), you can use this feature to read the article right in the terminal. *Note: It supports plain text files, or files in a markdown format. Not documents in PDF or HTML formats.*

**NOTE: If a publication has a PRICE on it. This command will automatically buy it as well.**

**channel**

Loads a list of publications of a channel of this publication.

**comments**

List comments under the publication.

**reply**

Post a comment.

**rss**

Gives the RSS feed for the channel of this publication.

**thumbnail**

Downloads the publication's thumbnail (if it has one) and open it in the default image viewer.

**follow**

Follow the channel that posted the publication.

**unfollow**

Unfollow the channel that posted the publication.

**repost**

Repost the publication to one of your channels. You can give the bid amount in the command, like `repost 0.01`.

**boost**

Boost a publication with LBC. This is refundable.

**tip**

Tip a publication with LBC. This is nonrefundable.

**analytics**

Show analytics graph of this publication. Only works with your own publications.

**sales**

Show sales graph of this publication. Only works with your own publications.
