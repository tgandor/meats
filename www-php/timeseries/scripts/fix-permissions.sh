#!/usr/bin/env bash
# fix-permissions.sh — ustawienie uprawnień www-data po (pierwszym) deploy
# Uruchom jako: sudo bash scripts/fix-permissions.sh
# lub:          sudo bash scripts/fix-permissions.sh /sciezka/docelowa

set -euo pipefail

# Odczyt DEPLOY_PATH z .env repo (katalog skryptu → katalog repo → .env)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
ENV_FILE="${REPO_DIR}/.env"

DEPLOY_PATH_DEFAULT=""
if [[ -f "$ENV_FILE" ]]; then
    DEPLOY_PATH_DEFAULT=$(grep -m1 '^DEPLOY_PATH=' "$ENV_FILE" 2>/dev/null | cut -d= -f2- | tr -d '"'"'" | xargs)
fi
DEPLOY_PATH_DEFAULT="${DEPLOY_PATH_DEFAULT:-/var/www/timeseries}"

APP_DIR="${1:-$DEPLOY_PATH_DEFAULT}"
WEB_USER="www-data"

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

ok()   { echo -e "${GREEN}[OK]${NC}  $*"; }
fail() { echo -e "${RED}[FAIL]${NC} $*"; exit 1; }

if [[ $EUID -ne 0 ]]; then
    fail "Uruchom skrypt jako root: sudo bash scripts/fix-permissions.sh"
fi

if [[ ! -d "$APP_DIR" ]]; then
    fail "Katalog aplikacji nie istnieje: $APP_DIR"
fi

echo "=== Time Series — ustawienie uprawnień ==="
echo "Katalog: $APP_DIR"
echo ""

# storage/ i bootstrap/cache/ — pełny dostęp dla www-data
chown -R "${WEB_USER}:${WEB_USER}" "${APP_DIR}/storage"
chmod -R 775 "${APP_DIR}/storage"
ok "storage/ → chown ${WEB_USER}, chmod 775"

chown -R "${WEB_USER}:${WEB_USER}" "${APP_DIR}/bootstrap/cache"
chmod -R 775 "${APP_DIR}/bootstrap/cache"
ok "bootstrap/cache/ → chown ${WEB_USER}, chmod 775"

# database/ — katalog i plik SQLite
if [[ -d "${APP_DIR}/database" ]]; then
    chmod 775 "${APP_DIR}/database"
    ok "database/ → chmod 775"
fi

SQLITE_FILE="${APP_DIR}/database/database.sqlite"
if [[ -f "$SQLITE_FILE" ]]; then
    chown "${WEB_USER}:${WEB_USER}" "$SQLITE_FILE"
    chmod 664 "$SQLITE_FILE"
    ok "database/database.sqlite → chown ${WEB_USER}, chmod 664"
else
    echo "  (database.sqlite nie istnieje — pomijam; wywołaj php artisan migrate --force)"
fi

echo ""
echo "Gotowe. Uprawnienia zaktualizowane."
