// fileUpload.js

// Função para obter o valor de um cookie pelo nome
export const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');  // Divide os cookies em um array
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));  // Decodifica o valor do cookie
                break;
            }
        }
    }
    return cookieValue;  // Retorna o valor do cookie
};

// Função para fazer upload de um arquivo
export const uploadFile = (file, csrftoken, loggedUserCode, chatSocket) => {
    const formData = new FormData();  // Cria um objeto FormData para enviar o arquivo
    formData.append('file', file);  // Anexa o arquivo ao FormData
    formData.append('filename', file.name);  // Anexa o nome do arquivo

    const xhr = new XMLHttpRequest();  // Cria um novo objeto XMLHttpRequest
    xhr.open('POST', '/upload-file/');  // Define o método e a URL do upload
    xhr.setRequestHeader('X-CSRFToken', csrftoken);  // Define o cabeçalho CSRF

    xhr.onload = function() {
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);  // Parseia a resposta do servidor
            const fileUrl = `/uploads/${response.filename}`;  // Cria a URL do arquivo

            // Envia o arquivo via WebSocket para o chat
            chatSocket.send(JSON.stringify({
                'file': fileUrl,
                'filename': response.filename,
                'username': loggedUserCode,
                'time': new Date().toLocaleTimeString()
            }));
        } else {
            console.error('Erro ao enviar o arquivo.');  // Loga um erro se a requisição falhar
        }
    };

    xhr.send(formData);  // Envia o FormData com o arquivo
};