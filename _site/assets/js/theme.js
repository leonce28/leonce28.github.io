(function() {
    // Theme management
    function getTheme() {
        return localStorage.getItem('theme') || 'dark';
    }

    function setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        updateToggleButton(theme);
    }

    function updateToggleButton(theme) {
        const icon = document.getElementById('theme-icon');
        const text = document.getElementById('theme-text');
        
        if (icon && text) {
            if (theme === 'light') {
                icon.textContent = '☀️';
                text.textContent = '浅色';
            } else {
                icon.textContent = '🌙';
                text.textContent = '深色';
            }
        }
    }

    function toggleTheme() {
        const currentTheme = getTheme();
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        setTheme(newTheme);
    }

    // Initialize theme
    setTheme(getTheme());

    // Bind toggle button
    const toggleBtn = document.getElementById('theme-toggle');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', toggleTheme);
    }

    // Mobile menu toggle
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    const mobileNav = document.querySelector('.mobile-nav');
    
    if (menuToggle && mobileNav) {
        menuToggle.addEventListener('click', function() {
            mobileNav.classList.toggle('active');
            
            // Animate hamburger icon
            const spans = this.querySelectorAll('span');
            spans.forEach((span, i) => {
                span.style.transform = mobileNav.classList.contains('active')
                    ? i === 0 ? 'rotate(45deg) translate(5px, 5px)'
                    : i === 1 ? 'opacity: 0'
                    : 'rotate(-45deg) translate(5px, -5px)'
                    : '';
            });
        });
    }

    // Close mobile menu when clicking outside
    document.addEventListener('click', function(e) {
        if (mobileNav && menuToggle) {
            if (!mobileNav.contains(e.target) && !menuToggle.contains(e.target)) {
                mobileNav.classList.remove('active');
            }
        }
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add copy button to code blocks
    document.querySelectorAll('pre code').forEach(codeBlock => {
        const pre = codeBlock.parentElement;
        const copyBtn = document.createElement('button');
        copyBtn.className = 'copy-btn';
        copyBtn.textContent = '复制';
        copyBtn.style.cssText = `
            position: absolute;
            top: 8px;
            right: 8px;
            padding: 4px 8px;
            font-size: 12px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 4px;
            cursor: pointer;
            color: var(--text-secondary);
        `;
        
        pre.style.position = 'relative';
        pre.appendChild(copyBtn);
        
        copyBtn.addEventListener('click', async () => {
            try {
                await navigator.clipboard.writeText(codeBlock.textContent);
                copyBtn.textContent = '已复制!';
                setTimeout(() => copyBtn.textContent = '复制', 2000);
            } catch (err) {
                console.error('Failed to copy:', err);
            }
        });
    });
})();
