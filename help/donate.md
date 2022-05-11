FastLBRY is a project that needs a lot of help. Help in both contributions and donations. To motivate contributors to contribute, we designed a system of donations that will spread the donated amount a given user is willing to give to the contributors of the project.

This document will explain you how it all works, so you start either donating or contributing.

# How to Donate?

First you type `donate` in the main input of FastLBRY Terminal. It will ask you for the amount you are willing to donate. Type that number and press enter.

Let's assume you have chosen to donate 100 LBC. It will present you with a table like this:

| DEVELOPER'S ADDRESS                   | SENDING LBC   |
|---------------------------------------|---------------|
| @FastLBRY:f                           |  7.57138426   |
| @JamesHacker:g                        |  41.08433555  |
| @FreeSoftwareContributor:x            |  51.34428019  |

*Note that addresses in this table are not representing real channels. Apart from the @FastLBRY:f obviously. It's our official LBRY channel. If by mistake I mentioned your channel and you want it removed from this table, please make a Pull Request or an Issue.*

You can see that with 100 LBC first channel receives 7 and half LBC, second channel receives 41 LBC and third channel 51 and a half. This is done using an algorithm, about which I gonna talk in the next chapter. Let's continue with the user side of things.

If you don't like the way the funds are spread, you can type the number of the line ( visible on the left of the table ) and update the amount a given channel gets. Note, that this might update the overall amount of LBC you are going to send. If for example you update the first one to receive 8 LBC instead of 7 and half, you just added another half LBC into the donation.

When you are ready to donate, just type `donate` again, to confirm the donation.

Next step will ask you to choose a channel from which to donate. If you want to keep the donation private, there is going to be an anonymous option. Which will not sign the transaction to any channel. Note the LBRY is a block-chain. And even though they take measures to add procedural noise into the blocks. Like giving each wallet a large amount of addresses. Every transaction is still traceable. Though not as easily as with a channel added.

As soon as you select the channel, if will send the funds to the corresponding contributors. If you have not chosen to be anonymous it will post a comment in the community discussion of the @FastLBRY:f channel, letting us know about your generous donation. If anonymous was chosen, it will skip the comment part entirely.

# The Spreading algorithm

Using some basic `git` commands, we are able to see the amount of commits a given email address made. We can filter it, to show only the last nth amount of commits.

So for example, we ask the computer "For the last 100 commits, who done how many?". And we get a precise number of how many actually approved commits are done by what user. We could use the full history of commits. But some contributors thought that it would motivate people more if we stop including old commits into the support. At the moment we look at the last 100 commits. This number may change.

So let's say there are 3 users that committed in the last 100 commits.

 - @FastLBRY:f has committed 1 commit.
 - @JamesHacker:g has committed 42 commits.
 - @FreeSoftwareContributor:x has committed 109.
 
*Note that I made up those names, as mentioned in the previous chapter.*

So how do we get from the number of the commits to the number of LBC to send to each? Well we could go the simple route and just make it a linear distribution.

`to_send = donation_amount / sum(all_commits) * their_commits`

Which would result in following numbers:


| DEVELOPER'S ADDRESS                   | SENDING LBC   |
|---------------------------------------|---------------|
| @FastLBRY:f                           |  0.65789474   |
| @JamesHacker:g                        |  27.63157895  |
| @FreeSoftwareContributor:x            |  71.71052632  |

But if you remember the example above, showed us different numbers:


| DEVELOPER'S ADDRESS                   | SENDING LBC   |
|---------------------------------------|---------------|
| @FastLBRY:f                           |  7.57138426   |
| @JamesHacker:g                        |  41.08433555  |
| @FreeSoftwareContributor:x            |  51.34428019  |


These are a little bit closer together. Not with such an extreme difference, as in the first table. People that discussed the implementation of this system were worrying that it's going to be unfair, since all you need to do to gain a lot of donations is a number of commits. Thus something to lessen the effect of commits on the over all fraction, was proposed. And it was to use a logarithmic scale.

We ended up using the [log1p](https://en.wikipedia.org/wiki/Natural_logarithm#lnp1) math function to produce fractions of the LBC. And the resulting formula looks something like this:

`to_send = donation_amount / sum(all_log1ps) * their_log1p`

You can see the actual implementation of this in code in [flbry/donate.py](../flbry/donate.py)

# Adding your channel to donations

When you contribute something to the FastLBRY project and want to be in the contributors list, you can do that in a few ways.

There is a file called [devs.json](../devs.json) with a database of contributors emails, lbry links and commit amounts. This file is used by the user to make the donations. And since we cannot hope that the user will have git installed, we have the commit amounts also in that file.

If the git is installed, the user wants to donate, but the number of the commits in not correct, the user will have a small warning. With a simple command `donations_update` the user can update the [devs.json](../devs.json) file. If a new contributor appears, that's not yet in the file, it will ask to provide an lbry link to this contributor. Leaving the link empty will make the donation program ignore this user.

If you enable `dev_mode` in the settings, you will have this file checked each time you start the software. Thus reminding the developers to update this file often.

Using `donations_diff`you can compare the current state of the file to the data coming from the git. And using `donations_add` you can add a user directly to the file. To test whether the file is up to date, use `donations_test`.

Keep in mind that the user is ultimately in control of where his funds are going. He can update the [devs.json](../devs.json) manually, use a different branch, with different contributors, edit the algorithm in the source files or select custom values to each contributor at donation. We as developers only provide the user with an easy to use donation feature. We cannot and should not force the user to use the feature as we written it.
