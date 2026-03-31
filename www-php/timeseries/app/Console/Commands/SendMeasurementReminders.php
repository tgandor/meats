<?php

namespace App\Console\Commands;

use App\Models\Series;
use App\Services\PushNotificationService;
use Illuminate\Console\Command;

class SendMeasurementReminders extends Command
{
    protected $signature = 'timeseries:reminders';
    protected $description = 'Send push reminders for overdue series measurements';

    public function handle(PushNotificationService $push): int
    {
        $dueSeries = Series::with(['latestMeasurement', 'user.pushSubscriptions'])
            ->whereNotNull('sampling_interval_hours')
            ->get()
            ->filter(fn (Series $s) => $s->isDueForMeasurement());

        foreach ($dueSeries as $series) {
            if ($series->user->pushSubscriptions->isEmpty()) {
                continue;
            }
            $push->sendToUser(
                $series->user,
                'Czas na pomiar: ' . $series->name,
                'Zaloguj się i dodaj nowy odczyt dla "' . $series->name . '"'
                    . ($series->unit ? ' (' . $series->unit . ')' : '') . '.'
            );
            $this->line("Notified user {$series->user->name} for series \"{$series->name}\"");
        }

        return self::SUCCESS;
    }
}
