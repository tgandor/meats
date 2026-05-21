#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 /path/to/program [/path/to/icon]"
    exit 1
fi

BIN="$1"
NAME=$(basename "$BIN")
DESKTOP="$HOME/.local/share/applications/$NAME.desktop"

cat > "$DESKTOP" <<EOF
[Desktop Entry]
Type=Application
Name=$NAME
Exec=$BIN
Icon=$2
Terminal=false
Categories=Utility;
EOF

echo "Opening menu editor..."
kmenuedit Utilities

echo "Created: $DESKTOP"
