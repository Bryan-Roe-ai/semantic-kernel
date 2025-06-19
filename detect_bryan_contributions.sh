```bash
#!/usr/bin/env bash
# Script: detect_bryan_contributions.sh
# Purpose: Automate detection of commits and files contributed by Bryan Roe

# Configuration
AUTHOR="Bryan‑Roe"                             # Author name or email to filter
OUTPUT_LOG="bryan_contributions.log"            # Detailed commit log output
OUTPUT_FILES="bryan_files.txt"                  # Unique list of files contributed

# Step 1: Export detailed commit information (SHA, date, message, files changed)
git log \
  --author="$AUTHOR" \
  --pretty=format:"Commit: %H%nDate: %ad%nMessage: %s%n" \
  --date=short \
  --name-status \
  > "$OUTPUT_LOG"

echo "Detailed log written to $OUTPUT_LOG"

# Step 2: Extract and dedupe file paths touched by the author
git log \
  --author="$AUTHOR" \
  --name-only \
  --pretty=format:"" \
  | grep -v '^$' \
  | sort \
  | uniq \
  > "$OUTPUT_FILES"

echo "Unique file list written to $OUTPUT_FILES"

# Optional: Display summary counts
echo "Total commits by $AUTHOR: $(grep -c '^Commit:' "$OUTPUT_LOG")"
echo "Total unique files modified by $AUTHOR: $(wc -l < "$OUTPUT_FILES")"
```
