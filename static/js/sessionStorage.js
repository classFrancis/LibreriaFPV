// Parte 1: Guardar la Posición de Desplazamiento
// Selecciona todos los enlaces y formularios en la página
document.querySelectorAll('a, form').forEach(element => {
    // Añade un controlador de eventos de clic a cada elemento seleccionado
    element.addEventListener('click', () => {
        // Al hacer clic, guarda la posición actual de desplazamiento vertical en localStorage
        // 'scrollPosition' es la clave donde se almacena la posición
        // window.scrollY es la posición actual de desplazamiento en píxeles desde la parte superior
        localStorage.setItem('scrollPosition', window.scrollY);
    });
});

// Parte 2: Restaurar la Posición de Desplazamiento
// Este evento se dispara cuando se completa la carga del contenido del DOM
document.addEventListener("DOMContentLoaded", () => {
    // Obtiene la posición de desplazamiento guardada desde localStorage
    const scrollPosition = localStorage.getItem('scrollPosition');
    // Si existe una posición guardada, es decir, no es nula
    if (scrollPosition) {
        // Desplaza la ventana a la posición guardada
        // parseInt convierte el valor de string a número
        window.scrollTo(0, parseInt(scrollPosition));
        // Limpia el valor guardado en localStorage para evitar interferencias futuras
        localStorage.removeItem('scrollPosition'); 
    }
});
  