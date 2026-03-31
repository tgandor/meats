<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Minishlink\WebPush\VAPID;

class GenerateVapidKeys extends Command
{
    protected $signature = 'vapid:generate';
    protected $description = 'Generate VAPID key pair for Web Push and write to .env';

    public function handle(): int
    {
        $keys = VAPID::createVapidKeys();

        $envPath = base_path('.env');
        $env = file_get_contents($envPath);

        $env = preg_replace('/^VAPID_PUBLIC_KEY=.*/m', 'VAPID_PUBLIC_KEY=' . $keys['publicKey'], $env);
        $env = preg_replace('/^VAPID_PRIVATE_KEY=.*/m', 'VAPID_PRIVATE_KEY=' . $keys['privateKey'], $env);

        file_put_contents($envPath, $env);

        $this->info('VAPID keys generated and written to .env');
        $this->line('Public key: ' . $keys['publicKey']);

        return self::SUCCESS;
    }
}
