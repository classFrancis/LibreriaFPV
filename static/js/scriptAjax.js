////////////////////aaaaarrrrreglarrrr


document.addEventListener("DOMContentLoaded", function() {
  document.querySelectorAll('.ajax-form').forEach(function(form) {
      form.addEventListener('submit', function(e) {
          e.preventDefault();

          fetch(form.action, {
              method: 'POST',
              body: new FormData(form),
              headers: {
                  'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value,
              },
          })
          .then(response => response.json())
          .then(data => {
              actualizarModal(data);
          })
          .catch(error => console.error('Error:', error));
      });
  });
});
function actualizarModal(data) {
  const listaLibros = document.getElementById('lista-libros-en-carro');
  listaLibros.innerHTML = '';

  data.libros.forEach(libro => {
      const elemento = document.createElement('li');
      elemento.textContent = `${libro.titulo} - Cantidad: ${libro.cantidad}`;
      listaLibros.appendChild(elemento);
  });

  const precioTotal = document.getElementById('precio-total');
  precioTotal.textContent = `Total: $${data.totalPrecio}`;
}
