<?php

namespace App\Services;

use App\Models\PushSubscription;
use App\Models\User;
use Minishlink\WebPush\Subscription;
use Minishlink\WebPush\WebPush;

class PushNotificationService
{
    private WebPush $webpush;

    public function __construct()
    {
        $auth = [
            'VAPID' => [
                'subject' => config('app.vapid_subject', 'mailto:admin@example.com'),
                'publicKey' => config('app.vapid_public_key'),
                'privateKey' => config('app.vapid_private_key'),
            ],
        ];
        $this->webpush = new WebPush($auth);
    }

    public function sendToUser(User $user, string $title, string $body): void
    {
        $payload = json_encode(['title' => $title, 'body' => $body]);

        foreach ($user->pushSubscriptions as $sub) {
            $subscription = Subscription::create([
                'endpoint' => $sub->endpoint,
                'publicKey' => $sub->public_key,
                'authToken' => $sub->auth_token,
            ]);
            $this->webpush->queueNotification($subscription, $payload);
        }

        foreach ($this->webpush->flush() as $report) {
            if ($report->isSubscriptionExpired()) {
                PushSubscription::where('endpoint', $report->getEndpoint())->delete();
            }
        }
    }
}
