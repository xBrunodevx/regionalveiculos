// Preload Optimizer - Regional Veículos
// Gerencia preloads de forma inteligente para evitar warnings de performance

class PreloadOptimizer {
    constructor() {
        this.preloadedResources = new Set();
        this.usageTracker = new Map();
    }
    
    // Adiciona preload apenas quando necessário
    smartPreload(href, as, condition = true) {
        if (!condition || this.preloadedResources.has(href)) {
            return false;
        }
        
        const link = document.createElement('link');
        link.rel = 'preload';
        link.as = as;
        link.href = href;
        
        // Track quando foi adicionado
        this.usageTracker.set(href, Date.now());
        
        // Adicionar ao head
        document.head.appendChild(link);
        this.preloadedResources.add(href);
        
        console.log(`[Preload] Added: ${href}`);
        
        // Auto-remove se não usado em 10 segundos
        setTimeout(() => {
            this.removeUnusedPreload(href);
        }, 10000);
        
        return true;
    }
    
    // Remove preload se não foi usado
    removeUnusedPreload(href) {
        const link = document.querySelector(`link[rel="preload"][href="${href}"]`);
        if (link) {
            // Verificar se o recurso está sendo usado
            let isUsed = false;
            
            if (link.getAttribute('as') === 'image') {
                isUsed = Array.from(document.querySelectorAll('img')).some(img => 
                    img.src === href || img.src.includes(href.split('/').pop())
                );
            } else if (link.getAttribute('as') === 'style') {
                isUsed = document.querySelector(`link[href="${href}"][rel="stylesheet"]`) !== null;
            }
            
            if (!isUsed) {
                link.remove();
                this.preloadedResources.delete(href);
                console.log(`[Preload] Removed unused: ${href}`);
            } else {
                console.log(`[Preload] Kept in use: ${href}`);
            }
        }
    }
    
    // Otimiza todos os preloads existentes
    optimizeExistingPreloads() {
        const existingPreloads = document.querySelectorAll('link[rel="preload"]');
        existingPreloads.forEach(link => {
            const href = link.href;
            if (!this.preloadedResources.has(href)) {
                this.preloadedResources.add(href);
                this.usageTracker.set(href, Date.now());
                
                // Verificar uso em 3 segundos
                setTimeout(() => {
                    this.removeUnusedPreload(href);
                }, 3000);
            }
        });
    }
}

// Inicializar otimizador
const preloadOpt = new PreloadOptimizer();

// Executar quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    preloadOpt.optimizeExistingPreloads();
    
    // Fazer preloads inteligentes baseados no conteúdo da página
    setTimeout(() => {
        // Logo apenas se estiver na navbar
        const hasNavbar = document.querySelector('.navbar');
        preloadOpt.smartPreload('/static/images/logo-regional-veiculos.png', 'image', hasNavbar);
        
        // Outras imagens críticas apenas se houver elementos que as usam
        const hasCarousel = document.querySelector('.brands-carousel');
        const hasFloatingCar = document.querySelector('.floating-car-image');
        
    }, 500);
});

// Executar otimização após carregamento completo
window.addEventListener('load', () => {
    setTimeout(() => {
        preloadOpt.optimizeExistingPreloads();
    }, 2000);
});