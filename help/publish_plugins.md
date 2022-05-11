FastLBRY has a system of plugins. But since FastLBRY is also an LBRY application, those plugins could be spread around and be searchable using the LBRY protocol. You can already see plugins published this way by searching the `FastLBRY-terminal-plugin-blob-json-file` tag on LBRY. They are json files that contain information about the plugin and links from where to retrieve the source code of the plugin.

# Commands for plugin publish function

**help**

Returns this help message.

**file** or **link**

Sets up the link for the source code. If the link will be a file that exists on your computer, it will be automatically published to LBRY before publishing the blob file. Else, both `http` and `lbry` links are supported.

**publish_file**

This will give you a more in depth setting to publish the source code file. This acts as the **file** function earlier, but instead of typing the link to the file manually, this will upload the file like a normal LBRY publication and then paste it's `lbry` link into the file data point.

Note: This way you can set a fee to the plugin source file. The blob should be always gratis. Payed blobs will be automatically filtered out. Those blobs has to be read before the user decides to get the plugin or not. And requiring payment for the information about the plugin is not nice.

**title**

Edits title of the plugin in the blob file.

**author**

Edits author name in the blob file.

**license**

Select a license for the plugin. Please [refer to this list](https://www.gnu.org/licenses/license-list.html) when choosing a license. Some licenses may restrict the user too much. Which will give them a warning of caution. Some users might even turn an additional filter to get rid of all non-free suggestions.

Providing no license also constitutes not giving user freedom. In some countries giving no license will make it illegal for the user to even run the software. So please add a license. Recommended license will be "GPLv3-or-later".

**description**

Provide a description of what the plugin does. You can use markdown to add links into the description.

**fastlbry**

Change the variant of FastLBRY to which this plugin is intended.

**version**

Provide the version for the plugin.

**fee**

Provide a fee amount for the source file if you want it to be uploaded automatically.

**publish**

Publish the plugin. It will give you a standard publish screen with the blob file already selected to publish. You will see the url where the blob file is stored. So you could read and edit the blob file manually before finalizing the publish.
