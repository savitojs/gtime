#!/bin/bash
# Demo script for gtime - Global Time Utility
# Records with: record-demo gtime -s ./demo.sh
# Or: terminalizer record demo -d demo.sh

# ── Typing simulator ──
TYPING_SPEED=0.04
PAUSE=1.8
PAUSE_LONG=3

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m'

type_cmd() {
    echo -n "$ "
    for (( i=0; i<${#1}; i++ )); do
        printf "${1:$i:1}"
        sleep "$TYPING_SPEED"
    done
    echo
}

header() {
    echo
    echo -e "${CYAN}━━━ $1 ━━━${NC}"
    sleep 0.8
}

# ── Backup and reset favorites for clean demo ──
restore_favorites() {
    cp ~/.gtime_favorites.json.demo-backup ~/.gtime_favorites.json 2>/dev/null
    rm -f ~/.gtime_favorites.json.demo-backup
}
trap restore_favorites EXIT INT TERM
cp ~/.gtime_favorites.json ~/.gtime_favorites.json.demo-backup 2>/dev/null
echo '[]' > ~/.gtime_favorites.json

clear

echo -e "${MAGENTA}gtime - Global Time Utility${NC}"
echo -e "${CYAN}pip install gtime | github.com/savitojs/gtime${NC}"
echo
sleep "$PAUSE"

# ── City lookup + fuzzy search ──
header "Look up any city - even with typos"

echo -e "${GREEN}Exact match:${NC}"
type_cmd "gtime Tokyo"
gtime Tokyo
sleep "$PAUSE"

echo ""

echo -e "${GREEN}Fuzzy search works too:${NC}"
type_cmd "gtime pairs"
gtime pairs
sleep "$PAUSE"

echo ""

echo -e "${GREEN}Case insensitive:${NC}"
type_cmd "gtime mumbai"
gtime mumbai
sleep "$PAUSE_LONG"

clear
# ── Favorites ──
header "Build your favorites for quick access"

type_cmd "gtime add Delhi Melbourne Brno \"New York\""
gtime add Delhi Melbourne Brno "New York"
sleep "$PAUSE"

echo ""

echo -e "${GREEN}View all favorites at once:${NC}"
type_cmd "gtime"
gtime
sleep "$PAUSE_LONG"

clear
# ── Compare ──
header "Compare cities side by side"

type_cmd "gtime compare Delhi Brno Melbourne \"New York\""
gtime compare Delhi Brno Melbourne "New York"
sleep "$PAUSE_LONG"

clear

# ── Meeting planner ──
header "Plan meetings across time zones"

echo -e "${GREEN}What time is 2 PM for everyone?${NC}"
type_cmd "gtime meeting at \"2:00 PM\""
gtime meeting at "2:00 PM"
sleep "$PAUSE_LONG"

echo ""

echo -e "${GREEN}Works with any timezone:${NC}"
type_cmd "gtime meeting at \"10:00 AM JST\""
gtime meeting at "10:00 AM JST"
sleep "$PAUSE_LONG"

clear
# ── Desktop widget ──
header "GNOME Desktop Widget (NEW!)"

echo -e "${GREEN}Style A - Flags + status:${NC}"
type_cmd "gtime widget a"
gtime widget a
sleep "$PAUSE"

echo
echo -e "${GREEN}Style B - Grouped by status:${NC}"
type_cmd "gtime widget b"
gtime widget b
sleep "$PAUSE"

echo
echo -e "${GREEN}Style C - Compact cards:${NC}"
type_cmd "gtime widget c"
gtime widget c
sleep "$PAUSE_LONG"

clear
# ── Manage favorites ──
header "Easy to manage"

type_cmd "gtime remove Brno"
gtime remove Brno
sleep "$PAUSE"

type_cmd "gtime add Brno"
gtime add Brno
sleep "$PAUSE"

clear
# ── Closing ──
echo
echo -e "${YELLOW}pip install gtime${NC}"
echo ""
echo -e "${BLUE}https://github.com/savitojs/gtime${NC}"
echo -e "🌟 ${GREEN}Star it if you find it useful!${NC}"
echo
sleep "$PAUSE_LONG"

# Favorites restored automatically by EXIT trap
