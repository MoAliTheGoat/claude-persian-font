# Setting this up for someone (instructions for Claude)

The person wants the Claude desktop app on their Mac to show Persian text in a nicer font. Do this:

1. Check it's macOS and `python3 --version` works. If python3 is missing, tell them to run `xcode-select --install` and come back.
2. Install the plugin. In a Claude Code terminal session:
   `claude plugin marketplace add MoAliTheGoat/claude-persian-font` then `claude plugin install persian-font@claude-persian-font`
   If you can't run that, tell them: in the desktop app click **+** next to the message box → **Plugins** → **Add marketplace** → `MoAliTheGoat/claude-persian-font` → add **persian-font**.
3. Turn on Vazirmatn now so it works after one restart (the plugin also does this on its first start):
   `python3 "$(find ~/.claude/plugins -path '*persian-font*' -name fontswitch.py | head -1)" use Vazirmatn`
   If the path isn't found, skip this step; the plugin does it itself.
4. If they own other Persian fonts (IRANSans, Modam, ...), offer to copy their `.ttf`/`.otf` files into `~/.claude-persian-font/fonts/<Font Name>/` (one folder per font, Regular and Bold at least). Never download paid fonts for them.
5. Tell them, in plain words: quit Claude with Cmd+Q and open it again. Then a small **Aa** button above the message box lets them switch fonts; Claude restarts itself after each switch.

To undo: `fontswitch.py off`, then remove the plugin from Plugins.
