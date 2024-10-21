// duo_chat.js

import { chatSocket, handleSocketClose } from './socket.js';  // Importa as funções do módulo socket.js
import { handleIncomingMessage } from './message.js';  // Importa a função do módulo message.js
import { getCookie, uploadFile } from './fileUpload.js';  // Importa funções do módulo fileUpload.js
import { startRecording, stopRecording, handleMouseLeave } from './audioRecorder.js';  // Importa as funções do módulo audioRecorder.js

const loggedUserCode = document.body.getAttribute('data-user-code');  // Obtém o código do usuário logado
const targetUserCode = document.body.getAttribute('data-target-user-code');  // Obtém o código do usuário alvo

// Cria o WebSocket para o chat
const socket = chatSocket(loggedUserCode, targetUserCode);
socket.onmessage = (event) => handleIncomingMessage(event, loggedUserCode);  // Define o manipulador de mensagens recebidas
socket.onclose = handleSocketClose;  // Define o manipulador para quando o socket é fechado

// Envia mensagens ao pressionar Enter
document.getElementById('chat-message-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        e.preventDefault();  // Previne o comportamento padrão
        sendMessage();  // Chama a função de enviar mensagem
    }
});

// Configura o botão de enviar mensagem
document.getElementById('send-message').onclick = sendMessage;

// Configura o botão de anexo de arquivo
document.getElementById('send-file').onclick = function () {
    document.getElementById('chat-file-input').click();  // Simula um clique no input de arquivo
};

// Obtém o token CSRF
const csrftoken = getCookie('csrftoken');

// Quando o arquivo é selecionado, faz upload pelo WebSocket
document.getElementById('chat-file-input').onchange = function(event) {
    const file = event.target.files[0];  // Obtém o arquivo selecionado
    if (file) {
        uploadFile(file, csrftoken, loggedUserCode, socket);  // Faz o upload do arquivo
    }
};

// Função para enviar mensagens
function sendMessage() {
    const messageInputDom = document.getElementById('chat-message-input');  // Obtém o campo de entrada de mensagem
    const message = messageInputDom.value.trim();  // Remove espaços em branco

    if (message === '') {
        return;  // Não envia mensagens vazias
    }

    socket.send(JSON.stringify({
        'message': message,
        'username': loggedUserCode,
        'time': new Date().toLocaleTimeString()
    }));

    messageInputDom.value = '';  // Limpa o campo de entrada
}

// Configuração do botão de gravação de áudio
const sendAudioButton = document.getElementById('send-audio');
sendAudioButton.addEventListener('mousedown', () => startRecording(sendAudioButton, socket, loggedUserCode));
sendAudioButton.addEventListener('mouseup', () => stopRecording(sendAudioButton, socket, loggedUserCode));
sendAudioButton.addEventListener('mouseleave', () => handleMouseLeave(sendAudioButton));