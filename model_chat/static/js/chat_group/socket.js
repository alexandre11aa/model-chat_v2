// socket.js

// Função para criar um novo WebSocket para o chat em grupo
export const createGroupChatSocket = (groupChatId) => {
    const socket = new WebSocket(
        'ws://' + window.location.host + '/ws/chat/group/' + groupChatId + '/'
    );

    return socket;  // Retorna o objeto WebSocket
};

// Função para lidar com o fechamento inesperado do socket
export const handleSocketClose = (event) => {
    console.error('Group chat socket closed unexpectedly');  // Loga um erro no console
};