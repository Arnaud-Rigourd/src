// console.log("Hello from index.js")
//
// const btn = document.getElementById('headerBtn')
//
// btn.addEventListener('mouseover', function(event) {
//   const btn = event.target;
//   const btnContainer = document.getElementById('btnContainer')
//
//   for(let i = 0; i < 4; i++) {
//     const trace = document.createElement('div');
//     trace.className = 'trace';
//     trace.style.top = (btn.offsetTop - i) + 'px';
//     trace.style.left = (btn.offsetLeft - i) + 'px';
//     btnContainer.appendChild(trace);
//   }
//
//   function step(timestamp) {
//       if (!start) start = timestamp;
//       var progress = timestamp - start;
//
//       // Calcule la nouvelle position de la div
//       var newTop = initialTop - (4 * progress / duration);
//       var newLeft = initialLeft - (4 * progress / duration);
//
//       // Applique la nouvelle position
//       box.style.top = newTop + 'px';
//       box.style.left = newLeft + 'px';
//
//       if (progress < duration) {
//           // Si l'animation n'est pas encore terminée, demande le prochain frame
//           window.requestAnimationFrame(step);
//       }
//   }
// });
//
// document.getElementById('headerBtn').addEventListener('mouseleave', function(event) {
//   var traces = document.getElementsByClassName('trace');
//
//   // Parcours et suppression de tous les éléments avec la classe 'trace'
//   while (traces[0]) {
//     traces[0].parentNode.removeChild(traces[0]);
//   }
// });

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