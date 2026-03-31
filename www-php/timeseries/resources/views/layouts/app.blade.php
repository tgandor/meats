<!DOCTYPE html>
<html lang="pl">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="csrf-token" content="{{ csrf_token() }}">
        <meta name="vapid-public-key" content="{{ config('app.vapid_public_key') }}">

        <title>{{ config('app.name', 'Time Series') }}</title>

        <!-- Scripts -->
        @vite(['resources/css/app.css', 'resources/js/app.js'])
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css">
        <script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns@3/dist/chartjs-adapter-date-fns.bundle.min.js"></script>
    </head>
    <body class="font-sans antialiased">
        <div class="min-h-screen bg-gray-100 dark:bg-gray-900">
            @include('layouts.navigation')

            @if(session('success'))
                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-4">
                    <div class="bg-green-100 dark:bg-green-900 border border-green-400 text-green-800 dark:text-green-200 px-4 py-2 rounded" role="alert">
                        {{ session('success') }}
                    </div>
                </div>
            @endif

            @isset($header)
                <header class="bg-white dark:bg-gray-800 shadow">
                    <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
                        {{ $header }}
                    </div>
                </header>
            @endisset

            <main class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
                {{ $slot }}
            </main>
        </div>
        @auth
        <script>
        const vapidPublicKey = document.querySelector('meta[name="vapid-public-key"]')?.content;

        function urlBase64ToUint8Array(base64String) {
            const padding = '='.repeat((4 - base64String.length % 4) % 4);
            const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
            const rawData = window.atob(base64);
            return Uint8Array.from([...rawData].map(c => c.charCodeAt(0)));
        }

        // Register Service Worker for push notifications
        if ('serviceWorker' in navigator && 'PushManager' in window) {
            navigator.serviceWorker.register('/ts/push_sw.js').then(reg => {
                window._swReg = reg;
                reg.pushManager.getSubscription().then(sub => {
                    const btn = document.getElementById('pushToggle');
                    if (btn) btn.textContent = sub ? 'Wyłącz powiadomienia push' : 'Włącz powiadomienia push';
                });
            });
        }

        async function togglePush(btn) {
            if (!window._swReg) return;
            const existing = await window._swReg.pushManager.getSubscription();
            if (existing) {
                await existing.unsubscribe();
                await fetch('{{ route('push.unsubscribe') }}', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'X-CSRF-TOKEN': document.querySelector('meta[name=csrf-token]').content },
                    body: JSON.stringify({ endpoint: existing.endpoint })
                });
                btn.textContent = 'Włącz powiadomienia push';
            } else {
                const sub = await window._swReg.pushManager.subscribe({
                    userVisibleOnly: true,
                    applicationServerKey: urlBase64ToUint8Array(vapidPublicKey)
                });
                const key = sub.getKey('p256dh');
                const auth = sub.getKey('auth');
                await fetch('{{ route('push.subscribe') }}', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'X-CSRF-TOKEN': document.querySelector('meta[name=csrf-token]').content },
                    body: JSON.stringify({
                        endpoint: sub.endpoint,
                        public_key: btoa(String.fromCharCode(...new Uint8Array(key))),
                        auth_token: btoa(String.fromCharCode(...new Uint8Array(auth)))
                    })
                });
                btn.textContent = 'Wyłącz powiadomienia push';
            }
        }
        </script>
        @endauth
    </body>
</html>
