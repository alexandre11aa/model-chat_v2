// group_chat.js

import { createGroupChatSocket, handleSocketClose } from './socket.js';  // Importa funções do módulo socket.js
import { handleIncomingMessage } from './message.js';  // Importa a função do módulo message.js

// Acessa as variáveis de dados através de atributos 'data-*' no HTML
const chatData = document.getElementById('chat-data');  // Obtém o elemento que contém os dados do chat
const groupChatId = chatData.getAttribute('data-group-id');  // Obtém o ID do grupo de chat
const loggedUserId = chatData.getAttribute('data-logged-user-id');  // Obtém o ID do usuário logado

// Cria o WebSocket para o chat em grupo
const chatSocket = createGroupChatSocket(groupChatId);
chatSocket.onmessage = handleIncomingMessage;  // Define o manipulador de mensagens recebidas
chatSocket.onclose = handleSocketClose;  // Define o manipulador para quando o socket é fechado

// Configura o botão de enviar mensagem
document.getElementById('send-message').onclick = function(e) {
    const messageInputDom = document.getElementById('chat-message-input');  // Obtém o campo de entrada de mensagem
    const message = messageInputDom.value;  // Obtém o valor da mensagem

    chatSocket.send(JSON.stringify({
        'message': message,
        'sender_id': loggedUserId  // Envia o ID do usuário logado
    }));

    messageInputDom.value = '';  // Limpa o campo de entrada
};