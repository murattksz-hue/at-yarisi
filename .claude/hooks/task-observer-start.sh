#!/bin/sh
# task-observer SessionStart kancası (kaynak: skill references/environments.md, "A session-start hook").
# Aktivasyonu ve inceleme durumunu additionalContext olarak enjekte eder.
OBS_WORKSPACE="${CLAUDE_PROJECT_DIR:-/home/user/at-yarisi}"   # çalışma kökü; skill "skill-observations/" alt klasörünü kendisi ekler
OBS_SKILL_DIR="${CLAUDE_PROJECT_DIR:-/home/user/at-yarisi}/.claude/skills/task-observer"
d="$OBS_WORKSPACE/skill-observations"
s="$OBS_SKILL_DIR"
if [ ! -f "$s/SKILL.md" ] || [ ! -f "$s/scripts/new-observation.sh" ]; then
  msg="task-observer is NOT INSTALLED at $s (SKILL.md or scripts/ missing): tell the user in your first reply and offer to install it from the repository. Do not invoke it and do not offer a review."
  msg=$(printf '%s' "$msg" | sed 's/\\/\\\\/g; s/"/\\"/g' | tr -d '\000-\037')
  printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"%s"}}\n' "$msg"; exit 0
fi
open=$(find "$d/observation-log" -maxdepth 1 -name '*.md' ! -empty -exec awk '
  function out() { print (st ~ /^(actioned|declined|superseded|parked)$/ ? "x" : "o") }
  FNR==1 { if (NR>1) out(); st=""; fm=0; sub(/^\357\273\277/, "") }
  { sub(/\r$/, "") }
  /^---[[:space:]]*$/ { fm++; next }
  fm==1 && /^status:/ { st=$2; gsub(/["\047]/, "", st) }
  END { if (NR>0) out() }' {} + 2>/dev/null | grep -c o)
last=$(tr -d '\r' 2>/dev/null < "$d/last-review-date.txt"); last=${last:-never}
msg="Make the first tool call of this session one batched call that lists the task-observer workspace ($OBS_WORKSPACE), invokes the task-observer skill and runs bash \"$s/scripts/skill-load.sh\" \"$OBS_WORKSPACE\" task-observer; then run its Session Start Protocol. Observation files are created only by scripts/new-observation.sh in the skill directory, never by copying a header."
msg="$msg $open open observations in $d; last review: $last."
if [ "$open" -gt 0 ]; then
  cutoff=$(date -d '7 days ago' +%F 2>/dev/null || date -v-7d +%F)
  case "$last" in
    (never) msg="$msg Offer the review." ;;
    (*) [ "$(printf '%s\n%s\n' "$last" "$cutoff" | sort | head -1)" = "$last" ] && msg="$msg Offer the review." ;;
  esac
fi
msg=$(printf '%s' "$msg" | sed 's/\\/\\\\/g; s/"/\\"/g' | tr -d '\000-\037')
printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"%s"}}\n' "$msg"
