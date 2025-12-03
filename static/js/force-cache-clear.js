// Script para forçar limpeza de cache no desenvolvimento
(function() {
    'use strict';
    
    // Força reload sem cache no desenvolvimento
    if (location.hostname === '127.0.0.1' || location.hostname === 'localhost') {
        // Adiciona timestamp a todos os links CSS e JS
        const links = document.querySelectorAll('link[rel="stylesheet"]');
        const scripts = document.querySelectorAll('script[src]');
        const timestamp = '?v=' + Date.now();
        
        links.forEach(link => {
            if (link.href && !link.href.includes('?v=')) {
                link.href += timestamp;
            }
        });
        
        scripts.forEach(script => {
            if (script.src && !script.src.includes('?v=')) {
                script.src += timestamp;
            }
        });
        
        // Log para debug
        console.log('🔄 Cache invalidado para desenvolvimento');
    }
})();