
document.querySelectorAll('a, form').forEach(element => {
    element.addEventListener('click', () => {
        localStorage.setItem('scrollPosition', window.scrollY);
    });
});
document.addEventListener("DOMContentLoaded", () => {
    const scrollPosition = localStorage.getItem('scrollPosition');
    if (scrollPosition) {
        window.scrollTo(0, parseInt(scrollPosition));
        localStorage.removeItem('scrollPosition'); // Limpia la posición guardada
    }
});


  