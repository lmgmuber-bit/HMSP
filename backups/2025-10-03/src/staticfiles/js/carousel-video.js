// Función para pausar todos los videos en el carrusel
function pauseAllVideos() {
    // Pausar videos de YouTube
    document.querySelectorAll('.youtube-player').forEach(iframe => {
        try {
            iframe.contentWindow.postMessage('{"event":"command","func":"pauseVideo","args":""}', '*');
        } catch (e) {
            console.error('Error al pausar video de YouTube:', e);
        }
    });

    // Pausar videos locales
    document.querySelectorAll('.local-video').forEach(video => {
        try {
            video.pause();
        } catch (e) {
            console.error('Error al pausar video local:', e);
        }
    });
}

// Agregar event listeners cuando el documento esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Obtener el carrusel
    const carousel = document.getElementById('carouselEventosPrincipal');
    if (!carousel) return;

    // Pausar videos cuando el carrusel cambia de slide
    carousel.addEventListener('slide.bs.carousel', function() {
        pauseAllVideos();
    });

    // Asegurarse de que los videos estén pausados al cargar la página
    pauseAllVideos();
});