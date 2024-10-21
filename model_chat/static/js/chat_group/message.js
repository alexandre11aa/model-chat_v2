// message.js

// Função para lidar com mensagens recebidas via WebSocket no chat em grupo
export const handleIncomingMessage = (event) => {
    const data = JSON.parse(event.data);  // Parseia a mensagem recebida
    const message = data.message;  // Extrai a mensagem
    const sender = message.sender;  // Extrai o remetente
    const timestamp = new Date(message.timestamp);  // Converte o timestamp para um objeto Date
    const chatLog = document.getElementById('chat-log');  // Seleciona o elemento do log do chat

    const newMessage = document.createElement('div');  // Cria um novo elemento para a mensagem
    newMessage.innerHTML = `<strong>${sender}:</strong> ${message.message} <em>(${timestamp.getHours()}:${timestamp.getMinutes()})</em>`;
    chatLog.appendChild(newMessage);  // Adiciona a nova mensagem ao log do chat
    chatLog.scrollTop = chatLog.scrollHeight;  // Rolagem automática para mostrar a última mensagem
};