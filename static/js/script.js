document.addEventListener('DOMContentLoaded', function() {
    // Mobile Menu Toggle
    const menuToggle = document.getElementById('menuToggle');
    const navLinks = document.getElementById('navLinks');
    
    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            const icon = menuToggle.querySelector('i');
            if (navLinks.classList.contains('active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    }

    // Flash Message Close
    const flashCloses = document.querySelectorAll('.flash-close');
    flashCloses.forEach(button => {
        button.addEventListener('click', function() {
            const message = this.parentElement;
            message.style.opacity = '0';
            message.style.transform = 'translateY(-10px)';
            setTimeout(() => message.remove(), 300);
        });
    });

    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            if (msg.parentElement) {
                msg.style.opacity = '0';
                msg.style.transform = 'translateY(-10px)';
                setTimeout(() => msg.remove(), 300);
            }
        }, 5000);
    });

    // Scroll Animation
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.card, .feature-card, .itinerary-day');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.1;
            
            if (elementPosition < screenPosition) {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }
        });
    };

    // Initialize elements for scroll animation
    document.querySelectorAll('.card, .feature-card, .itinerary-day').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'all 0.6s ease-out';
    });

    window.addEventListener('load', animateOnScroll);
    window.addEventListener('scroll', animateOnScroll);

    // Confirm Delete
    const deleteButtons = document.querySelectorAll('.btn-delete, .delete-trip');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this trip itinerary?')) {
                e.preventDefault();
            }
        });
    });
});