#!/bin/bash
# Demo script for gtime - Global Time Utility
# This script demonstrates the key features of gtime for recording with Terminalizer

# Colors for better visual appeal
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Timing variables
TYPING_SPEED=0.03
PAUSE_SHORT=1
PAUSE_MEDIUM=2
PAUSE_LONG=3

# Function to simulate typing
type_command() {
    local cmd="$1"
    local speed="${2:-$TYPING_SPEED}"
    
    echo -n "$ "
    for (( i=0; i<${#cmd}; i++ )); do
        printf "${cmd:$i:1}"
        sleep "$speed"
    done
    echo
}

# Function to show a section header
show_section() {
    echo
    echo -e "${CYAN}=== $1 ===${NC}"
    sleep "$PAUSE_SHORT"
}

# Welcome message
echo -e "${MAGENTA}🌐 Welcome to gtime - Global Time Utility Demo!${NC}"
echo -e "${CYAN}===============================================${NC}"
sleep "$PAUSE_MEDIUM"

# Basic city lookup
show_section "📍 Basic City Lookup"
echo -e "${GREEN}Let's check the current time in London:${NC}"
type_command "gtime London"
gtime London
sleep "$PAUSE_LONG"

# Adding favorites
show_section "🌟 Adding Favorite Cities"
echo -e "${GREEN}Let's add some cities to our favorites:${NC}"
type_command "gtime add Tokyo"
gtime add Tokyo
sleep "$PAUSE_SHORT"

type_command "gtime add \"New York\""
gtime add "New York"
sleep "$PAUSE_SHORT"

type_command "gtime add Sydney"
gtime add Sydney
sleep "$PAUSE_SHORT"

type_command "gtime add Mumbai"
gtime add Mumbai
sleep "$PAUSE_MEDIUM"

# Listing favorites
show_section "📋 Viewing Our Favorites"
echo -e "${GREEN}Now let's see all our favorite cities at once:${NC}"
type_command "gtime list"
gtime list
sleep "$PAUSE_LONG"

# Comparing cities
show_section "⚖️ Comparing Multiple Cities"
echo -e "${GREEN}Let's compare times across different cities:${NC}"
type_command "gtime compare London Tokyo \"New York\" Sydney"
gtime compare London Tokyo "New York" Sydney
sleep "$PAUSE_LONG"

# Meeting time conversion
show_section "🤝 Meeting Time Planning"
echo -e "${GREEN}Planning a meeting? Let's see what 3:00 PM London time is everywhere:${NC}"
type_command "gtime meeting at 3:00 PM"
gtime meeting at 3:00 PM
sleep "$PAUSE_LONG"

# Fuzzy search
show_section "🔍 Fuzzy Search Demo"
echo -e "${GREEN}Fuzzy search makes finding cities easy - let's search for 'par':${NC}"
type_command "gtime par"
gtime par
sleep "$PAUSE_LONG"

# Cleanup
show_section "🧹 Managing Favorites"
echo -e "${GREEN}Let's clean up some of our favorites:${NC}"
type_command "gtime remove Tokyo"
gtime remove Tokyo
sleep "$PAUSE_SHORT"

type_command "gtime remove Sydney"
gtime remove Sydney
sleep "$PAUSE_MEDIUM"

echo -e "${GREEN}Final favorites list:${NC}"
type_command "gtime list"
gtime list
sleep "$PAUSE_LONG"

# Help system
show_section "❓ Getting Help"
echo -e "${GREEN}Need help? Here's the complete help menu:${NC}"
type_command "gtime --help"
gtime --help
sleep "$PAUSE_LONG"

# Closing
show_section "✨ That's gtime!"
echo -e "${YELLOW}Your global time companion for the terminal${NC}"
echo -e "${BLUE}📦 Install with: ${GREEN}pip install gtime${NC}"
echo -e "${MAGENTA}🌍 Happy time zone hopping!${NC}"
sleep "$PAUSE_MEDIUM"
