#!/bin/bash
# ============================================================
# Growth System Setup Checklist — adsdrop
# ============================================================
# Interaktive Checkliste zum Abhaken aller Setup-Schritte
# Usage: bash scripts/growth-setup-checklist.sh
# ============================================================

CHECKLIST_FILE="$HOME/.openclaw/workspace/scripts/.growth-checklist-state"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

# Load state
declare -A DONE
if [ -f "$CHECKLIST_FILE" ]; then
  while IFS= read -r line; do
    DONE["$line"]=1
  done < "$CHECKLIST_FILE"
fi

save_state() {
  > "$CHECKLIST_FILE"
  for key in "${!DONE[@]}"; do
    echo "$key" >> "$CHECKLIST_FILE"
  done
}

print_item() {
  local id="$1"
  local text="$2"
  if [ "${DONE[$id]}" == "1" ]; then
    echo -e "  ${GREEN}✅ $text${NC}"
  else
    echo -e "  ${RED}☐  $text${NC}"
  fi
}

toggle_item() {
  local id="$1"
  if [ "${DONE[$id]}" == "1" ]; then
    unset DONE["$id"]
  else
    DONE["$id"]=1
  fi
  save_state
}

count_done() {
  local prefix="$1"
  local total="$2"
  local count=0
  for key in "${!DONE[@]}"; do
    if [[ "$key" == "$prefix"* ]]; then
      ((count++))
    fi
  done
  echo "$count/$total"
}

show_checklist() {
  clear
  echo -e "${BOLD}╔══════════════════════════════════════════════╗${NC}"
  echo -e "${BOLD}║   🚀 Growth System Setup — adsdrop           ║${NC}"
  echo -e "${BOLD}╚══════════════════════════════════════════════╝${NC}"
  echo ""

  # Phase 1
  echo -e "${BLUE}${BOLD}═══ PHASE 1: Content Engine (Woche 1) ═══${NC} [$(count_done 'p1' 12)]"
  echo ""
  echo -e "${YELLOW}Tag 1: Struktur${NC}"
  print_item "p1_01" "Content Engine Folder in ClickUp erstellen"
  print_item "p1_02" "Content Ideas Liste erstellen"
  print_item "p1_03" "YouTube Pipeline Liste erstellen"
  print_item "p1_04" "Reels Pipeline Liste erstellen"
  print_item "p1_05" "LinkedIn Pipeline Liste erstellen"
  print_item "p1_06" "Newsletter Pipeline Liste erstellen"
  print_item "p1_07" "Distribution Tracker Liste erstellen"
  echo ""
  echo -e "${YELLOW}Tag 2: Custom Fields${NC}"
  print_item "p1_08" "Status-Workflows für alle 6 Listen konfigurieren"
  print_item "p1_09" "Custom Fields für Content Ideas (8 Fields)"
  print_item "p1_10" "Custom Fields für YouTube Pipeline (13 Fields)"
  print_item "p1_11" "Custom Fields für Reels (10 Fields)"
  print_item "p1_12" "Custom Fields für LinkedIn (10 Fields)"
  print_item "p1_13" "Custom Fields für Newsletter (11 Fields)"
  print_item "p1_14" "Custom Fields für Distribution Tracker (4 Fields)"
  echo ""
  echo -e "${YELLOW}Tag 3: Templates & Views${NC}"
  print_item "p1_15" "YouTube Task Template mit Checkliste erstellen"
  print_item "p1_16" "Newsletter Task Template mit Checkliste erstellen"
  print_item "p1_17" "Board Views für alle Listen"
  print_item "p1_18" "Table Views für alle Listen"
  print_item "p1_19" "Calendar Views für YouTube + LinkedIn + Newsletter"
  echo ""
  echo -e "${YELLOW}Tag 4-5: Migration & Test${NC}"
  print_item "p1_20" "Bestehende Content Tasks migrieren"
  print_item "p1_21" "Bestehende Newsletter Tasks migrieren"
  print_item "p1_22" "Erstes YouTube Video durch Pipeline testen"
  echo ""

  # Phase 2
  echo -e "${BLUE}${BOLD}═══ PHASE 2: Outbound Engine (Woche 2) ═══${NC} [$(count_done 'p2' 10)]"
  echo ""
  echo -e "${YELLOW}Tag 1: Struktur${NC}"
  print_item "p2_01" "Outbound Engine Folder erstellen"
  print_item "p2_02" "Lead Lists Liste erstellen"
  print_item "p2_03" "Campaigns Liste erstellen"
  print_item "p2_04" "Sequences Liste erstellen"
  print_item "p2_05" "Reply Management Liste erstellen"
  print_item "p2_06" "Inbox & Domain Health Liste erstellen"
  echo ""
  echo -e "${YELLOW}Tag 2: Custom Fields${NC}"
  print_item "p2_07" "Status-Workflows für alle 5 Listen"
  print_item "p2_08" "Custom Fields für Lead Lists (8 Fields)"
  print_item "p2_09" "Custom Fields für Campaigns (14 Fields)"
  print_item "p2_10" "Custom Fields für Sequences (10 Fields)"
  print_item "p2_11" "Custom Fields für Reply Management (10 Fields)"
  print_item "p2_12" "Custom Fields für Domain Health (11 Fields)"
  echo ""
  echo -e "${YELLOW}Tag 3: Setup & Test${NC}"
  print_item "p2_13" "4 bestehende Inbox-Accounts eintragen"
  print_item "p2_14" "Campaign Task Template erstellen"
  print_item "p2_15" "Views einrichten (Board, Table)"
  print_item "p2_16" "Bestehende Outbound Tasks migrieren"
  print_item "p2_17" "Erste Campaign durch Pipeline testen"
  echo ""

  # Phase 3
  echo -e "${BLUE}${BOLD}═══ PHASE 3: Automations (Woche 3-4) ═══${NC} [$(count_done 'p3' 6)]"
  echo ""
  print_item "p3_01" "ClickUp Automation: YouTube Published → 3 Reels Tasks"
  print_item "p3_02" "ClickUp Automation: YouTube Published → LinkedIn Task"
  print_item "p3_03" "ClickUp Automation: YouTube Published → Newsletter Reminder"
  print_item "p3_04" "ClickUp Automation: Reply Interested → Meeting Subtask"
  print_item "p3_05" "ClickUp Automation: Meeting Booked → CRM Prospect"
  print_item "p3_06" "Script: Weekly Report Generator"
  echo ""

  # Phase 4
  echo -e "${BLUE}${BOLD}═══ PHASE 4: Dashboards (Woche 3-4) ═══${NC} [$(count_done 'p4' 4)]"
  echo ""
  print_item "p4_01" "Content Performance Dashboard erstellen"
  print_item "p4_02" "Outbound Performance Dashboard erstellen"
  print_item "p4_03" "Growth Overview Dashboard erstellen"
  print_item "p4_04" "KPI-Ziele eintragen"
  echo ""

  echo -e "${BOLD}──────────────────────────────────────────────${NC}"
  echo -e "  Enter item ID to toggle (e.g. ${YELLOW}p1_01${NC})"
  echo -e "  ${YELLOW}q${NC} = quit | ${YELLOW}r${NC} = refresh"
  echo -e "${BOLD}──────────────────────────────────────────────${NC}"
}

# Main loop
while true; do
  show_checklist
  read -rp "  > " input
  case "$input" in
    q|Q|quit|exit) echo "Bye! 👋"; exit 0 ;;
    r|R) continue ;;
    p[1-4]_[0-9][0-9]) toggle_item "$input" ;;
    *) echo -e "${RED}  Invalid input. Use format: p1_01${NC}"; sleep 1 ;;
  esac
done
