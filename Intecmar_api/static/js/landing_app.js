// Register usage of GSAP ScrollTrigger
gsap.registerPlugin(ScrollTrigger);

document.addEventListener('DOMContentLoaded', () => {

    /**
     * 1. REUSABLE SEQUENTIAL ANIMATION FUNCTION
     * Animates steps -> connectors -> target content
     */
    function createSequentialTimeline(sectionId, targetElements) {
        const container = document.querySelector(`${sectionId} .intro-anim-container`);
        if (!container) return;

        const steps = container.querySelectorAll('.anim-step');
        const connectors = container.querySelectorAll('.anim-connector');

        const mainTl = gsap.timeline({
            scrollTrigger: {
                trigger: sectionId,
                start: "top 70%",
                toggleActions: "play none none none"
            }
        });

        // Step 1: Sequential steps and connectors
        steps.forEach((step, index) => {
            mainTl.to(step, {
                y: 0,
                opacity: 1,
                duration: 0.6,
                ease: "back.out(1.7)",
                onStart: () => step.classList.add('active')
            }, index === 0 ? 0 : "-=0.4");

            if (connectors[index]) {
                mainTl.to(connectors[index], {
                    opacity: 1,
                    onStart: () => connectors[index].classList.add('active')
                }, "-=0.3");
            }
        });

        // Step 2: Reveal the main content (Gallery or Hero Image)
        targetElements.forEach((el, index) => {
            mainTl.to(el, {
                opacity: 1,
                y: 0,
                duration: 0.8,
                stagger: 0.1,
                ease: "power2.out"
            }, "-=0.2");
        });
    }

    // Initialize Magazine Section Sequence
    createSequentialTimeline('#magazine-showcase', ['.mag-showcase']);

    // Initialize Agent Section Sequence
    createSequentialTimeline('#agent-process', ['.pinterest-grid', '.pin-item']);


    /**
     * 2. INTERACTIVE MASONRY / PINTEREST LOGIC
     */
    const pinItems = document.querySelectorAll('.pin-item');
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxTitle = document.getElementById('lightbox-title');
    const lightboxDesc = document.getElementById('lightbox-desc');
    const overlay = document.createElement('div');
    overlay.className = 'gallery-focus-overlay';
    document.body.appendChild(overlay);

    pinItems.forEach((pin, index) => {
        pin.addEventListener('click', () => {
            const rect = pin.getBoundingClientRect();

            // Show overlay
            overlay.classList.add('active');

            // Update Lightbox Content
            lightboxImg.src = pin.getAttribute('data-img');
            lightboxTitle.textContent = pin.getAttribute('data-title');
            lightboxDesc.textContent = pin.getAttribute('data-desc');

            // Animate Lightbox Opening (Scale from original position)
            gsap.fromTo('.lightbox-content',
                { scale: 0.5, opacity: 0, y: 50 },
                { scale: 1, opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }
            );

            lightbox.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    });

    // Close Lightbox
    const closeLightbox = () => {
        gsap.to('.lightbox-content', {
            scale: 0.8,
            opacity: 0,
            duration: 0.3,
            ease: "power2.in",
            onComplete: () => {
                lightbox.classList.remove('active');
                overlay.classList.remove('active');
                document.body.style.overflow = '';
                lightboxImg.src = ''; // Clean up
            }
        });
    };

    document.querySelector('.lightbox-close').addEventListener('click', closeLightbox);
    overlay.addEventListener('click', closeLightbox);

    // Close on Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && lightbox.classList.contains('active')) closeLightbox();
    });

    /**
     * 3. MICRO-INTERACTIONS
     */
    // Spotlight follows mouse for a premium feel
    document.addEventListener('mousemove', (e) => {
        const { clientX, clientY } = e;
        gsap.to('body', {
            '--mouse-x': clientX + 'px',
            '--mouse-y': clientY + 'px',
            duration: 0.3,
            ease: "power2.out"
        });
    });

});
