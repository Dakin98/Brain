#!/bin/bash
# Meta Ads Reporting Pull for Razeco UG → Google Sheets
# Only pulls missing months (checks what's already in the sheet)

SHEET_ID="1XTMtZwPRQVR7pRZv2ZZQC_pC5_61JIhkclOsCn1uESA"
ACCOUNT_ID="act_1538907656986107"
ACCOUNT_NAME="Razeco UG"
META_TOKEN=$(grep META_ACCESS_TOKEN /Users/denizakin/.openclaw/workspace/.env | cut -d= -f2)

# Campaign fields
CAMPAIGN_FIELDS="campaign_id,campaign_name,objective,spend,impressions,reach,frequency,clicks,ctr,cpm,actions,action_values,cost_per_action_type"
# Ad Set fields
ADSET_FIELDS="campaign_id,campaign_name,adset_id,adset_name,objective,spend,impressions,reach,frequency,clicks,ctr,cpm,actions,cost_per_action_type"
# Ad/Creative fields
AD_FIELDS="campaign_name,adset_name,ad_id,ad_name,objective,spend,impressions,clicks,ctr,cpc,cpm,actions,cost_per_action_type,video_30_sec_watched_actions,video_p25_watched_actions,video_p75_watched_actions,video_p100_watched_actions,video_play_actions"

echo "=== Meta Ads Reporting Pull ==="
echo "Account: $ACCOUNT_NAME ($ACCOUNT_ID)"
echo ""
