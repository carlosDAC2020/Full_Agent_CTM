// Register usage of GSAP ScrollTrigger
gsap.registerPlugin(ScrollTrigger);

document.addEventListener('DOMContentLoaded', () => {

    // --- 1. INTRO ANIMATIONS (Process Flow) ---
    // Select all animation containers
    document.querySelectorAll('.intro-anim-container').forEach(container => {
        const steps = container.querySelectorAll('.anim-step');
        const connectors = container.querySelectorAll('.anim-connector');

        const tl = gsap.timeline({
            scrollTrigger: {
                trigger: container,
                start: "top 80%", // Start when top of container hits 80% viewport height
                toggleActions: "play none none reverse"
            }
        });

        // Animate Steps and Connectors sequentially
        steps.forEach((step, index) => {
            // Pop in the step
            tl.to(step, {
                y: 0,
                opacity: 1,
                duration: 0.5,
                ease: "back.out(1.7)"
            });

            // If there's a connector following this step, animate it filling up
            if (connectors[index]) {
                if (window.innerWidth > 600) {
                    // Horizontal fill
                    tl.to(connectors[index], {
                        "--fill-width": "100%", // CSS var approach or simple width check
                        opacity: 1,
                        duration: 0.3
                    }, "-=0.1"); // slight overlap
                } else {
                    // Vertical fill for mobile
                    tl.to(connectors[index], {
                        opacity: 1,
                        duration: 0.3
                    }, "-=0.1");
                }
            }
        });
    });

    // Connector CSS Hack: We can't animate pseudo-elements directly with GSAP easily without CSS vars.
    // Simpler approach: Just fade them in or use a real element relative to parent.
    // Refined approach: Use the CSS transition on the pseudo-class and just add a class.

    // REDO ANIMATION LOGIC FOR CONNECTORS TO BE SIMPLER WITH CLASSES
    const observerOptions = { threshold: 0.5 };
    const stepObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, observerOptions);

    // --- 2. MAGAZINE SECTION ANIMATION ---
    gsap.to(".mag-image-container", {
        scrollTrigger: {
            trigger: ".mag-showcase",
            start: "top 75%"
        },
        x: 0,
        opacity: 1,
        duration: 1,
        ease: "power3.out"
    });

    gsap.to(".mag-content", {
        scrollTrigger: {
            trigger: ".mag-showcase",
            start: "top 75%"
        },
        x: 0,
        opacity: 1,
        duration: 1,
        delay: 0.3,
        ease: "power3.out"
    });


    // --- 3. AGENT SECTION (Pinterest Grid Stagger) ---
    gsap.to(".pin-item", {
        scrollTrigger: {
            trigger: ".pinterest-grid",
            start: "top 85%"
        },
        y: 0,
        opacity: 1,
        duration: 0.8,
        stagger: 0.2, // Pinterest stagger effect
        ease: "power2.out"
    });


    // --- 4. LIGHTBOX LOGIC ---
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxTitle = document.getElementById('lightbox-title');
    const lightboxDesc = document.getElementById('lightbox-desc');
    const closeBtn = document.querySelector('.lightbox-close');

    // Open
    document.querySelectorAll('.pin-item').forEach(item => {
        item.addEventListener('click', () => {
            const imgParams = {
                src: item.getAttribute('data-img'),
                title: item.getAttribute('data-title'),
                desc: item.getAttribute('data-desc')
            };

            lightboxImg.src = imgParams.src;
            lightboxTitle.textContent = imgParams.title;
            lightboxDesc.textContent = imgParams.desc;

            lightbox.classList.add('active');
            document.body.style.overflow = 'hidden'; // Prevent scrolling
        });
    });

    // Close
    function closeLightbox() {
        lightbox.classList.remove('active');
        document.body.style.overflow = ''; // Restore scrolling
        // Clear src after delay to prevent ugly flash
        setTimeout(() => lightboxImg.src = '', 300);
    }

    closeBtn.addEventListener('click', closeLightbox);

    // Close on background click
    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) {
            closeLightbox();
        }
    });

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && lightbox.classList.contains('active')) {
            closeLightbox();
        }
    });

});
