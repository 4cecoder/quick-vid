# This is trying to brute force through all terminals
# until it finds one that works.

for terminal in $TERMINAL x-terminal-emulator urxvt rxvt st terminology qterminal Eterm aterm uxterm xterm roxterm xfce4-terminal.wrapper mate-terminal lxterminal konsole alacritty kitty; do
    if command -v $terminal >/dev/null 2>&1; then
        exec $terminal -e "python3 run.py"
    fi
done
