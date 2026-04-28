/* PTMS Service Worker — Push Notifications + Offline Cache */

const CACHE_NAME = 'ptms-v1';

// ── Install: cache the main app shell ────────────────────────
self.addEventListener('install', e => {
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(clients.claim());
});

// ── Push: show notification ───────────────────────────────────
self.addEventListener('push', e => {
  if (!e.data) return;

  let data = {};
  try { data = e.data.json(); } catch { data = { title: 'PTMS', body: e.data.text() }; }

  const title   = data.title  || 'PTMS Notification';
  const options = {
    body:    data.body  || '',
    icon:    data.icon  || '/icon-192.png',
    badge:   data.badge || '/icon-192.png',
    tag:     data.url   || '/',       // collapse duplicate notifications
    renotify: true,
    data: { url: data.url || '/' },
    vibrate: [200, 100, 200],
    actions: [
      { action: 'open',    title: 'Open Task' },
      { action: 'dismiss', title: 'Dismiss'   },
    ]
  };

  e.waitUntil(self.registration.showNotification(title, options));
});

// ── Notification click: open PTMS ────────────────────────────
self.addEventListener('notificationclick', e => {
  e.notification.close();

  if (e.action === 'dismiss') return;

  const targetUrl = (e.notification.data && e.notification.data.url) || '/';

  e.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then(list => {
      // If PTMS tab already open, focus it
      for (const client of list) {
        if (client.url.includes(self.location.origin) && 'focus' in client) {
          return client.focus();
        }
      }
      // Otherwise open new tab
      if (clients.openWindow) return clients.openWindow(targetUrl);
    })
  );
});
