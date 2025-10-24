document.addEventListener('DOMContentLoaded', function() {
    const textElement = document.getElementById('typewriter-text');
    if (!textElement) return;

    const phrases = [
        "Bem-vindo à JCC CONSTRUÇÕES, E.I.",
        "Construindo o Futuro, bloco a bloco.",
        "Sua Visão, Nossa Realidade."
    ];

    let phraseIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    let typingSpeed = 100; // ms por caractere
    let deletingSpeed = 50; // ms por caractere ao apagar
    let pauseTime = 1500; // Tempo de pausa no final da frase

    function typeWriter() {
        const currentPhrase = phrases[phraseIndex];

        if (isDeleting) {
            // Apagando
            textElement.textContent = currentPhrase.substring(0, charIndex - 1);
            charIndex--;
            typingSpeed = deletingSpeed;
        } else {
            // Escrevendo
            textElement.textContent = currentPhrase.substring(0, charIndex + 1);
            charIndex++;
            typingSpeed = 100; // Velocidade normal
        }

        if (!isDeleting && charIndex === currentPhrase.length) {
            // Terminou de escrever, pausa e começa a apagar
            typingSpeed = pauseTime;
            isDeleting = true;
        } else if (isDeleting && charIndex === 0) {
            // Terminou de apagar, muda para a próxima frase
            isDeleting = false;
            phraseIndex = (phraseIndex + 1) % phrases.length;
            typingSpeed = 200; // Pequena pausa antes de começar a escrever a próxima
        }

        setTimeout(typeWriter, typingSpeed);
    }

    typeWriter(); // Inicia o efeito
});