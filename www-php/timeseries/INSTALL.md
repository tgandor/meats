# Instalacja i konfiguracja — Time Series

Aplikacja Laravel 11 do śledzenia serii czasowych. Domyślna baza: SQLite. Działa pod ścieżką `/ts/`.

---

## Wymagania systemowe

| Składnik | Minimalna wersja |
|---|---|
| PHP | 8.2+ |
| Rozszerzenia PHP | pdo, pdo_sqlite, mbstring, openssl, curl, json, fileinfo, xml, zip, tokenizer |
| Composer | 2.x |
| Nginx / Apache | dowolna aktualna |
| SQLite | dowolna (PHP ext wystarczy) |
| Node/npm | tylko do buildu frontendu (nie potrzebny na serwerze) |

### Ubuntu / Debian / Raspberry Pi OS

```bash
sudo apt update
sudo apt install php-fpm php-sqlite3 php-mbstring \
     php-xml php-curl php-zip php-intl \
     composer nginx sqlite3

# Opcjonalnie dla MySQL/MariaDB:
sudo apt install php-mysql

# Opcjonalnie dla PostgreSQL:
sudo apt install php-pgsql
```

Sprawdzenie zależności:
```bash
bash scripts/check_deps.sh
```

---

## Instalacja

### 1. Klonowanie / kopiowanie plików

```bash
sudo mkdir -p /var/www/timeseries
sudo chown $USER:$USER /var/www/timeseries
# Skopiuj pliki projektu do /var/www/timeseries
```

### 2. Zależności PHP

```bash
cd /var/www/timeseries
composer install --no-dev --optimize-autoloader
```

### 3. Konfiguracja .env

```bash
cp .env.example .env   # jeśli nie istnieje .env
php artisan key:generate
```

Minimalny `.env` dla SQLite:

```ini
APP_NAME="Time Series"
APP_ENV=production
APP_DEBUG=false
APP_URL=https://twoja.domena.pl/ts
APP_SUBPATH=/ts

DB_CONNECTION=sqlite
DB_DATABASE=/var/www/timeseries/database/database.sqlite

ADMIN_EMAIL=admin@localhost
ADMIN_NAME=Admin
ADMIN_PASSWORD=zmien_mnie_natychmiast

VAPID_SUBJECT=mailto:admin@twoja.domena.pl
VAPID_PUBLIC_KEY=
VAPID_PRIVATE_KEY=

SESSION_DRIVER=file
CACHE_STORE=file
QUEUE_CONNECTION=sync
```

### 4. Baza danych i seeder admina

```bash
touch database/database.sqlite
chmod 664 database/database.sqlite

php artisan migrate --force
php artisan db:seed --force   # tworzy konto admin wg ADMIN_* z .env
```

### 5. Klucze VAPID (Web Push)

```bash
php artisan vapid:generate
```

Klucze zostaną zapisane automatycznie do `.env`.

### 6. Uprawnienia

```bash
sudo chown -R www-data:www-data /var/www/timeseries/storage
sudo chown -R www-data:www-data /var/www/timeseries/bootstrap/cache
sudo chown www-data:www-data /var/www/timeseries/database/database.sqlite
sudo chmod 664 /var/www/timeseries/database/database.sqlite
sudo chmod 775 /var/www/timeseries/database
```

### 7. Cache konfiguracji (produkcja)

```bash
php artisan config:cache
php artisan route:cache
php artisan view:cache
```

---

## Konfiguracja nginx — subpath `/ts/`

Aplikacja działa pod ścieżką `/ts/` (konfigurowane przez `APP_SUBPATH` w `.env`).

```nginx
server {
    listen 80;
    listen 443 ssl;
    server_name twoja.domena.pl;

    # Let's Encrypt (Certbot doda automatycznie)
    # ssl_certificate /etc/letsencrypt/live/twoja.domena.pl/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/twoja.domena.pl/privkey.pem;

    # ... inne lokalizacje serwera ...

    # /ts bez trailing slash → redirect 301
    location = /ts {
        return 301 /ts/;
    }

    # Vite build assets — ^~ blokuje regex poniżej, serwowane statycznie
    location ^~ /ts/build/ {
        alias /var/www/timeseries/public/build/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Pliki statyczne z public/ (push_sw.js, favicon.ico, robots.txt)
    location ~* ^/ts/([^/]+\.(ico|txt|js|webmanifest|png|svg))$ {
        alias /var/www/timeseries/public/$1;
        expires 7d;
    }

    # Wszystkie trasy Laravel → jeden entry point (brak alias, brak try_files)
    location ~ ^/ts {
        include       fastcgi_params;          # najpierw — nasze jawne params nadpiszą
        fastcgi_pass  unix:/run/php/php-fpm.sock;
        fastcgi_param SCRIPT_FILENAME /var/www/timeseries/public/index.php;
        fastcgi_param SCRIPT_NAME     /ts/index.php;
    }
}
```

Przeładowanie nginx:
```bash
sudo nginx -t && sudo systemctl reload nginx
```

---

## Konfiguracja MySQL / MariaDB (alternatywa dla SQLite)

W `.env` zmień:

```ini
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=timeseries
DB_USERNAME=ts_user
DB_PASSWORD=tajne_haslo
```

```sql
CREATE DATABASE timeseries CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'ts_user'@'localhost' IDENTIFIED BY 'tajne_haslo';
GRANT ALL PRIVILEGES ON timeseries.* TO 'ts_user'@'localhost';
FLUSH PRIVILEGES;
```

Potem normalnie: `php artisan migrate`.

---

## Konfiguracja PostgreSQL

```ini
DB_CONNECTION=pgsql
DB_HOST=127.0.0.1
DB_PORT=5432
DB_DATABASE=timeseries
DB_USERNAME=ts_user
DB_PASSWORD=tajne_haslo
```

---

## Cron — scheduler przypomnień

Dodaj do crontab użytkownika `www-data`:

```bash
sudo crontab -u www-data -e
```

```cron
* * * * * cd /var/www/timeseries && php artisan schedule:run >> /dev/null 2>&1
```

Scheduler uruchamia `timeseries:reminders` co 15 minut — wysyła Web Push do użytkowników, którzy mają serie z upływającym interwałem pomiaru.

---

## Let's Encrypt (RPi)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d twoja.domena.pl
```

**Ważne:** Web Push (VAPID) wymaga HTTPS. Na localhost działa bez certyfikatu.

---

## Zarządzanie

### Zmiana hasła admina przez CLI

```bash
php artisan tinker
>>> App\Models\User::where('email','admin@localhost')->first()->update(['password' => bcrypt('nowe_haslo')]);
```

### Backup SQLite

```bash
cp /var/www/timeseries/database/database.sqlite /backup/timeseries_$(date +%Y%m%d).sqlite
```

### Aktualizacja aplikacji

```bash
cd ~/meats/www-php/timeseries   # katalog repo (nie /var/www/timeseries!)
git pull
composer deploy
```

Skrypt `deploy` wykonuje kolejno: `composer install --no-dev`, `npm ci`, `npm run build`, `rsync` do `DEPLOY_PATH`, `migrate --force`, `config:cache`, `route:cache`, `view:cache`.

Ścieżka docelowa pochodzi ze zmiennej `DEPLOY_PATH` w `.env` repo (domyślnie `/var/www/timeseries`).

**Pierwsze uruchomienie** (nowa instalacja po skonfigurowaniu `.env` w `DEPLOY_PATH`):

```bash
composer deploy:first
```

Dodaje do powyższego: `db:seed` (konto admina z `ADMIN_*` w `.env`) oraz `vapid:generate`.

**Uprawnienia** (po pierwszym deploy lub po zmianie właściciela plików):

```bash
sudo bash scripts/fix-permissions.sh
```

---

## Logowanie pierwszego admina

1. Wejdź na `https://twoja.domena.pl/ts/login`
2. E-mail: `admin@localhost` (lub wartość `ADMIN_EMAIL` z `.env`)
3. Hasło: `changeme` (lub wartość `ADMIN_PASSWORD` z `.env`) — **zmień natychmiast po pierwszym zalogowaniu!**
4. W menu → **Zaproszenia** → wygeneruj link dla nowych użytkowników

---

## RPi 2B — uwagi praktyczne

- `composer deploy` uruchamia `npm ci && npm run build` na samym serwerze — na RPi 2B (armv6) może to potrwać kilka minut; można przyspieszyć kopiując `public/build/` z maszyny dev przez rsync i pomijając npm
- Ustaw `PHP_CLI_SERVER_WORKERS=1` jeśli używasz wbudowanego serwera PHP do testów
- SQLite jest optymalny — nie wymaga daemon MySQL
- Recommend: `memory_limit = 64M` w `php.ini`
