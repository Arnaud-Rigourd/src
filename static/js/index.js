// Header

hoverEffect('btnContainer');
hoverEffect('profileContainer');

/**
 * Set the opacity of a trace element after a delay
 * @param {HTMLElement} trace - The trace element to set the opacity of
 * @param {number} opacity - The opacity to set
 * @param {number} delay - The delay before setting the opacity, in milliseconds
 * @return {number} The ID of the timeout that was started
 */
function setTraceOpacity(trace, opacity, delay) {
    return setTimeout(() => {
        trace.style.opacity = opacity;
    }, delay);
}

/**
 * Clear a list of timeouts and return an empty array
 * @param {number[]} timeouts - The list of timeout IDs to clear
 * @return {number[]} An empty array
 */
function clearAndResetTimeouts(timeouts) {
    timeouts.forEach(clearTimeout);
    return [];
}

/**
 * Add a hover effect to all elements with a given class name.
 * The effect will fade in/out all children with the 'trace' class.
 * @param {string} containerClassName - The class name of the containers to apply the hover effect to
 */
function hoverEffect(containerClassName) {
    const animationTime = 300;

    const containers = document.querySelectorAll(`.${containerClassName}`);

    containers.forEach((container) => {
        // Variables to store the IDs of timeouts
        let hoverTimeout;
        let fadeIns = [];
        let fadeOuts = [];

        // Select all traces within the current container
        const traces = Array.from(container.querySelectorAll('.trace'));
        const traceNum = traces.length;

        // Add a hover effect to each trace
        container.addEventListener('mouseenter', () => {
            hoverTimeout = setTimeout(() => {
                fadeIns = traces.map((trace, index) =>
                    setTraceOpacity(trace, 1, index * animationTime / traceNum)
                );
            }, 50);
        });

        // Add a hover out effect to each trace
        container.addEventListener('mouseleave', () => {
            clearTimeout(hoverTimeout);
            fadeIns = clearAndResetTimeouts(fadeIns);
            fadeOuts = traces.map((trace, index) =>
                setTraceOpacity(trace, 0, (traceNum - 1 - index) * animationTime / traceNum)
            );
        });

        // Add a mouse out effect to each trace in case the mouseleave is not detected
        container.addEventListener('mouseout', (e) => {
            if (!container.contains(e.relatedTarget)) {
                fadeIns = clearAndResetTimeouts(fadeIns);
                fadeOuts = traces.map((trace, index) =>
                    setTraceOpacity(trace, 0, (traceNum - 1 - index) * animationTime / traceNum)
                );
            }
        });

        // Add a mousedown effect to each trace
        container.addEventListener('mousedown', () => {
            fadeIns = clearAndResetTimeouts(fadeIns);
            fadeOuts = clearAndResetTimeouts(fadeOuts);
            traces.forEach(trace => trace.style.opacity = 0);
        });
    });
}




// Main

const QACards = document.querySelectorAll('.QA-card')

QACards.forEach((card) => {
    card.addEventListener('click', e => {
        e.stopPropagation()

        const currentHeight = window.getComputedStyle(card).height
        const fullHeight = `${card.scrollHeight}px`


        QACards.forEach((otherCards) => {
            otherCards.style.height = '60px'
        })

        if (currentHeight != '60px') {
            card.style.height = '60px'
        } else {
            card.style.height = fullHeight
            card.style.backgroundColor = '#e8ebf78c'
        }
    })
})

document.addEventListener('click', e => {
    QACards.forEach((card) => {
        card.style.height = '60px'
    })
})



// Navbar

const navbar = document.getElementById('navbar')
const wrapper = document.getElementById('wrapper')

if (wrapper != null) {
    wrapper.addEventListener("scroll", e => {
        if (wrapper.scrollTop >= (window.innerHeight - 72)) {
          navbar.classList.add("nav-bg")
        } else {
          navbar.classList.remove("nav-bg")
        }
    })
} else {
    navbar.classList.add("nav-bg")
}

