// audioRecorder.js

import { getCookie, uploadFile } from './fileUpload.js';  // Importa funções de fileUpload.js

let mediaRecorder;
let audioChunks = [];

// Função para iniciar a gravação de áudio
export const startRecording = async (sendAudioButton, socket, loggedUserCode) => {
    sendAudioButton.classList.add('recording');

    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };

        mediaRecorder.start();
    } else {
        alert('Seu navegador não suporta gravação de áudio.');
    }
};

// Função para parar a gravação e enviar o arquivo
export const stopRecording = async (sendAudioButton, socket, loggedUserCode) => {
    sendAudioButton.classList.remove('recording');

    if (mediaRecorder) {
        mediaRecorder.stop();

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/mpeg' });

            // Cria um nome de arquivo único usando a data e hora atuais
            const timestamp = new Date().toISOString().replace(/[:.-]/g, '_'); // Substitui caracteres inválidos
            const file = new File([audioBlob], `audio_recording_${timestamp}.mp3`, { type: 'audio/mpeg' });

            // Enviar o arquivo usando a função uploadFile
            const csrftoken = getCookie('csrftoken');  // Obtém o token CSRF
            await uploadFile(file, csrftoken, loggedUserCode, socket);  // Faz o upload do arquivo

            // Limpa os chunks de áudio
            audioChunks = [];
        };

        mediaRecorder.stream.getTracks().forEach(track => track.stop());
    }
};

// Função para lidar com o mouseleave do botão de gravação
export const handleMouseLeave = (sendAudioButton) => {
    sendAudioButton.classList.remove('recording');
    if (mediaRecorder) {
        mediaRecorder.stop();
        audioChunks = [];
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
    }
};