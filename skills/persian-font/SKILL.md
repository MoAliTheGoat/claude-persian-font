---
name: persian-font
description: Change, add or remove the font the Claude desktop app uses for Persian/Farsi (and Arabic-script) text on macOS. Use when the user says Persian text looks ugly, asks to change Claude's font, wants Vazirmatn/IRANSans/Modam or another Persian font in Claude, or asks «فونت Claude را عوض کن» / «فونت فارسی».
---

# Persian font for Claude desktop

The tool is `scripts/fontswitch.py` in this plugin's folder. Find it with:

```bash
F="$(find ~/.claude/plugins -path '*persian-font*' -name fontswitch.py | head -1)"
```

- `python3 "$F" list` — fonts available (JSON). Vazirmatn is bundled.
- `python3 "$F" current` — the font in use (`(off)` when turned off).
- `python3 "$F" use "<name>"` — switch. Then Claude must restart to show it.
- `python3 "$F" off` — back to macOS's own Persian font.

To add a font the user owns: copy its `.ttf`/`.otf` files (at least Regular and Bold) into `~/.claude-persian-font/fonts/<Font Name>/`, then `use "<Font Name>"`. Never download paid fonts for them.

Restarting: tell the user to quit Claude (Cmd+Q) and open it again, or to use the small **Aa** button above the message box, which switches and restarts Claude by itself. Don't quit Claude yourself: it ends the conversation you are in.

Limits worth telling the user plainly: every change needs one restart; the fonts can't be added to Claude's own Settings → Interface font menu; the button can only sit above the message box. Latin text and code keep their fonts.
