// Algoritmo completo da pasta "chat", configurado em um único arquivo (SEM A FUNÇÃO DE MANDAR AUDIO)

const loggedUserCode = document.body.getAttribute('data-user-code');
const targetUserCode = document.body.getAttribute('data-target-user-code');

const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/' + loggedUserCode + '/' + targetUserCode + '/'
);

chatSocket.onmessage = handleIncomingMessage;
chatSocket.onclose = handleSocketClose;

// Envia mensagens ao pressionar Enter
document.getElementById('chat-message-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        sendMessage();
    }
});

document.getElementById('send-message').onclick = sendMessage;

// Botão de anexo de arquivo
document.getElementById('send-file').onclick = function () {
    document.getElementById('chat-file-input').click();  // Simula clique no input de arquivo
};

// Função para obter o token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken'); // Obtém o token CSRF

// Quando o arquivo é selecionado, faz upload pelo WebSocket
document.getElementById('chat-file-input').onchange = function(event) {
    const file = event.target.files[0];

    if (file) {
        const formData = new FormData();
        formData.append('file', file);  // Anexa o arquivo
        formData.append('filename', file.name);  // Usa file.name para obter o nome do arquivo
    
        // Enviar o arquivo para o backend (upload)
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/upload-file/');
        xhr.setRequestHeader('X-CSRFToken', csrftoken);
    
        xhr.onload = function() {
            if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                const fileUrl = `/uploads/${response.filename}`;  // Supondo que o arquivo seja salvo na pasta 'uploads'
    
                // Enviar o arquivo via WebSocket para o chat
                chatSocket.send(JSON.stringify({
                    'file': fileUrl,
                    'filename': response.filename,
                    'username': loggedUserCode,
                    'time': new Date().toLocaleTimeString()
                }));
            } else {
                console.error('Erro ao enviar o arquivo.');
            }
        };
    
        xhr.send(formData);  // Envia o FormData
    }
};

function sendMessage() {
    const messageInputDom = document.getElementById('chat-message-input');
    const message = messageInputDom.value.trim();

    if (message === '') {
        return;  // Não envia mensagens vazias
    }

    chatSocket.send(JSON.stringify({
        'message': message,
        'username': loggedUserCode,
        'time': new Date().toLocaleTimeString()
    }));

    messageInputDom.value = '';  // Limpa o campo de entrada
}

// Função de envio de mensagens assíncrono para o chat    
function handleIncomingMessage(event) {
    const data = JSON.parse(event.data);
    const chatLog = document.getElementById('chat-log');

    const newMessage = document.createElement('div');
    const timeDisplay = data.time ? ` (${data.time})` : '';

    if (data.file) {
        const fileExtension = data.filename.split('.').pop().toLowerCase(); // Obtemos a extensão do arquivo
        if (['jpg', 'jpeg', 'png', 'gif'].includes(fileExtension)) {
            // Se for uma imagem, criamos o HTML para exibir a imagem
            newMessage.innerHTML = `
                <strong>${data.username}:</strong>
                <div>
                    <img src="${data.file}" alt="${data.filename}" style="max-width: 200px; max-height: 200px;"><br>
                    <a href="${data.file}" download="${data.filename}">${data.filename}</a>${timeDisplay}
                </div>
            `;
        } else {
            // Para outros tipos de arquivos, apenas um link
            newMessage.innerHTML = `
                <strong>${data.username}:</strong>
                <a href="${data.file}" download="${data.filename}">${data.filename}</a>${timeDisplay}
            `;
        }
    } else {
        newMessage.innerHTML = `<strong>${data.username}:</strong> ${data.message}${timeDisplay}`;
    }

    chatLog.appendChild(newMessage);
    chatLog.scrollTop = chatLog.scrollHeight;  // Rolagem automática
}

function handleSocketClose(event) {
    console.error('Chat socket closed unexpectedly');
}