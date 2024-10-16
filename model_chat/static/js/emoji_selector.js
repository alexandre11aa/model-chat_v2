const emojiButton = document.getElementById('send-emoji');
const emojiContainer = document.getElementById('emoji-container');
const chatMessageInput = document.getElementById('chat-message-input');

// Mostra ou esconde o contêiner de emojis ao clicar no botão
emojiButton.onclick = function(event) {
    event.stopPropagation(); // Evita que o evento clique se propague
    const rect = emojiButton.getBoundingClientRect(); // Obtém a posição do botão
    emojiContainer.style.top = (rect.top + window.scrollY - emojiContainer.offsetHeight) + 'px'; // Posiciona acima do botão
    emojiContainer.style.left = (rect.left + window.scrollX) + 'px'; // Alinha ao botão
    emojiContainer.style.display = (emojiContainer.style.display === 'block') ? 'none' : 'block'; // Alterna a visibilidade
};

// Adiciona o emoji ao campo de mensagem ao clicar no emoji
document.querySelectorAll('.emoji').forEach(function(emoji) {
    emoji.onclick = function() {
        chatMessageInput.value += emoji.getAttribute('data-emoji'); // Adiciona o emoji à mensagem
        emojiContainer.style.display = 'none'; // Esconde o contêiner de emojis após a seleção
        chatMessageInput.focus(); // Foca no campo de mensagem
    };
});

// Fecha o contêiner de emojis ao clicar fora
document.addEventListener('click', function() {
    emojiContainer.style.display = 'none';
});