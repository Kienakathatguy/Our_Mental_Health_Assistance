/**
 * Skeleton Loader Utility
 * Shows skeleton placeholders during page transitions and loading states
 */

class SkeletonLoader {
    constructor() {
        this.loaderElement = null;
    }

    /**
     * Initialize skeleton loader overlay
     */
    init() {
        if (!document.getElementById('skeleton-loader-overlay')) {
            const overlay = document.createElement('div');
            overlay.id = 'skeleton-loader-overlay';
            overlay.innerHTML = `
                <div class="skeleton-loader-content">
                    <div class="skeleton-card">
                        <div class="skeleton-text" style="width: 30%; height: 20px; margin-bottom: 16px;"></div>
                        <div class="skeleton-text" style="width: 100%; height: 12px; margin-bottom: 8px;"></div>
                        <div class="skeleton-text" style="width: 95%; height: 12px; margin-bottom: 8px;"></div>
                        <div class="skeleton-text" style="width: 80%; height: 12px; margin-bottom: 16px;"></div>
                    </div>
                    <div class="skeleton-card">
                        <div class="skeleton-text" style="width: 35%; height: 20px; margin-bottom: 16px;"></div>
                        <div class="skeleton-text" style="width: 100%; height: 12px; margin-bottom: 8px;"></div>
                        <div class="skeleton-text" style="width: 92%; height: 12px; margin-bottom: 8px;"></div>
                        <div class="skeleton-text" style="width: 75%; height: 12px;"></div>
                    </div>
                </div>
            `;
            overlay.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(255, 255, 255, 0.95);
                display: none;
                z-index: 9999;
                overflow: auto;
                padding: 40px 20px;
                transition: opacity 0.3s ease;
            `;
            document.body.appendChild(overlay);
        }
        this.loaderElement = document.getElementById('skeleton-loader-overlay');
    }

    /**
     * Show the skeleton loader overlay
     */
    show() {
        if (this.loaderElement) {
            this.loaderElement.style.display = 'block';
            setTimeout(() => {
                this.loaderElement.style.opacity = '1';
            }, 10);
        }
    }

    /**
     * Hide the skeleton loader overlay
     */
    hide() {
        if (this.loaderElement) {
            this.loaderElement.style.opacity = '0';
            setTimeout(() => {
                this.loaderElement.style.display = 'none';
            }, 300);
        }
    }

    /**
     * Show skeleton with custom delay
     */
    showWithDelay(delay = 300) {
        setTimeout(() => this.show(), delay);
    }

    /**
     * Hide skeleton with custom delay
     */
    hideWithDelay(delay = 500) {
        setTimeout(() => this.hide(), delay);
    }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', function () {
    window.skeletonLoader = new SkeletonLoader();
    window.skeletonLoader.init();

    // Show skeleton on navigation links
    document.querySelectorAll('a[href*="#"]').forEach(link => {
        link.addEventListener('click', function (e) {
            // Don't show loader for anchor links
            if (this.getAttribute('href').startsWith('#')) {
                return;
            }
        });
    });

    // Show skeleton on form submissions that navigate
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function () {
            // Only show if form action navigates away
            if (this.getAttribute('action') && 
                !this.getAttribute('action').includes('#')) {
                window.skeletonLoader.showWithDelay(100);
            }
        });
    });
});

// Show skeleton when navigating to different features
function navigateWithSkeleton(url) {
    if (window.skeletonLoader) {
        window.skeletonLoader.show();
        setTimeout(() => {
            window.location.href = url;
        }, 200);
    } else {
        window.location.href = url;
    }
}
