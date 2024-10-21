// socket.js

// Função para criar um novo WebSocket para o chat
export const chatSocket = (loggedUserCode, targetUserCode) => {
    const socket = new WebSocket(
        'ws://' + window.location.host + '/ws/chat/' + loggedUserCode + '/' + targetUserCode + '/'
    );

    return socket;  // Retorna o objeto WebSocket
};

// Função para lidar com o fechamento inesperado do socket
export const handleSocketClose = (event) => {
    console.error('Chat socket closed unexpectedly');  // Loga um erro no console
};