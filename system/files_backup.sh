#!/usr/bin/env bash
set -euo pipefail

# ---- Config (overridable via env) ----
BACKUP_DIR="${BACKUP_DIR:-$HOME/backup}"
LEVEL="${LEVEL:-10}"               # zstd compression level (e.g., 1..19)
CHECKSUM_FILE="$BACKUP_DIR/checksums.txt"
LOG_FILE="$BACKUP_DIR/zstd.log"

mkdir -p "$BACKUP_DIR"

# ---- Logging helper (console + file, with ISO timestamp) ----
log() {
  local ts
  ts="$(date -Iseconds)"
  # echo to console AND append to log
  printf '%s %s\n' "$ts" "$*" | tee -a "$LOG_FILE"
}

# ---- Choose pv or cat ----
if command -v pv >/dev/null 2>&1; then
  PV_CMD="pv"
else
  PV_CMD="cat"
fi

log "Starting compression & checksums. BACKUP_DIR='$BACKUP_DIR' LEVEL=$LEVEL PV_CMD=$PV_CMD"

# Iterate over args if provided, otherwise all files in current dir
for file in "${@:-*}"; do
  [[ -f "$file" ]] || continue

  base="$(basename "$file")"
  out_file="$BACKUP_DIR/$base.zstd"

  log "Processing: '$file' -> '$out_file'"

  # Read the file once: PV_CMD -> tee -> md5sum & zstd
  # - md5sum line format: "<md5>  <original_filename>"
  # - zstd uses specified LEVEL and all threads (-T0)
  "${PV_CMD}" "$file" \
    | tee >(md5sum | awk '{print $1 "  " "'"$file"'" }' >> "$CHECKSUM_FILE") \
    | zstd -T0 -"${LEVEL}" -o "$out_file"
done

log "Done. Checksums saved to $CHECKSUM_FILE"
