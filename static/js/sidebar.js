/**
 * JT Sistemas - Interactive Sidebar Manager
 * Handles sidebar behavior, animations, and responsive functionality
 */

class SidebarManager {
    constructor() {
        this.sidebar = document.getElementById('sidebar');
        this.sidebarToggle = document.getElementById('sidebarToggle');
        this.sidebarOverlay = document.getElementById('sidebarOverlay');
        this.mainContent = document.getElementById('mainContent');
        
        this.isMobile = window.innerWidth <= 768;
        this.isExpanded = false;
        this.hoverTimeout = null;
        this.touchDevice = this.isTouchDevice();
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.handleResize();
        this.highlightActiveRoute();
        this.setupDropdowns();
        
        // Initialize sidebar state
        if (this.isMobile) {
            this.sidebar.classList.remove('expanded');
        }
    }
    
    setupEventListeners() {
        // Mobile toggle
        if (this.sidebarToggle) {
            this.sidebarToggle.addEventListener('click', () => {
                this.toggleMobileSidebar();
            });
        }
        
        // Overlay click to close
        if (this.sidebarOverlay) {
            this.sidebarOverlay.addEventListener('click', () => {
                this.closeMobileSidebar();
            });
        }
        
        // Desktop hover behavior (only for non-touch devices)
        if (!this.touchDevice) {
            this.sidebar.addEventListener('mouseenter', () => {
                this.handleMouseEnter();
            });
            
            this.sidebar.addEventListener('mouseleave', () => {
                this.handleMouseLeave();
            });
        }
        
        // Window resize
        window.addEventListener('resize', () => {
            this.handleResize();
        });
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            this.handleKeyboard(e);
        });
        
        // Prevent sidebar close on interaction
        this.sidebar.addEventListener('click', (e) => {
            e.stopPropagation();
        });
        
        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', (e) => {
            if (this.isMobile && this.sidebar.classList.contains('show')) {
                if (!this.sidebar.contains(e.target) && !this.sidebarToggle.contains(e.target)) {
                    this.closeMobileSidebar();
                }
            }
        });
    }
    
    setupDropdowns() {
        const dropdownToggles = this.sidebar.querySelectorAll('[data-bs-toggle="collapse"]');
        
        dropdownToggles.forEach(toggle => {
            toggle.addEventListener('click', (e) => {
                e.preventDefault();
                this.handleDropdownClick(toggle);
            });
        });
    }
    
    handleDropdownClick(toggle) {
        const targetId = toggle.getAttribute('data-bs-target');
        const targetElement = document.querySelector(targetId);
        const isExpanded = toggle.getAttribute('aria-expanded') === 'true';
        
        // Close other dropdowns
        this.closeOtherDropdowns(targetId);
        
        // Toggle current dropdown
        if (isExpanded) {
            this.closeDropdown(toggle, targetElement);
        } else {
            this.openDropdown(toggle, targetElement);
        }
    }
    
    openDropdown(toggle, targetElement) {
        toggle.setAttribute('aria-expanded', 'true');
        targetElement.classList.add('show');
        
        // Add rotation to chevron icon
        const icon = toggle.querySelector('.dropdown-icon');
        if (icon) {
            icon.style.transform = 'rotate(180deg)';
        }
    }
    
    closeDropdown(toggle, targetElement) {
        toggle.setAttribute('aria-expanded', 'false');
        targetElement.classList.remove('show');
        
        // Remove rotation from chevron icon
        const icon = toggle.querySelector('.dropdown-icon');
        if (icon) {
            icon.style.transform = 'rotate(0deg)';
        }
    }
    
    closeOtherDropdowns(currentTargetId) {
        const allDropdowns = this.sidebar.querySelectorAll('[data-bs-toggle="collapse"]');
        
        allDropdowns.forEach(dropdown => {
            const targetId = dropdown.getAttribute('data-bs-target');
            if (targetId !== currentTargetId) {
                const targetElement = document.querySelector(targetId);
                this.closeDropdown(dropdown, targetElement);
            }
        });
    }
    
    handleMouseEnter() {
        if (this.isMobile || this.touchDevice) return;
        
        clearTimeout(this.hoverTimeout);
        this.expandSidebar();
    }
    
    handleMouseLeave() {
        if (this.isMobile || this.touchDevice) return;
        
        // Add delay before collapsing
        this.hoverTimeout = setTimeout(() => {
            this.collapseSidebar();
        }, 300);
    }
    
    expandSidebar() {
        if (!this.isMobile) {
            this.sidebar.classList.add('expanded');
            this.isExpanded = true;
        }
    }
    
    collapseSidebar() {
        if (!this.isMobile) {
            this.sidebar.classList.remove('expanded');
            this.isExpanded = false;
        }
    }
    
    toggleMobileSidebar() {
        if (this.isMobile) {
            const isOpen = this.sidebar.classList.contains('show');
            
            if (isOpen) {
                this.closeMobileSidebar();
            } else {
                this.openMobileSidebar();
            }
        }
    }
    
    openMobileSidebar() {
        this.sidebar.classList.add('show');
        this.sidebarOverlay.classList.add('show');
        document.body.style.overflow = 'hidden';
        
        // Focus management for accessibility
        const firstLink = this.sidebar.querySelector('.nav-link');
        if (firstLink) {
            firstLink.focus();
        }
    }
    
    closeMobileSidebar() {
        this.sidebar.classList.remove('show');
        this.sidebarOverlay.classList.remove('show');
        document.body.style.overflow = '';
        
        // Return focus to toggle button
        if (this.sidebarToggle) {
            this.sidebarToggle.focus();
        }
    }
    
    handleResize() {
        const wasMobile = this.isMobile;
        this.isMobile = window.innerWidth <= 768;
        
        // Handle mobile/desktop transition
        if (wasMobile && !this.isMobile) {
            // Switched from mobile to desktop
            this.closeMobileSidebar();
            this.sidebar.classList.remove('expanded');
        } else if (!wasMobile && this.isMobile) {
            // Switched from desktop to mobile
            this.sidebar.classList.remove('expanded');
            this.closeMobileSidebar();
        }
    }
    
    highlightActiveRoute() {
        const currentPath = window.location.pathname;
        const navLinks = this.sidebar.querySelectorAll('.nav-link');
        
        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            
            // Remove active class
            link.classList.remove('active');
            
            // Check if current path matches link
            if (href && (currentPath === href || currentPath.startsWith(href + '/'))) {
                link.classList.add('active');
                
                // Expand parent dropdown if link is inside a dropdown
                const parentCollapse = link.closest('.collapse');
                if (parentCollapse) {
                    const parentToggle = this.sidebar.querySelector(`[data-bs-target="#${parentCollapse.id}"]`);
                    if (parentToggle) {
                        this.openDropdown(parentToggle, parentCollapse);
                    }
                }
            }
        });
    }
    
    handleKeyboard(e) {
        // ESC key to close mobile sidebar
        if (e.key === 'Escape' && this.isMobile && this.sidebar.classList.contains('show')) {
            this.closeMobileSidebar();
        }
        
        // Arrow key navigation within sidebar
        if (document.activeElement.closest('.sidebar')) {
            this.handleArrowNavigation(e);
        }
    }
    
    handleArrowNavigation(e) {
        const focusableElements = this.sidebar.querySelectorAll('.nav-link:not(.collapsed)');
        const currentIndex = Array.from(focusableElements).indexOf(document.activeElement);
        
        let nextIndex;
        
        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                nextIndex = currentIndex + 1;
                if (nextIndex >= focusableElements.length) nextIndex = 0;
                focusableElements[nextIndex].focus();
                break;
                
            case 'ArrowUp':
                e.preventDefault();
                nextIndex = currentIndex - 1;
                if (nextIndex < 0) nextIndex = focusableElements.length - 1;
                focusableElements[nextIndex].focus();
                break;
        }
    }
    
    isTouchDevice() {
        return (('ontouchstart' in window) ||
                (navigator.maxTouchPoints > 0) ||
                (navigator.msMaxTouchPoints > 0));
    }
    
    // Public methods for external use
    
    /**
     * Programmatically open mobile sidebar
     */
    open() {
        if (this.isMobile) {
            this.openMobileSidebar();
        } else {
            this.expandSidebar();
        }
    }
    
    /**
     * Programmatically close mobile sidebar
     */
    close() {
        if (this.isMobile) {
            this.closeMobileSidebar();
        } else {
            this.collapseSidebar();
        }
    }
    
    /**
     * Check if sidebar is currently open/expanded
     */
    isOpen() {
        if (this.isMobile) {
            return this.sidebar.classList.contains('show');
        } else {
            return this.isExpanded;
        }
    }
    
    /**
     * Update active navigation item
     */
    updateActiveRoute(path) {
        const navLinks = this.sidebar.querySelectorAll('.nav-link');
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            
            const href = link.getAttribute('href');
            if (href && (path === href || path.startsWith(href + '/'))) {
                link.classList.add('active');
            }
        });
    }
    
    /**
     * Destroy the sidebar manager
     */
    destroy() {
        // Remove event listeners
        if (this.sidebarToggle) {
            this.sidebarToggle.removeEventListener('click', this.toggleMobileSidebar);
        }
        
        if (this.sidebarOverlay) {
            this.sidebarOverlay.removeEventListener('click', this.closeMobileSidebar);
        }
        
        window.removeEventListener('resize', this.handleResize);
        document.removeEventListener('keydown', this.handleKeyboard);
        
        // Clear timeouts
        clearTimeout(this.hoverTimeout);
        
        // Reset styles
        document.body.style.overflow = '';
    }
}

// Auto-initialize if DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.sidebarManager = new SidebarManager();
    });
} else {
    window.sidebarManager = new SidebarManager();
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SidebarManager;
}