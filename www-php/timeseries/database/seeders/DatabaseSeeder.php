<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    use WithoutModelEvents;

    /**
     * Seed the application's database.
     */
    public function run(): void
    {
        // Create admin user — credentials set via env or changed after first login
        User::firstOrCreate(
            ['email' => env('ADMIN_EMAIL', 'admin@localhost')],
            [
                'name' => env('ADMIN_NAME', 'Admin'),
                'password' => bcrypt(env('ADMIN_PASSWORD', 'changeme')),
                'is_admin' => true,
            ]
        );
    }
}
