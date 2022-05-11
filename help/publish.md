This file will explain how to publish to the LBRY network using FastLBRY. While publishing you need to fill up a form with variables. Some of them are optional. So you can skip this whole thing and move on with publishing. But in order for the publication to be find-able, you may input move values.

For now, the only things that are required to publish have already been inputted. Like LBRY URL, bid amount and file it self.  All the other variables are optional.

**file**

This function will let you edit the file that you are trying to publish. 

**bid**

This function will let you set a bid amount for your publication. If an LBRY URL with the chosen link is already taken, you will need to put higher amount here. Or choose a different LBRY URL.

**url**

By default FastLBRY gives you a random string for the LBRY URL. You may edit it to be something easy to remember using this function. **Note: if you input an LBRY URL name that you already control, instead of publishing a new publication, it will edit the old one.**

**title**

It will give you an option to edit the title of the publication.

**price**

Set a price tag to access the LBRY publication.

**tags**

Set a list of tags separated by a ','. *Seems like LBRY supports up to 6 tags per publication. But it gives me to put more then 6 when uploading without errors. IDK*

**license**

This will help you select the license for your publication. 

**channel**

By default all publications are anonymous. But you may select a channel from those you control to publish using this option.

**thumbnail**

To put a thumbnail preview you need it to be uploaded somewhere already. Good that you can publish the thumbnail file first *(perhaps anonymously or using a special channel for it)* and use the **https** function on it, to get a direct link *(spee.ch)* to the file. 

You may use any https link to any image as a thumbnail to your publication. This command will allow you to edit this link.

Alternatively you can put an image file path on your system. Which will be uploaded to LBRY as a separate publication during upload.

**description**

This will allow you to edit the description of the publication. You may use it in a number of ways.

 `description </file/name>` 
 
This will get the description text from a file that was prepared earlier.

 `description <software>`
 
This will let you edit the description in a multiple text editor of your choice. 

Or just simply type `description` and type a one line text as a description. 

**save**

Saves the current upload settings into a preset.

**load**

Loads a preset previously saved.

**help**

Print out this help message.

**publish**

Will take the current settings and use them to publish the publication.
