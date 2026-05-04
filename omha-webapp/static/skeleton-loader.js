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
            overlay.innerHTML = this.getSkeletonContent();
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
     * Get appropriate skeleton content based on current page
     */
    getSkeletonContent() {
        const path = window.location.pathname;

        if (path.includes('/diary')) {
            return this.getDiarySkeleton();
        } else if (path.includes('/chat') || path.includes('/chatbot')) {
            return this.getChatSkeleton();
        } else if (path.includes('/forum')) {
            return this.getForumSkeleton();
        } else {
            return this.getDefaultSkeleton();
        }
    }

    /**
     * Diary page skeleton matching the exact layout
     */
    getDiarySkeleton() {
        return `
            <div class="skeleton-loader-content container">
                <!-- Diary Entry Form Card -->
                <div class="card shadow-sm p-4 mb-4 bg-white rounded skeleton-card">
                    <div class="skeleton-text" style="width: 40%; height: 28px; margin-bottom: 24px;"></div>

                    <!-- Form rows -->
                    <div class="row g-3 mb-3">
                        <div class="col-md-6">
                            <div class="skeleton-text" style="width: 30%; height: 16px; margin-bottom: 8px;"></div>
                            <div class="skeleton-text" style="width: 100%; height: 38px;"></div>
                        </div>
                        <div class="col-md-6">
                            <div class="skeleton-text" style="width: 25%; height: 16px; margin-bottom: 8px;"></div>
                            <div class="skeleton-text" style="width: 100%; height: 38px;"></div>
                        </div>
                    </div>

                    <div class="row g-3 mb-3">
                        <div class="col-md-6">
                            <div class="skeleton-text" style="width: 20%; height: 16px; margin-bottom: 8px;"></div>
                            <div class="skeleton-text" style="width: 100%; height: 38px;"></div>
                        </div>
                        <div class="col-md-6">
                            <div class="skeleton-text" style="width: 25%; height: 16px; margin-bottom: 8px;"></div>
                            <div class="skeleton-text" style="width: 100%; height: 38px;"></div>
                        </div>
                    </div>

                    <div class="row align-items-end mb-3">
                        <div class="col-md-6">
                            <div class="skeleton-text" style="width: 35%; height: 16px; margin-bottom: 8px;"></div>
                            <div class="skeleton-text" style="width: 100%; height: 38px;"></div>
                        </div>
                        <div class="col-md-6 text-md-end mt-3 mt-md-0">
                            <div class="skeleton-text" style="width: 120px; height: 32px; margin-left: auto;"></div>
                            <div class="skeleton-text" style="width: 100px; height: 32px; margin-left: 8px;"></div>
                        </div>
                    </div>

                    <div class="mb-3">
                        <div class="skeleton-text" style="width: 25%; height: 16px; margin-bottom: 8px;"></div>
                        <div class="skeleton-text" style="width: 100%; height: 38px;"></div>
                    </div>

                    <!-- Journal prompt -->
                    <div class="alert alert-info mb-3">
                        <div class="skeleton-text" style="width: 20%; height: 16px; margin-bottom: 8px;"></div>
                        <div class="skeleton-text" style="width: 85%; height: 14px;"></div>
                    </div>

                    <!-- Toolbar -->
                    <div class="journal-toolbar mb-2">
                        <div class="skeleton-text" style="width: 32px; height: 32px; display: inline-block; margin-right: 4px;"></div>
                        <div class="skeleton-text" style="width: 32px; height: 32px; display: inline-block; margin-right: 4px;"></div>
                        <div class="skeleton-text" style="width: 32px; height: 32px; display: inline-block; margin-right: 4px;"></div>
                        <div class="skeleton-text" style="width: 32px; height: 32px; display: inline-block; margin-right: 4px;"></div>
                        <div class="skeleton-text" style="width: 32px; height: 32px; display: inline-block; margin-right: 4px;"></div>
                        <div class="skeleton-text" style="width: 32px; height: 32px; display: inline-block;"></div>
                    </div>

                    <!-- Sticker library -->
                    <div class="mb-3">
                        <div class="skeleton-text" style="width: 15%; height: 16px; margin-bottom: 8px;"></div>
                        <div class="sticker-library mb-2">
                            ${Array(10).fill().map(() => '<div class="skeleton-text" style="width: 32px; height: 32px; display: inline-block; margin-right: 4px;"></div>').join('')}
                        </div>
                    </div>

                    <!-- Textarea -->
                    <div class="skeleton-text" style="width: 100%; height: 120px; margin-bottom: 16px;"></div>

                    <!-- Templates -->
                    <div class="mb-3">
                        <div class="skeleton-text" style="width: 25%; height: 16px; margin-bottom: 8px;"></div>
                        <div class="d-flex flex-wrap gap-2">
                            ${Array(4).fill().map(() => '<div class="skeleton-text" style="width: 80px; height: 32px; display: inline-block;"></div>').join('')}
                        </div>
                    </div>

                    <!-- Reflection prompt -->
                    <div class="mb-4">
                        <div class="skeleton-text" style="width: 25%; height: 14px; margin-bottom: 4px;"></div>
                        <div class="skeleton-text" style="width: 90%; height: 14px;"></div>
                    </div>

                    <!-- Save button -->
                    <div class="skeleton-text" style="width: 120px; height: 38px;"></div>
                </div>

                <!-- Horizontal rule -->
                <hr class="my-4">

                <!-- Recent entries heading -->
                <div class="skeleton-text" style="width: 35%; height: 24px; margin-bottom: 24px;"></div>

                <!-- Diary entry cards -->
                ${Array(3).fill().map(() => `
                    <div class="card mb-3 skeleton-card">
                        <div class="card-header d-flex justify-content-between">
                            <div class="skeleton-text" style="width: 40%; height: 18px;"></div>
                            <div class="skeleton-text" style="width: 24px; height: 18px;"></div>
                        </div>
                        <div class="card-body">
                            <!-- Image placeholder -->
                            <div class="skeleton-text" style="width: 100%; height: 200px; margin-bottom: 16px;"></div>
                            <!-- Content -->
                            <div class="skeleton-text" style="width: 100%; height: 12px; margin-bottom: 6px;"></div>
                            <div class="skeleton-text" style="width: 95%; height: 12px; margin-bottom: 6px;"></div>
                            <div class="skeleton-text" style="width: 88%; height: 12px; margin-bottom: 6px;"></div>
                            <div class="skeleton-text" style="width: 92%; height: 12px; margin-bottom: 16px;"></div>
                            <!-- Stickers -->
                            <div class="mt-2">
                                <div class="skeleton-text" style="width: 24px; height: 20px; display: inline-block; margin-right: 4px;"></div>
                                <div class="skeleton-text" style="width: 24px; height: 20px; display: inline-block; margin-right: 4px;"></div>
                                <div class="skeleton-text" style="width: 24px; height: 20px; display: inline-block;"></div>
                            </div>
                            <!-- Action buttons -->
                            <div class="skeleton-text" style="width: 60px; height: 32px; display: inline-block; margin-right: 8px;"></div>
                            <div class="skeleton-text" style="width: 60px; height: 32px; display: inline-block;"></div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    /**
     * Chat page skeleton
     */
    getChatSkeleton() {
        return `
            <div class="skeleton-loader-content container">
                <div class="skeleton-card" style="height: 60px; margin-bottom: 20px;"></div>
                ${Array(5).fill().map(() => `
                    <div class="skeleton-card" style="margin-bottom: 16px;">
                        <div class="skeleton-text" style="width: 20%; height: 16px; margin-bottom: 8px;"></div>
                        <div class="skeleton-text" style="width: 100%; height: 12px; margin-bottom: 6px;"></div>
                        <div class="skeleton-text" style="width: 85%; height: 12px; margin-bottom: 6px;"></div>
                        <div class="skeleton-text" style="width: 70%; height: 12px;"></div>
                    </div>
                `).join('')}
                <div class="skeleton-card" style="height: 80px; margin-top: 20px;"></div>
            </div>
        `;
    }

    /**
     * Forum page skeleton
     */
    getForumSkeleton() {
        return `
            <div class="skeleton-loader-content container">
                <div class="skeleton-card" style="height: 100px; margin-bottom: 24px;"></div>
                ${Array(4).fill().map(() => `
                    <div class="skeleton-card" style="margin-bottom: 20px;">
                        <div class="skeleton-text" style="width: 30%; height: 20px; margin-bottom: 12px;"></div>
                        <div class="skeleton-text" style="width: 100%; height: 14px; margin-bottom: 8px;"></div>
                        <div class="skeleton-text" style="width: 90%; height: 14px; margin-bottom: 8px;"></div>
                        <div class="skeleton-text" style="width: 60%; height: 14px; margin-bottom: 12px;"></div>
                        <div class="skeleton-text" style="width: 40%; height: 16px;"></div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    /**
     * Default generic skeleton
     */
    getDefaultSkeleton() {
        return `
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
    }

    /**
     * Show the skeleton loader overlay
     */
    show() {
        // Refresh skeleton content based on current page
        this.init();
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
    window.skeletonLoader.skipOnUnload = false;

    // Show skeleton on internal navigation links
    document.querySelectorAll('a[href]').forEach(link => {
        link.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (!href || href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:')) {
                return;
            }
            if (this.target && this.target !== '_self') {
                return;
            }
            if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) {
                return;
            }
            if (window.skeletonLoader) {
                window.skeletonLoader.showWithDelay(50);
            }
        });
    });

    // Show skeleton on form submissions that navigate, except chatbot response submissions
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function () {
            if (this.id === 'chat-form') {
                if (window.skeletonLoader) {
                    window.skeletonLoader.skipOnUnload = true;
                }
                return;
            }
            if (this.getAttribute('action') && !this.getAttribute('action').includes('#')) {
                if (window.skeletonLoader) {
                    window.skeletonLoader.showWithDelay(100);
                }
            }
        });
    });

    window.addEventListener('beforeunload', function () {
        if (window.skeletonLoader && !window.skeletonLoader.skipOnUnload) {
            window.skeletonLoader.show();
        }
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
