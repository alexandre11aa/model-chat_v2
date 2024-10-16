// Função para abrir o seletor de emoticons
function toggleEmojiPicker() {
    const emojiPicker = document.getElementById('emoji-picker');
    emojiPicker.classList.toggle('d-none'); // Alterna a visibilidade do seletor
}

// Função para inserir o emoticon no campo de entrada
function insertEmoji(emoji) {
    const messageInput = document.getElementById('chat-message-input');
    messageInput.value += emoji; // Adiciona o emoticon ao campo de entrada
}

// Adiciona eventos ao botão de emoticons
document.getElementById('emoji-button').onclick = toggleEmojiPicker;

// Adiciona eventos para cada emoticon
document.querySelectorAll('.emoji').forEach(emoji => {
    emoji.onclick = function () {
        insertEmoji(this.innerHTML);
        toggleEmojiPicker(); // Fecha o seletor após selecionar
    };
});