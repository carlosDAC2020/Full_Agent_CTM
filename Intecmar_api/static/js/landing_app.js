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
     * 2. INTERACTIVE HOVER LOGIC
     * Descriptions now appear as overlays on hover via CSS.
     * Click interaction removed as requested.
     */
    const pinItems = document.querySelectorAll('.pin-item');
    pinItems.forEach(pin => {
        pin.style.cursor = 'default';
        // No click event needed
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
            duration: 0.4,
            ease: "power2.out"
        });
    });

});
