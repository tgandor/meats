#!/usr/bin/env bash
# deploy.sh — buduje aplikację i kopiuje do DEPLOY_PATH
#
# Użycie:
#   composer deploy          (aktualizacja)
#   composer deploy:first    (pierwsze uruchomienie: seed + vapid:generate)
#
# Workflow na serwerze:
#   cd ~/meats/www-php/timeseries
#   git pull
#   composer deploy

set -euo pipefail

FIRST=0
for arg in "$@"; do
    [[ "$arg" == "--first" ]] && FIRST=1
done

# ---------- kolory ----------
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; BOLD='\033[1m'; NC='\033[0m'
step()  { echo -e "\n${BOLD}>>>${NC} $*"; }
ok()    { echo -e "${GREEN}[OK]${NC}  $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
die()   { echo -e "${RED}[FAIL]${NC} $*" >&2; exit 1; }

# ---------- ścieżka docelowa ----------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Odczyt DEPLOY_PATH z .env repo (jeśli istnieje)
ENV_FILE="${REPO_DIR}/.env"
DEPLOY_PATH=""
if [[ -f "$ENV_FILE" ]]; then
    DEPLOY_PATH=$(grep -m1 '^DEPLOY_PATH=' "$ENV_FILE" 2>/dev/null | cut -d= -f2- | tr -d '"'"'" | xargs)
fi
DEPLOY_PATH="${DEPLOY_PATH:-/var/www/timeseries}"

if [[ ! -d "$DEPLOY_PATH" ]]; then
    die "Katalog docelowy nie istnieje: $DEPLOY_PATH\nUtwórz go lub ustaw DEPLOY_PATH w .env"
fi
if [[ ! -f "${DEPLOY_PATH}/.env" ]]; then
    die "Brak .env w katalogu docelowym: ${DEPLOY_PATH}/.env\nSkopiuj i uzupełnij .env.example przed pierwszym deploy."
fi

echo "=== Time Series — deploy ==="
echo "Repo:   $REPO_DIR"
echo "Target: $DEPLOY_PATH"
[[ $FIRST -eq 1 ]] && echo "Tryb:   pierwsze uruchomienie (--first)"

# ---------- 1. PHP dependencies ----------
step "composer install --no-dev"
composer install --no-dev --optimize-autoloader -d "$REPO_DIR"
ok "Zależności PHP zainstalowane"

# ---------- 2. Frontend build ----------
step "npm ci && npm run build"
cd "$REPO_DIR"
npm ci
npm run build
ok "Frontend zbudowany (public/build/)"

# ---------- 3. rsync do DEPLOY_PATH ----------
step "rsync → $DEPLOY_PATH"
rsync -av --delete \
    --exclude='.env' \
    --exclude='.git/' \
    --exclude='node_modules/' \
    --exclude='database/database.sqlite' \
    --exclude='storage/logs/' \
    --exclude='storage/app/' \
    --exclude='tests/' \
    "${REPO_DIR}/" "${DEPLOY_PATH}/"
ok "Pliki skopiowane"

# ---------- 4. Artisan — uruchom z katalogu produkcyjnego ----------
cd "$DEPLOY_PATH"

step "php artisan migrate --force"
php artisan migrate --force
ok "Migracje wykonane"

step "Cache konfiguracji"
php artisan config:cache
php artisan route:cache
php artisan view:cache
ok "Cache odświeżony"

# ---------- 5. Opcjonalnie: pierwsze uruchomienie ----------
if [[ $FIRST -eq 1 ]]; then
    step "db:seed (konto admina)"
    php artisan db:seed --force
    ok "Seed wykonany"

    step "vapid:generate"
    php artisan vapid:generate
    ok "Klucze VAPID wygenerowane"
fi

echo ""
echo -e "${GREEN}Deploy zakończony pomyślnie.${NC}"
if [[ $FIRST -eq 1 ]]; then
    echo "Pamiętaj: sudo bash scripts/fix-permissions.sh ${DEPLOY_PATH}"
fi
