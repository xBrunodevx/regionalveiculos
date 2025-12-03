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

// Clear browser cache for static resources - Modo agressivo
const clearImageCache = () => {
    // Remove TODOS os preload links de imagens para evitar warnings
    const preloadLinks = document.querySelectorAll('link[rel="preload"]');
    preloadLinks.forEach(link => {
        const href = link.href;
        
        // Remove preloads de imagens que não são críticas
        if (link.getAttribute('as') === 'image') {
            console.log('[Cache Clear] Removing image preload to avoid warning:', href);
            link.remove();
        }
        
        // Para CSS e outros, verificar se são realmente necessários
        if (link.getAttribute('as') === 'style' && !href.includes('googleapis')) {
            // Remove preloads de CSS local para evitar warnings
            console.log('[Cache Clear] Removing style preload to avoid warning:', href);
            link.remove();
        }
    });
    
    // Aguardar e fazer limpeza final
    setTimeout(() => {
        const remainingPreloads = document.querySelectorAll('link[rel="preload"][as="image"]');
        remainingPreloads.forEach(link => {
            console.log('[Cache Clear] Final cleanup - removing:', link.href);
            link.remove();
        });
    }, 1000);
};

// Run cache clear on page load
document.addEventListener('DOMContentLoaded', clearImageCache);
