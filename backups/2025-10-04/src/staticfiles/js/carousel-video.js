document.addEventListener('DOMContentLoaded', function() {
    const carousel = document.getElementById('carouselEventosPrincipal');
    if (!carousel) return;

    // Función para intentar reproducir audio
    async function tryPlayAudio(video, toggleIcon) {
        try {
            video.muted = false;
            video.volume = 1.0;
            await video.play();
            toggleIcon.classList.remove('fa-volume-mute');
            toggleIcon.classList.add('fa-volume-up');
            console.log('Audio activado automáticamente');
        } catch (error) {
            console.log('No se pudo activar el audio automáticamente:', error);
            video.muted = true;
        }
    }

    // Intentar reproducir audio en la primera interacción del usuario con la página
    function setupAutoplay() {
        const firstInteractionHandler = async () => {
            const videos = document.querySelectorAll('.local-video');
            const activeVideo = document.querySelector('.carousel-item.active .local-video');
            const activeToggleIcon = document.querySelector('.carousel-item.active .toggle-audio i');
            
            if (activeVideo && activeToggleIcon) {
                await tryPlayAudio(activeVideo, activeToggleIcon);
            }
            
            // Remover los event listeners después de la primera interacción
            document.removeEventListener('click', firstInteractionHandler);
            document.removeEventListener('touchstart', firstInteractionHandler);
            document.removeEventListener('keydown', firstInteractionHandler);
        };

        document.addEventListener('click', firstInteractionHandler);
        document.addEventListener('touchstart', firstInteractionHandler);
        document.addEventListener('keydown', firstInteractionHandler);
    }

    function handleLocalVideos() {
        document.querySelectorAll('.local-video').forEach(video => {
            const container = video.closest('.carousel-video-container');
            const toggleButton = container.querySelector('.toggle-audio');
            const toggleIcon = toggleButton.querySelector('i');

            // Registrar eventos de error y estado
            video.addEventListener('error', (e) => {
                console.error('Error en el video:', {
                    error: e.target.error,
                    src: video.currentSrc,
                    networkState: video.networkState,
                    readyState: video.readyState
                });
            });

            // Asegurarse de que el video esté listo para reproducirse
            video.load();
            
            // Configurar reproducción automática (inicialmente silenciado)
            video.muted = true;
            video.loop = true;
            video.playsInline = true;
            video.volume = 1.0; // Asegurarse que el volumen esté al máximo

            // Manejar el botón de audio
            toggleButton.addEventListener('click', async (e) => {
                e.preventDefault();
                e.stopPropagation();
                
                try {
                    if (video.muted) {
                        await tryPlayAudio(video, toggleIcon);
                    } else {
                        // Silenciar el video
                        video.muted = true;
                        toggleIcon.classList.remove('fa-volume-up');
                        toggleIcon.classList.add('fa-volume-mute');
                        console.log('Audio desactivado');
                    }
                } catch (error) {
                    console.error('Error al manejar el audio:', error);
                    // Si hay un error, volver a silenciar el video
                    video.muted = true;
                    toggleIcon.classList.remove('fa-volume-up');
                    toggleIcon.classList.add('fa-volume-mute');
                }
            });

            // Asegurarse que el video se silencia al cambiar de slide
            carousel.addEventListener('slide.bs.carousel', () => {
                video.muted = true;
                toggleIcon.classList.remove('fa-volume-up');
                toggleIcon.classList.add('fa-volume-mute');
            });
            
            // Intentar reproducir el video
            const playPromise = video.play();
            if (playPromise !== undefined) {
                playPromise.catch(error => {
                    console.error('Error reproduciendo video:', {
                        error: error,
                        src: video.currentSrc,
                        readyState: video.readyState
                    });
                });
            }

            // Monitorear el estado del video
            video.addEventListener('volumechange', () => {
                console.log('Cambio de volumen:', {
                    muted: video.muted,
                    volume: video.volume,
                    playing: !video.paused
                });
            });
        });
    }

    function pauseAllVideos() {
        // Pausar videos locales
        document.querySelectorAll('.local-video').forEach(video => {
            try {
                video.pause();
            } catch (e) {
                console.error('Error al pausar video local:', e);
            }
        });

        // Pausar videos de YouTube
        document.querySelectorAll('.youtube-player').forEach(iframe => {
            try {
                iframe.contentWindow.postMessage('{"event":"command","func":"pauseVideo","args":""}', '*');
            } catch (e) {
                console.error('Error al pausar video de YouTube:', e);
            }
        });
    }

    // Reproducir el video del slide activo
    function playActiveSlideVideo() {
        const activeSlide = carousel.querySelector('.carousel-item.active');
        if (!activeSlide) return;

        const video = activeSlide.querySelector('.local-video');
        if (video) {
            const playPromise = video.play();
            if (playPromise !== undefined) {
                playPromise.catch(error => {
                    console.log("Error reproduciendo video:", error);
                });
            }
        }
    }

    // Manejar cambios de slide
    carousel.addEventListener('slide.bs.carousel', pauseAllVideos);
    carousel.addEventListener('slid.bs.carousel', playActiveSlideVideo);

            // Inicializar videos al cargar
            handleLocalVideos();
            setupAutoplay();
        });