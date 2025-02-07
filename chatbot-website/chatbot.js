const subscriptionKey = "AaOOJMzfudw2A0CXdT9t37SnuQ2MJlcaL8oaOiEplqLM8IDD1OrAJQQJ99BBACYeBjFXJ3w3AAAaACOGmY72";
const endpoint = "https://languaje-service-mike-tajamar.cognitiveservices.azure.com/language/:analyze-conversations?api-version=2022-10-01-preview";

document.addEventListener('DOMContentLoaded', function() {
    const chatBox = document.querySelector('.chat-box');
    const chatInput = document.querySelector('.chat-input');

    chatInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            const userMessage = chatInput.value;
            if (userMessage.trim() !== '') {
                addMessageToChat('user', userMessage);
                chatInput.value = '';
                sendMessageToModel(userMessage);
            }
        }
    });

    document.querySelector('.send-button').addEventListener('click', sendMessage);

    function sendMessage() {
        const input = document.querySelector('.chat-input');
        const message = input.value;
        if (message.trim() !== "") {
            addMessageToChat('user', message);
            input.value = "";
            sendMessageToModel(message);
        }
    }

    function addMessageToChat(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('chat-message', sender);
        messageElement.textContent = message;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // read ../azure-qna/questions.json
    fetch('../azure-qna/questions.json')
    .then(response => response.json()) // Convierte la respuesta a formato JSON
    .then(data => {
        console.log('Archivo JSON cargado correctamente');
        questions = data;
    })
    .catch(error => {
        console.error('Error al cargar el archivo JSON:', error);
    });

    function generateQuestions(questions) {
        const container = document.querySelector('.sugested-questions');
        container.innerHTML = ''; // Limpiar cualquier contenido previo

        // Seleccionar 4 preguntas al azar
        const randomQuestions = [];
        while (randomQuestions.length < 1) {
            const randomIndex = Math.floor(Math.random() * questions.length);
            if (!randomQuestions.includes(questions[randomIndex])) {
                randomQuestions.push(questions[randomIndex]);
            }
        }

        // Crear un div para cada pregunta
        randomQuestions.forEach(questionObj => {
            const questionText = Object.keys(questionObj)[0];
            const questionDiv = document.createElement('div');
            questionDiv.classList.add('question');
            questionDiv.textContent = questionText;
            container.appendChild(questionDiv);
        });
    }

    document.getElementById('generate-btn').addEventListener('click', function() {
        generateQuestions(questionsJson);
    });

    // Llamar a la función para generar las preguntas
    generateQuestions(questionsJson);
    
    async function sendMessageToModel(message) {
        try {
            const response = await fetch("https://languaje-service-mike-tajamar.cognitiveservices.azure.com/language/:analyze-conversations?api-version=2022-10-01-preview", {
                method: 'POST',
                headers: {
                    'Ocp-Apim-Subscription-Key': 'AaOOJMzfudw2A0CXdT9t37SnuQ2MJlcaL8oaOiEplqLM8IDD1OrAJQQJ99BBACYeBjFXJ3w3AAAaACOGmY72',
                    'Apim-Request-Id': '4ffcac1c-b2fc-48ba-bd6d-b69d9942995a',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    kind: "Conversation",
                    analysisInput: {
                        conversationItem: {
                            id: "PARTICIPANT_ID_HERE",
                            text: message,
                            modality: "text",
                            language: "QUERY_LANGUAGE_HERE",
                            participantId: "PARTICIPANT_ID_HERE"
                        }
                    },
                    parameters: {
                        projectName: "musical-advisor",
                        verbose: true,
                        deploymentName: "CHATBOT-1",
                        stringIndexType: "TextElement_V8"
                    }
                })
            });
            const data = await response.json();
            addMessageToChat('bot', data.response);
        } catch (error) {
            console.error('Error:', error);
        }
    }

    //curl -X POST "https://languaje-service-mike-tajamar.cognitiveservices.azure.com/language/:analyze-conversations?api-version=2022-10-01-preview" -H "Ocp-Apim-Subscription-Key: AaOOJMzfudw2A0CXdT9t37SnuQ2MJlcaL8oaOiEplqLM8IDD1OrAJQQJ99BBACYeBjFXJ3w3AAAaACOGmY72"  -H "Apim-Request-Id: 4ffcac1c-b2fc-48ba-bd6d-b69d9942995a" -H "Content-Type: application/json" -d "{\"kind\":\"Conversation\",\"analysisInput\":{\"conversationItem\":{\"id\":\"PARTICIPANT_ID_HERE\",\"text\":\"YOUR_QUERY_HERE\",\"modality\":\"text\",\"language\":\"QUERY_LANGUAGE_HERE\",\"participantId\":\"PARTICIPANT_ID_HERE\"}},\"parameters\":{\"projectName\":\"musical-advisor\",\"verbose\":true,\"deploymentName\":\"CHATBOT-1\",\"stringIndexType\":\"TextElement_V8\"}}"


});
