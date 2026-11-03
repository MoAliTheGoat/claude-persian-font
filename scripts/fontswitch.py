#!/usr/bin/env python3
"""Make the Claude desktop app draw Persian text in a font you choose.

Claude's font lists name a few fonts a Mac doesn't have ("Segoe UI",
"Noto Sans Hebrew") ahead of the Mac fonts that draw Persian badly. This
installs a Persian-letters-only copy of the chosen font under those names,
so Claude picks it up for Persian text and leaves Latin text alone.
Claude reads fonts only when it starts, so restart it after a change.

  fontswitch.py list            fonts you can choose, as JSON
  fontswitch.py current         the font in use
  fontswitch.py use NAME        switch to NAME
  fontswitch.py off             remove the Persian copies (back to macOS's own)

Fonts: Vazirmatn ships with this plugin. Add your own by putting its .ttf or
.otf files in a folder ~/.claude-persian-font/fonts/<Font Name>/.
"""
import json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
HOME_DIR = os.path.expanduser("~/.claude-persian-font")
FONT_DIRS = [os.path.join(HERE, "..", "fonts"), os.path.join(HOME_DIR, "fonts")]
TARGET = os.path.expanduser("~/Library/Fonts")
STATE = os.path.join(HOME_DIR, "current")
MARK = "ClaudeFa"
# Names Claude lists before Arial (sans) and Times New Roman (serif).
ALIASES = ["Segoe UI", "Noto Sans Hebrew"]
ARABIC = (list(range(0x600, 0x700)) + list(range(0x750, 0x780)) + list(range(0x8A0, 0x900))
          + list(range(0xFB50, 0xFE00)) + list(range(0xFE70, 0xFF00))
          + [0x20, 0x200C, 0x200D, 0x200E, 0x200F])


def need_fonttools():
    try:
        import fontTools  # noqa: F401
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "--user", "-q", "--disable-pip-version-check",
                        "--no-warn-script-location", "fonttools"], check=True)
        # the user site folder may not have existed when Python started
        import importlib, site
        site.addsitedir(site.getusersitepackages())
        importlib.invalidate_caches()


def fonts():
    found = {}
    for base in FONT_DIRS:
        if not os.path.isdir(base):
            continue
        for entry in sorted(os.listdir(base)):
            d = os.path.join(base, entry)
            if not os.path.isdir(d):
                continue
            files = sorted(os.path.join(d, f) for f in os.listdir(d)
                           if f.lower().endswith((".ttf", ".otf")) and os.path.isfile(os.path.join(d, f)))
            if files:
                found[os.path.basename(d)] = files
    return found


OFF = "(off)"


def current():
    try:
        return open(STATE).read().strip("\n")
    except OSError:
        return ""


OURS = re.compile(r"^(SegoeUI|NotoSansHebrew)-%s\d+\.(ttf|otf)$" % MARK)


def installed():
    if not os.path.isdir(TARGET):
        return []
    return [os.path.join(TARGET, f) for f in os.listdir(TARGET)
            if OURS.match(f) and os.path.isfile(os.path.join(TARGET, f))]


def remove_installed():
    for old in installed():
        os.remove(old)


def use(name):
    available = fonts()
    if name not in available:
        sys.exit("unknown font: %s (choose one of: %s)" % (name, ", ".join(available)))
    need_fonttools()
    from fontTools.ttLib import TTFont

    def has_persian(path):
        try:
            cmap = TTFont(path, lazy=True).getBestCmap() or {}
        except Exception:
            return False  # unreadable file: skip it
        return all(cp in cmap for cp in (0x627, 0x6CC, 0x6A9))  # ا ی ک

    sources = [src for src in available[name] if has_persian(src)]
    if not sources:
        sys.exit("%s has no Persian letters (or no readable font file); nothing changed" % name)

    # Build everything first, then swap, so a failure leaves the old font in place.
    work = tempfile.mkdtemp()
    try:
        build(sources, work)
        os.makedirs(TARGET, exist_ok=True)
        remove_installed()
        for f in os.listdir(work):
            shutil.move(os.path.join(work, f), os.path.join(TARGET, f))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    os.makedirs(HOME_DIR, exist_ok=True)
    open(STATE, "w").write(name)


def build(sources, out):
    from fontTools import subset
    from fontTools.ttLib import TTFont

    for n, src in enumerate(sources):
        for alias in ALIASES:
            f = TTFont(src)
            opts = subset.Options()
            opts.layout_features = ["*"]
            opts.name_IDs = ["*"]
            opts.notdef_outline = True
            s = subset.Subsetter(opts)
            s.populate(unicodes=ARABIC)
            s.subset(f)
            # some fonts mislabel their style, so name it from the weight
            weight = f["OS/2"].usWeightClass
            style = f["name"].getDebugName(17) or f["name"].getDebugName(2) or "Regular"
            ps = "%s-%s%d" % (alias.replace(" ", ""), MARK, n)
            names = f["name"]
            for r in list(names.names):
                if r.nameID in (1, 2, 3, 4, 6, 16, 17):
                    names.removeNames(nameID=r.nameID)
            names.setName(alias, 1, 3, 1, 0x409)
            names.setName("Bold" if weight >= 700 else "Regular", 2, 3, 1, 0x409)
            names.setName(ps, 3, 3, 1, 0x409)
            names.setName("%s %s %d" % (alias, style, weight), 4, 3, 1, 0x409)
            names.setName(ps, 6, 3, 1, 0x409)
            names.setName(alias, 16, 3, 1, 0x409)
            names.setName("%s %d" % (style, weight), 17, 3, 1, 0x409)
            bold = weight >= 700
            os2 = f["OS/2"]
            os2.fsSelection = (os2.fsSelection & ~0x61) | (0x20 if bold else 0x40)
            f["head"].macStyle = (f["head"].macStyle & ~1) | (1 if bold else 0)
            ext = os.path.splitext(src)[1].lower()
            f.save(os.path.join(out, ps + ext))


def main(argv):
    cmd = argv[1] if len(argv) > 1 else ""
    if cmd == "list":
        print(json.dumps(list(fonts()), ensure_ascii=False))
    elif cmd == "current":
        print(current())
    elif cmd == "use" and len(argv) > 2:
        use(argv[2] if len(argv) == 3 else " ".join(argv[2:]))
        print("now using %s; restart Claude to see it" % (argv[2] if len(argv) == 3 else " ".join(argv[2:])))
    elif cmd == "off":
        remove_installed()
        os.makedirs(HOME_DIR, exist_ok=True)
        open(STATE, "w").write(OFF)  # remembered, so the plugin doesn't turn Vazirmatn back on
        print("Persian font removed; restart Claude")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
