// Cache Clear - Regional Veículos
// Force cache update for performance optimization

// Clear outdated service worker cache
if ('serviceWorker' in navigator && 'caches' in window) {
    // Clear old cache versions
    caches.keys().then(function(cacheNames) {
        return Promise.all(
            cacheNames.map(function(cacheName) {
                if (cacheName.indexOf('regional-veiculos-v1.0.0') !== -1) {
                    console.log('[Cache Clear] Removing old cache:', cacheName);
                    return caches.delete(cacheName);
                }
            })
        );
    }).then(function() {
        console.log('[Cache Clear] Old caches cleared successfully');
        // Force page reload to get fresh content
        if (window.location.search.indexOf('cache=cleared') === -1) {
            const separator = window.location.search ? '&' : '?';
            window.location.href = window.location.href + separator + 'cache=cleared';
        }
    });
}

// Clear browser cache for static resources
const clearImageCache = () => {
    // Remove preload links for unused images
    const preloadLinks = document.querySelectorAll('link[rel="preload"][as="image"]');
    preloadLinks.forEach(link => {
        if (link.href.includes('imagemcarr.jpg')) {
            link.remove();
            console.log('[Cache Clear] Removed unused preload:', link.href);
        }
    });
};

// Run cache clear on page load
document.addEventListener('DOMContentLoaded', clearImageCache);
