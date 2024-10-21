// message.js

// Função para lidar com mensagens recebidas via WebSocket
export const handleIncomingMessage = (event, loggedUserCode) => {
    const data = JSON.parse(event.data);  // Parseia a mensagem recebida
    const chatLog = document.getElementById('chat-log');  // Seleciona o elemento do log do chat

    const newMessage = document.createElement('div');  // Cria um novo elemento para a mensagem
    const timeDisplay = data.time ? ` (${data.time})` : '';  // Formata a hora da mensagem

    if (data.file) {  // Se a mensagem contém um arquivo
        const fileExtension = data.filename.split('.').pop().toLowerCase();  // Obtém a extensão do arquivo
    
        if (['jpg', 'jpeg', 'png', 'gif'].includes(fileExtension)) {
            // Se for uma imagem, cria o HTML para exibir a imagem
            newMessage.innerHTML = `
                <strong>${data.username}:</strong>
                <div>
                    <img src="${data.file}" alt="${data.filename}" style="max-width: 200px; max-height: 200px;"><br>
                    <a href="${data.file}" download="${data.filename}">${data.filename}</a>${timeDisplay}
                </div>
            `;
        } else if (['mp3', 'wav', 'ogg'].includes(fileExtension)) {
            // Se for um arquivo de áudio, cria o HTML para exibir o player de áudio
            newMessage.innerHTML = `
                <strong>${data.username}:</strong>
                <div>
                    <audio controls>
                        <source src="${data.file}" type="audio/mpeg">
                        Seu navegador não suporta o elemento de áudio.
                    </audio>
                    <!-- <br><a href="${data.file}" download="${data.filename}">${data.filename}</a>${timeDisplay} -->
                </div>
            `;
        } else {
            // Para outros tipos de arquivos, apenas cria um link
            newMessage.innerHTML = `
                <strong>${data.username}:</strong>
                <a href="${data.file}" download="${data.filename}">${data.filename}</a>${timeDisplay}
            `;
        }
    } else {
        // Se a mensagem não contém arquivo, apenas exibe a mensagem de texto
        newMessage.innerHTML = `<strong>${data.username}:</strong> ${data.message}${timeDisplay}`;
    }

    chatLog.appendChild(newMessage);  // Adiciona a nova mensagem ao log do chat
    chatLog.scrollTop = chatLog.scrollHeight;  // Rolagem automática para mostrar a última mensagem
};