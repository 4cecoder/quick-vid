This file will explain you how to make themes for FastLBRY terminal. So if you have some imagination, you can make themes for this program.

# Where Are Theme Files?

There are two locations for themes. One is in the `themes` folder in the software it self. Those are maintained in the repository, so any change in those themes will be overwritten on update.

The second place is `~/.local/share/flbry/themes` where you can store theme files too.

# The format

Themes are basically overwriting colors in the fastLBRY color preset. You can find the preset in `flbry/variables.py` toward the beginning of the file.

Terminal has escape codes that if printed, will result in a mode change, or a color change. For example the mode `0` is normal text. Mode `1` is **bold text** and mode `3` is *italic text*.

There are 3 levels of color detail. The one used in the preset originally using 16 colors. But there is a way to use 256 colors or a full spectrum RGB. So don't be afraid. Any colors you want, could be put into the theme.

Let's look at the theme file. This is a test theme:

```
{"bdma":"bdcy",
 "bdcy":"48;2;255;0;0"}
```

If you can see, the file is formatted in a json format. This theme overwrites two presets. `bdma` ( background dark magenta ) which is used most often in the default theme. And it sets it to `bdcy` ( background dark cyan ). The full list of codes are available in the `flbry/variables.py` file.

The second line overwrites the `bdcy` variable with a custom color. Let's look at 3 ways of making a custom color.

## 16 colors custom setting

You can just write a simple number. For example a theme like this:

```
{"bdma":"44"}
```

In this example the `bdma` color will be overwritten with escape code `44`. Which is you look into the `flbry/variables.py` is a code for Dark Blue. You can notice that in the list the code is more complex. Instead of simply being `44` it's `\033[44m`. It's because this way it tells python that it's an escape code and not just some random number. In the theme you may just put the number. The conversion is done for you.

## 256 colors

For 256 colors you may use a more complex code. For example:

```
{"bdma":"48;5;124",
"tbma":"38;5;207"}
```

In this case `bdma` ( background dark magenta ) is overwritten by a fancy dark red and `tbma` ( text bright magenta ) is overwritten with a bright purple. You can see that the code for the background starts with `48;5` and the code for the text starts with `38;5`.

The full range of the 256 colors. Plus explanation for the entire system you can find [on wikipedia here.](https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit)

# Full RGB

Now the most interesting. The full RGB color. This one is quite simple in concept. So let's look at our example.

```
{"bdma":"48;2;255;0;0",
"tbma":"38;2;0;255;0"}
```
You can see that this one is similar to the 256 colors. But it has a more complex number. For example the `5` in the 256 colors was changed to `2`. And the rest are the 3 numbers of the RGB from 0 to 255.

So the first one will overwrite the `bdma` to red. And the second will overwrite the `tbma` to green.
