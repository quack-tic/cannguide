// CannGuide — Service Worker
// WICHTIG: Bei jedem Release die Versionsnummer hochzählen, damit
// bestehende Installationen den neuen Cache übernehmen.
const CACHE_NAME = 'cannguide-v2';

// Relative Pfade: lösen gegen den SW-Speicherort auf (Repo-Root).
// Dadurch case-sicher auf GitHub Pages und portabel (Codespace-Preview, TWA).
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icon192.jpg',
  './icon512.jpg',
  'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js'
];

// Installation: alle Assets cachen
self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return cache.addAll(ASSETS);
    }).then(function() {
      return self.skipWaiting();
    })
  );
});

// Aktivierung: alte Caches löschen
self.addEventListener('activate', function(e) {
  e.waitUntil(
    caches.keys().then(function(keys) {
      return Promise.all(
        keys.filter(function(k) { return k !== CACHE_NAME; })
            .map(function(k) { return caches.delete(k); })
      );
    }).then(function() {
      return self.clients.claim();
    })
  );
});

// Fetch-Strategie:
//  - Navigation / index.html: NETWORK-FIRST (App-Updates kommen sofort an,
//    Cache nur als Offline-Fallback). Bei einer Single-File-App lebt der
//    gesamte Inhalt in index.html — cache-first würde Nutzer dauerhaft
//    auf einer alten Version festhalten.
//  - Alles andere (Chart.js, Icons): CACHE-FIRST (ändert sich selten).
self.addEventListener('fetch', function(e) {
  if (e.request.method !== 'GET') return; // cache.put erlaubt nur GET

  var isNavigation = e.request.mode === 'navigate' ||
                     e.request.url.indexOf('index.html') !== -1;

  if (isNavigation) {
    e.respondWith(
      fetch(e.request).then(function(response) {
        if (response && response.status === 200) {
          var toCache = response.clone();
          caches.open(CACHE_NAME).then(function(cache) {
            cache.put(e.request, toCache);
          });
        }
        return response;
      }).catch(function() {
        // Offline: gecachte Seite liefern ('./index.html' löst relativ
        // zum SW auf — der frühere Pfad '/cannguide/index.html' traf den
        // Cache-Eintrag '/CannGuide/index.html' wegen Case-Sensitivität nie)
        return caches.match(e.request).then(function(cached) {
          return cached || caches.match('./index.html');
        });
      })
    );
    return;
  }

  // Statische Assets: cache-first, dann Netzwerk
  e.respondWith(
    caches.match(e.request).then(function(cached) {
      if (cached) return cached;
      return fetch(e.request).then(function(response) {
        if (!response || response.status !== 200 || response.type === 'opaque') {
          return response;
        }
        var toCache = response.clone();
        caches.open(CACHE_NAME).then(function(cache) {
          cache.put(e.request, toCache);
        });
        return response;
      });
    })
  );
});
