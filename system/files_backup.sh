#!/usr/bin/env bash
set -euo pipefail

# Destination directories
BACKUP_DIR="$HOME/backup"
CHECKSUM_FILE="$BACKUP_DIR/checksums.txt"

mkdir -p "$BACKUP_DIR"

# Iterate over files in current directory or passed as arguments
for file in "${@:-*}"; do
    # Skip if not a regular file
    [[ -f "$file" ]] || continue

    out_file="$BACKUP_DIR/$(basename "$file").zst"

    echo "Processing: $file -> $out_file"

    # Read file once: tee to md5sum and zstd
    # Use process substitution for md5sum
    tee >(md5sum | awk '{print $1 "  " "'"$file"'" }' >> "$CHECKSUM_FILE") \
        < "$file" | zstd -T0 -o "$out_file"
done

echo "Done. Checksums saved to $CHECKSUM_FILE"
