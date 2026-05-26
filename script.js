document.addEventListener('DOMContentLoaded', () => {
    // Mobile Navigation
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    if (hamburger) {
        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
    }

    // Placeholder functions for buttons if needed
    window.requestBooking = function () {
        alert("Thank you for your interest! Booking features coming soon.");
    };

    // Lightbox Logic
    const lightbox = document.getElementById('lightbox');
    if (lightbox) {
        const lightboxImg = document.getElementById('lightbox-img');
        const closeBtn = document.querySelector('.lightbox-close');
        const prevBtn = document.querySelector('.lightbox-prev');
        const nextBtn = document.querySelector('.lightbox-next');
        const galleryImages = Array.from(document.querySelectorAll('.masonry-item img'));
        
        let currentIndex = 0;

        // Open Lightbox
        galleryImages.forEach((img, index) => {
            img.style.cursor = 'pointer';
            img.addEventListener('click', () => {
                currentIndex = index;
                showLightboxImage(currentIndex);
                lightbox.style.display = 'block';
                document.body.style.overflow = 'hidden'; // Prevent scrolling
            });
        });

        function showLightboxImage(index) {
            lightboxImg.src = galleryImages[index].src;
        }

        function closeLightbox() {
            lightbox.style.display = 'none';
            document.body.style.overflow = 'auto'; // Re-enable scrolling
        }

        closeBtn.addEventListener('click', closeLightbox);

        // Click outside to close
        lightbox.addEventListener('click', (e) => {
            if (e.target === lightbox || e.target.classList.contains('lightbox-content-wrapper')) {
                closeLightbox();
            }
        });

        // Prev/Next Navigation
        function showNext() {
            currentIndex = (currentIndex + 1) % galleryImages.length;
            showLightboxImage(currentIndex);
        }

        function showPrev() {
            currentIndex = (currentIndex - 1 + galleryImages.length) % galleryImages.length;
            showLightboxImage(currentIndex);
        }

        nextBtn.addEventListener('click', showNext);
        prevBtn.addEventListener('click', showPrev);

        // Keyboard Navigation
        document.addEventListener('keydown', (e) => {
            if (lightbox.style.display === 'block') {
                if (e.key === 'Escape') closeLightbox();
                if (e.key === 'ArrowRight') showNext();
                if (e.key === 'ArrowLeft') showPrev();
            }
        });
    }
});
