document.addEventListener('DOMContentLoaded', function () {
    const botonFiltros = document.getElementById('toggle-filtros');
    const panelFiltros = document.getElementById('panel-filtros');
  
    if (botonFiltros && panelFiltros) {
      botonFiltros.addEventListener('click', () => {
        panelFiltros.classList.toggle('visible');
      });
    }
  });
  


//Lightbox -----------------------------------------
function abrirLightbox(url, titulo, fecha, codigo, autor , personas , lugar_orig , tema , coleccion , creado_en) {
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-imagen');
    const lightboxTitulo = document.getElementById('lightbox-titulo');
    const lightboxFecha = document.getElementById('lightbox-fecha');
    const lightboxCodigo= document.getElementById('lightbox-codigo');
    const lightboxAutor = document.getElementById('lightbox-autor');
    const lightboxPersonas = document.getElementById('lightbox-personas');
    const lightboxLugar = document.getElementById('lightbox-lugar_orig');
    const lightboxTema = document.getElementById('lightbox-tema');
    const lightboxColeccion = document.getElementById('lightbox-coleccion');
    const lightboxCreado = document.getElementById('lightbox-creado_en'); 


    lightbox.style.display = 'flex';
    lightboxImg.src = url;
    lightboxTitulo.textContent = titulo;
    lightboxCodigo.textContent='codigo: ' + codigo;
    lightboxFecha.textContent ='año: ' + fecha;
    lightboxAutor.textContent='Autor: ' + autor;
    lightboxPersonas.textContent = 'Personas en la foto: ' + personas;
    lightboxLugar.textContent = 'Tomada en: ' + lugar_orig;
    lightboxTema.textContent = 'Tematica: ' + tema;
    lightboxColeccion.textContent = 'Colección: ' + coleccion;
    lightboxCreado.textContent = 'Creado en: ' + creado_en;
}

function cerrarLightbox() {
    document.getElementById('lightbox').style.display = 'none';
}

// Cerrar al presionar ESC
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') cerrarLightbox();
});