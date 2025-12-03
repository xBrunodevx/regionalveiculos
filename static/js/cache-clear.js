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

// Clear browser cache for static resources - Otimizado
const clearImageCache = () => {
    // Remove preload links para imagens não utilizadas
    const preloadLinks = document.querySelectorAll('link[rel="preload"]');
    preloadLinks.forEach(link => {
        // Verificar se a imagem/recurso está sendo usado
        const href = link.href;
        
        // Para imagens, verificar se há elementos img usando o recurso
        if (link.getAttribute('as') === 'image') {
            const isUsed = Array.from(document.querySelectorAll('img')).some(img => 
                img.src && img.src.includes(href.split('/').pop())
            );
            
            if (!isUsed) {
                console.log('[Cache Clear] Removed unused image preload:', href);
                link.remove();
            }
        }
        
        // Para CSS, verificar se foi carregado há mais de 5 segundos
        if (link.getAttribute('as') === 'style' && link.hasAttribute('onload')) {
            setTimeout(() => {
                if (document.head.contains(link) && !document.querySelector(`link[href="${href}"][rel="stylesheet"]`)) {
                    console.log('[Cache Clear] Removed unused style preload:', href);
                    link.remove();
                }
            }, 5000);
        }
    });
};

// Run cache clear on page load
document.addEventListener('DOMContentLoaded', clearImageCache);
