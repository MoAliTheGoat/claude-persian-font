#!/bin/zsh
# Run by launchd (not by Claude) so it outlives Claude quitting.
sleep 1
osascript -e 'quit app "Claude"'
for i in {1..30}; do
  pgrep -f "^/Applications/Claude.app/Contents/MacOS/Claude" >/dev/null || break
  sleep 1
done
sleep 1
open -a Claude
launchctl remove local.claude-persian-font.restart
