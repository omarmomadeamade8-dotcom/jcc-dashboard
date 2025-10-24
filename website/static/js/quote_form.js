document.addEventListener('DOMContentLoaded', function() {
    const formSection = document.getElementById('quote-form-section');
    const quoteButtons = document.querySelectorAll('.show-quote-form-btn');
    const serviceSelectField = document.getElementById('servico'); 

    // 1. VERIFICAÇÃO E REFORÇO DA INVISIBILIDADE INICIAL
    // Se o formulário for encontrado, garanta que ele está oculto.
    if (formSection) {
        formSection.style.display = 'none';
        console.log("DEBUG: Formulário de Orçamento definido como 'display: none' pelo JS.");
    }

    // Se não houver formulário ou botões para pedir orçamento, sai.
    if (!formSection || quoteButtons.length === 0) {
        console.log("DEBUG: Componentes cruciais do formulário não encontrados.");
        return;
    }

    // Adicionar um 'event listener' a todos os botões "Pedir Orçamento"
    quoteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault(); // <-- CRUCIAL: Impede o salto padrão do link
            
            console.log("DEBUG: Botão 'Pedir Orçamento' clicado. Tentando mostrar o formulário.");
            
            // a) Mostrar a secção do formulário (display: block)
            formSection.style.display = 'block';

            // b) Obter o nome do serviço
            const serviceName = this.getAttribute('data-service');
            console.log("Serviço selecionado: " + serviceName);

            // c) Preencher o campo <select> com o serviço clicado
            if (serviceSelectField) {
                let found = false;
                for (let i = 0; i < serviceSelectField.options.length; i++) {
                    // Verifica se o valor (value) ou o texto (text) da opção corresponde
                    if (serviceSelectField.options[i].value === serviceName || serviceSelectField.options[i].text === serviceName) {
                        serviceSelectField.value = serviceSelectField.options[i].value;
                        found = true;
                        break;
                    }
                }
                if (!found) {
                     // Tenta selecionar a opção 'Outro' ou o primeiro elemento (o default "Escolha uma opção" está disabled)
                     // Se não encontrar, tenta forçar o valor 'Outro'
                     serviceSelectField.value = 'Outro'; 
                     console.log("Não encontrado no select, definindo como 'Outro'.");
                }
            }

            // d) Fazer o scroll suave até ao formulário
            formSection.scrollIntoView({ behavior: 'smooth' });
        });
    });
});