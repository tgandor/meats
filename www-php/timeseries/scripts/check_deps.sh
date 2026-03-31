#!/usr/bin/env bash
# check_deps.sh — weryfikacja zależności dla aplikacji Time Series
# Uruchom jako: bash scripts/check_deps.sh

set -uo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PASS=0
FAIL=0
WARN=0

ok()   { echo -e "${GREEN}[OK]${NC}  $*"; PASS=$((PASS+1)); }
fail() { echo -e "${RED}[FAIL]${NC} $*"; FAIL=$((FAIL+1)); }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; WARN=$((WARN+1)); }

echo "=== Time Series — sprawdzanie zależności ==="
echo ""

# PHP version
if command -v php &>/dev/null; then
    PHP_VERSION=$(php -r 'echo PHP_MAJOR_VERSION . "." . PHP_MINOR_VERSION;')
    if php -r 'exit(PHP_MAJOR_VERSION >= 8 && PHP_MINOR_VERSION >= 2 ? 0 : 1);' 2>/dev/null; then
        ok "PHP $PHP_VERSION (wymagane >= 8.2)"
    else
        fail "PHP $PHP_VERSION — wymagane >= 8.2 (sudo apt install php8.3-fpm)"
    fi
else
    fail "PHP nie znaleziono (sudo apt install php8.3-fpm)"
fi

# PHP extensions
EXTENSIONS=(pdo pdo_sqlite mbstring openssl curl json fileinfo xml zip tokenizer)
for ext in "${EXTENSIONS[@]}"; do
    if php -m 2>/dev/null | grep -qi "^${ext}$"; then
        ok "PHP ext: $ext"
    else
        fail "PHP ext: $ext brakuje (sudo apt install php8.3-${ext} lub php8.3-common)"
    fi
done

# pdo_mysql / pdo_pgsql — opcjonalne
for ext in pdo_mysql pdo_pgsql; do
    if php -m 2>/dev/null | grep -qi "^${ext}$"; then
        ok "PHP ext: $ext (opcjonalne — dostępne)"
    else
        warn "PHP ext: $ext niedostępne (potrzebne tylko dla MySQL/PgSQL)"
    fi
done

# Composer
if command -v composer &>/dev/null; then
    COMP_VER=$(composer --version 2>/dev/null | awk '{print $3}')
    ok "Composer $COMP_VER"
else
    fail "Composer nie znaleziony (https://getcomposer.org/download/ lub sudo apt install composer)"
fi

# Nginx
if command -v nginx &>/dev/null; then
    ok "nginx $(nginx -v 2>&1 | grep -oP '[\d.]+')"
else
    warn "nginx nie znaleziony (sudo apt install nginx)"
fi

# SQLite3
if command -v sqlite3 &>/dev/null; then
    ok "sqlite3 $(sqlite3 --version | awk '{print $1}')"
else
    warn "sqlite3 CLI nie znaleziony (sudo apt install sqlite3) — nie jest wymagany dla PHP"
fi

# Node/npm — tylko do buildu frontendu (nie potrzebne na serwerze produkcyjnym)
if command -v node &>/dev/null; then
    NODE_VER=$(node --version)
    ok "Node.js $NODE_VER (potrzebny do budowania frontendu)"
else
    warn "Node.js niedostępny — wymagany do 'npm run build' (nie potrzebny na serwerze z gotowym buildem)"
fi

# Write perms for storage / database
APP_DIR="$(cd "$(dirname "$0")/.." && pwd)"
for dir in storage storage/logs storage/framework bootstrap/cache; do
    if [ -w "$APP_DIR/$dir" ]; then
        ok "Uprawnienia zapisu: $dir"
    else
        fail "Brak uprawnień zapisu: $dir (rozwiąż: sudo chown -R www-data:www-data $APP_DIR)"
    fi
done

if [ -f "$APP_DIR/database/database.sqlite" ]; then
    if [ -w "$APP_DIR/database/database.sqlite" ]; then
        ok "Plik SQLite: database/database.sqlite (zapisywalny)"
    else
        fail "Plik SQLite: database/database.sqlite nie jest zapisywalny"
    fi
else
    warn "Plik SQLite: database/database.sqlite nie istnieje (zostanie utworzony przy migrate)"
fi

# .env exists
if [ -f "$APP_DIR/.env" ]; then
    ok ".env plik istnieje"
    if grep -q "APP_KEY=base64:" "$APP_DIR/.env"; then
        ok "APP_KEY ustawiony"
    else
        fail "APP_KEY nie ustawiony — uruchom: php artisan key:generate"
    fi
else
    fail ".env nie znaleziony — skopiuj .env.example i skonfiguruj"
fi

echo ""
echo "=== Podsumowanie: ${GREEN}${PASS} OK${NC}  ${RED}${FAIL} FAIL${NC}  ${YELLOW}${WARN} WARN${NC} ==="

[ $FAIL -gt 0 ] && exit 1 || exit 0
