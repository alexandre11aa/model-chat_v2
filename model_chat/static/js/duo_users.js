const userCode = document.body.getAttribute('data-user-code');
const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/notifications/' + userCode + '/'
);    
chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log("Dados recebidos:", data);
    
    // Altere de data.username para data.from_user
    const fromUser = data.from_user ? data.from_user.trim() : null;  // Adiciona verificação
    console.log("fromUser recebido:", fromUser);

    if (fromUser) {
        // Atualizar a contagem de mensagens não lidas
        const userElement = Array.from(document.querySelectorAll('.user-list li')).find(li => {
            return li.innerText.split(/\s*\d+\s*$/)[0].trim() === fromUser;
        });

        if (userElement) {
            let badge = userElement.querySelector('.badge');
            if (badge) {
                badge.textContent = parseInt(badge.textContent) + 1; // Somar 1
            } else {
                userElement.innerHTML += `<span class="badge badge-warning">1</span>`; // Definir como 1
            }
            console.log("Atualizando badge:", badge ? badge.textContent : '1');
        } else {
            console.log("Usuário não encontrado na lista:", fromUser);
        }
    } else {
        console.warn('from_user não definido na mensagem:', data);
    }
};