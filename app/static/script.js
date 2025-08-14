document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('videoForm');
  const categoriasSelect = document.getElementById('categorias');
  const nuevaCategoriaInput = document.getElementById('nuevaCategoria');
  const videosList = document.getElementById('videosList');
  const filtroCategoria = document.getElementById('filtroCategoria');
  const formContainer = document.getElementById('formContainer');
  const toggleFormBtn = document.getElementById('toggleFormBtn');
  let categorias = [];
  let videos = [];
  let formVisible = true;

  function cargarCategorias() {
    fetch('/categorias').then(r => r.json()).then(data => {
      categorias = data;
      categoriasSelect.innerHTML = '';
      filtroCategoria.innerHTML = '<option value="">Todas</option>';
      categorias.forEach(cat => {
        const opt = document.createElement('option');
        opt.value = cat;
        opt.textContent = cat;
        categoriasSelect.appendChild(opt);
        const filtroOpt = document.createElement('option');
        filtroOpt.value = cat;
        filtroOpt.textContent = cat;
        filtroCategoria.appendChild(filtroOpt);
      });
    });
  }

  function cargarVideos() {
    fetch('/videos').then(r => r.json()).then(data => {
      videos = data;
      mostrarVideos();
    });
  }

  function mostrarVideos() {
    const filtro = filtroCategoria.value;
    videosList.innerHTML = '';
    videos.filter(v => !filtro || v.categorias.split(',').includes(filtro)).forEach(video => {
      const col = document.createElement('div');
      col.className = 'col-md-6 col-lg-4';
      col.innerHTML = `
        <div class="card h-100">
          <img src="${video.miniatura_url}" class="card-img-top" alt="Miniatura">
          <div class="card-body">
            <div class="mb-2">
              ${video.categorias.split(',').map(cat => `<span class="badge bg-info me-1">${cat}</span>`).join('')}
            </div>
            <h5 class="card-title">${video.titulo.length > 60 ? video.titulo.slice(0, 60) + '...' : video.titulo}</h5>
            <p class="card-text">${video.descripcion && video.descripcion.length > 300 ? video.descripcion.slice(0, 300) + '...' : (video.descripcion || '')}</p>
            <a href="${video.url}" target="_blank" class="btn btn-sm btn-outline-primary mb-2">Ver video</a>
            <button class="btn btn-sm btn-warning" onclick="editarVideo(${video.id})">Editar</button>
            <div id="editForm${video.id}" style="display:none;" class="mt-2">
              <input type="text" class="form-control mb-1" id="editTitulo${video.id}" value="${video.titulo}">
              <input type="text" class="form-control mb-1" id="editDescripcion${video.id}" value="${video.descripcion}">
              <select multiple class="form-select mb-1" id="editCategorias${video.id}">
                ${categorias.map(cat => `<option value="${cat}" ${video.categorias.split(',').includes(cat) ? 'selected' : ''}>${cat}</option>`).join('')}
              </select>
              <button class="btn btn-sm btn-success" onclick="guardarEdicion(${video.id})">Guardar cambios</button>
            </div>
          </div>
        </div>
      `;
      videosList.appendChild(col);
    });
  }

  form.addEventListener('submit', e => {
    e.preventDefault();
    const url = document.getElementById('url').value;
    const categoriasSeleccionadas = Array.from(categoriasSelect.selectedOptions).map(opt => opt.value);
    const nuevaCategoria = nuevaCategoriaInput.value.trim();
    fetch('/agregar_video', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ url, categorias: categoriasSeleccionadas, nueva_categoria: nuevaCategoria })
    })
    .then(r => {
      if (!r.ok) return r.json().then(err => Promise.reject(err));
      return r.json();
    })
    .then(() => {
      form.reset();
      cargarCategorias();
      cargarVideos();
    })
    .catch(err => alert(err.detail || 'Error al guardar'));
  });

  filtroCategoria.addEventListener('change', mostrarVideos);

  toggleFormBtn.addEventListener('click', () => {
    formVisible = !formVisible;
    formContainer.style.display = formVisible ? 'block' : 'none';
    toggleFormBtn.textContent = formVisible ? 'Ocultar formulario' : 'Mostrar formulario';
  });

  window.editarVideo = function(id) {
    document.getElementById('editForm'+id).style.display = 'block';
  };

  window.guardarEdicion = function(id) {
    const titulo = document.getElementById('editTitulo'+id).value;
    const descripcion = document.getElementById('editDescripcion'+id).value;
    const categoriasSeleccionadas = Array.from(document.getElementById('editCategorias'+id).selectedOptions).map(opt => opt.value);
    fetch(`/editar_video/${id}`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ titulo, descripcion, categorias: categoriasSeleccionadas })
    })
    .then(r => {
      if (!r.ok) return r.json().then(err => Promise.reject(err));
      return r.json();
    })
    .then(() => {
      cargarVideos();
    })
    .catch(err => alert(err.detail || 'Error al editar'));
  };

  cargarCategorias();
  cargarVideos();
});
