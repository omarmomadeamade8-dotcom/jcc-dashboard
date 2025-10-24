document.addEventListener('DOMContentLoaded', function() {
    const galleryItems = document.querySelectorAll('.gallery-item img');
    const body = document.body;

    // Criar o overlay e o container para a imagem grande
    const lightboxOverlay = document.createElement('div');
    lightboxOverlay.id = 'lightbox-overlay';
    lightboxOverlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.8);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
        opacity: 0;
        visibility: hidden;
        transition: opacity 0.3s ease-in-out;
    `;

    const lightboxImage = document.createElement('img');
    lightboxImage.style.cssText = `
        max-width: 90%;
        max-height: 90%;
        object-fit: contain;
        border: 2px solid white;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
        transform: scale(0.8);
        transition: transform 0.3s ease-in-out;
    `;

    lightboxOverlay.appendChild(lightboxImage);
    body.appendChild(lightboxOverlay);

    galleryItems.forEach(item => {
        item.style.cursor = 'zoom-in'; // Indicar que é clicável
        item.addEventListener('click', function() {
            lightboxImage.src = this.src; // Define a imagem clicada
            lightboxOverlay.style.opacity = '1';
            lightboxOverlay.style.visibility = 'visible';
            lightboxImage.style.transform = 'scale(1)'; // Animação de entrada
        });
    });

    // Fechar o lightbox ao clicar no overlay
    lightboxOverlay.addEventListener('click', function() {
        this.style.opacity = '0';
        this.style.visibility = 'hidden';
        lightboxImage.style.transform = 'scale(0.8)'; // Animação de saída
    });
});