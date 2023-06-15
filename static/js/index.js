// Header

const header = document.getElementById('header');
const btnContainer = document.getElementById('btnContainer');
const traces = document.querySelectorAll('.trace');

const animationTime = 300
const traceNum = 5

let hoverTimeout;
let fadeIns = [];
let fadeOuts = [];

btnContainer.addEventListener('mouseenter', e => {
    hoverTimeout = setTimeout(() => {
        traces.forEach((trace, index) => {
            fadeIns[index] = setTimeout(() => {
                trace.style.opacity = 1;
            }, index * animationTime/traceNum);
        });
    }, 50);
})

function fadeOutTraces() {
    fadeIns.forEach(clearTimeout); // Clear any ongoing fadeIn timeouts
    fadeIns = []; // Reset the fadeIn timeouts array

    traces.forEach((trace, index) => {
        fadeOuts[index] = setTimeout(() => {
            trace.style.opacity = 0;
        }, (traces.length - 1 - index) * animationTime/traceNum);
    });
}

btnContainer.addEventListener('mouseleave', e => {
    clearTimeout(hoverTimeout);
    fadeOuts.forEach(clearTimeout); // Clear any ongoing fadeOut timeouts
    fadeOuts = []; // Reset the fadeOut timeouts array
    fadeOutTraces();
})

btnContainer.addEventListener('mouseout', e => {
    if (!btnContainer.contains(e.relatedTarget)) {
        fadeOutTraces();
    }
})

btnContainer.addEventListener('mousedown', e => {
    traces.forEach((trace) => {
        trace.style.opacity = 0;
    })

})



// Main

const QACards = document.querySelectorAll('.QA-card')

QACards.forEach((card) => {
    card.addEventListener('click', e => {
        e.stopPropagation()

        const currentHeight = window.getComputedStyle(card).height
        const fullHeight = `${card.scrollHeight}px`


        QACards.forEach((otherCards) => {
            otherCards.style.height = '60px'
            otherCards.style.backgroundColor = '#FFFBFF'
        })

        if (currentHeight != '60px') {
            card.style.height = '60px'
            card.style.backgroundColor = '#FFFBFF'
        } else {
            card.style.height = fullHeight
            card.style.backgroundColor = '#e8ebf78c'
        }
    })
})

document.addEventListener('click', e => {
    QACards.forEach((card) => {
        card.style.height = '60px'
        card.style.backgroundColor = '#FFFBFF'
    })
})

