/* Finance Tracker service worker — cache-first with background refresh,
   so the app works offline after the first visit and quietly picks up updates. */
const CACHE = 'finance-tracker-v7';
const ASSETS = ['./', './index.html', './manifest.webmanifest', './icon-180.png', './icon-512.png'];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE)
      // cache:'reload' bypasses the HTTP cache so the SW installs fresh copies.
      .then((c) => c.addAll(ASSETS.map((u) => new Request(u, { cache: 'reload' }))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') return;
  const cachedP = caches.match(e.request, { ignoreSearch: true });
  const refreshP = cachedP.then((cached) =>
    fetch(e.request)
      .then((res) => {
        if (res && res.ok) {
          const copy = res.clone();
          return caches.open(CACHE).then((c) => c.put(e.request, copy)).then(() => res);
        }
        return res;
      })
      .catch(() => cached)
  );
  // Keep the worker alive until the background refresh's cache write settles,
  // even when the response was already served from cache.
  e.waitUntil(refreshP.then(() => {}, () => {}));
  e.respondWith(
    cachedP
      .then((cached) => cached || refreshP)
      .then((res) =>
        // Total miss (nothing cached AND network failed): serve the cached app
        // shell for page navigations instead of responding with nothing.
        res || (e.request.mode === 'navigate' ? caches.match('./index.html') : res)
      )
  );
});
