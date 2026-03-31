// Time Series Push Service Worker
self.addEventListener('push', function (event) {
    let data = { title: 'Time Series', body: 'Czas na pomiar!' };
    try {
        data = event.data.json();
    } catch (e) {}

    event.waitUntil(
        self.registration.showNotification(data.title, {
            body: data.body,
            icon: '/ts/favicon.ico',
            badge: '/ts/favicon.ico',
        })
    );
});

self.addEventListener('notificationclick', function (event) {
    event.notification.close();
    event.waitUntil(clients.openWindow('/ts/'));
});
