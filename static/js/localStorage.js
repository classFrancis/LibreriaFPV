
document.querySelector('.btn-outline-success.bi.bi-cart').addEventListener('click', function() {
    // Establecer un indicador en localStorage antes de la redirección
    localStorage.setItem('reopenModal', 'true');
});

document.addEventListener("DOMContentLoaded", function() {
    // Verificar si el indicador para reabrir el modal está establecido en localStorage
    if (localStorage.getItem('reopenModal') === 'true') {
        // Abre el modal
        var myModal = new bootstrap.Modal(document.getElementById('carrodecomprasmodal'));
        myModal.show();

        // Limpia el indicador
        localStorage.removeItem('reopenModal');
    }
});
