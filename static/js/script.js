// Flash message handling
function hideFlash() {
    const flash = document.getElementById('flashMsg');
    if (flash) {
        flash.classList.add('hide');
        setTimeout(() => {
            flash.style.display = 'none';
        }, 300);
    }
}

// Auto-hide flash message after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const flash = document.getElementById('flashMsg');
    if (flash) {
        // Set timeout to match the progress bar animation (5 seconds)
        setTimeout(hideFlash, 5000);
    }
});

function toggleMobileNav() {
    const navLinks = document.getElementById("navLinks");
    navLinks.classList.toggle("show");
}

window.addEventListener("DOMContentLoaded", () => {
    const chipsContainer = document.getElementById('chipsContainer');
    let isDown = false, startX, scrollLeft;

    chipsContainer.addEventListener('wheel', e => {
        e.preventDefault();
        chipsContainer.scrollLeft += e.deltaY;
    });

    chipsContainer.addEventListener('mousedown', e => {
        isDown = true;
        chipsContainer.classList.add('active');
        startX = e.pageX - chipsContainer.offsetLeft;
        scrollLeft = chipsContainer.scrollLeft;
    });

    chipsContainer.addEventListener('mouseleave', () => isDown = false);
    chipsContainer.addEventListener('mouseup', () => isDown = false);

    chipsContainer.addEventListener('mousemove', e => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - chipsContainer.offsetLeft;
        const walk = (x - startX) * 2;
        chipsContainer.scrollLeft = scrollLeft - walk;
    });

    chipsContainer.addEventListener('touchstart', e => {
        startX = e.touches[0].pageX - chipsContainer.offsetLeft;
        scrollLeft = chipsContainer.scrollLeft;
    });

    chipsContainer.addEventListener('touchmove', e => {
        const x = e.touches[0].pageX - chipsContainer.offsetLeft;
        const walk = (x - startX) * 1.5;
        chipsContainer.scrollLeft = scrollLeft - walk;
    });

    document.querySelector('.scroll-btn.left')?.addEventListener('click', () => {
        chipsContainer.scrollBy({ left: -300, behavior: 'smooth' });
    });

    document.querySelector('.scroll-btn.right')?.addEventListener('click', () => {
        chipsContainer.scrollBy({ left: 300, behavior: 'smooth' });
    });
});

// Mobile navigation toggle
function toggleNav() {
    const navLinks = document.getElementById("navLinks");
    navLinks.classList.toggle("show");
    
    // Add animation effect
    const hamburger = document.querySelector(".hamburger");
    hamburger.classList.toggle("active");
    
    // Accessibility
    const expanded = navLinks.classList.contains("show");
    hamburger.setAttribute("aria-expanded", expanded);
}

// Close mobile nav when clicking outside
document.addEventListener('click', function(e) {
    const navLinks = document.getElementById("navLinks");
    const hamburger = document.querySelector(".hamburger");
    
    if (navLinks.classList.contains("show") && 
        !navLinks.contains(e.target) && 
        !hamburger.contains(e.target)) {
        toggleNav();
    }
});
