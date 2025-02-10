const subscriptionKey = "AaOOJMzfudw2A0CXdT9t37SnuQ2MJlcaL8oaOiEplqLM8IDD1OrAJQQJ99BBACYeBjFXJ3w3AAAaACOGmY72";
const endpoint = "https://languaje-service-mike-tajamar.cognitiveservices.azure.com/language/:analyze-conversations?api-version=2022-10-01-preview";

document.addEventListener('DOMContentLoaded', function() {
    const chatBox = document.querySelector('.chat-box');
    const chatInput = document.querySelector('.chat-input');
    const randomButton = document.querySelector('#random-button'); // Seleccionar el botón
    let questions = []; // Inicializamos un array vacío para las preguntas

    chatInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });

    document.querySelector('#send-button').addEventListener('click', sendMessage);

    function sendMessage() {
        const message = chatInput.value.trim();
        if (message !== "") {
            addMessageToChat('user', message);
            chatInput.value = "";
            sendMessageToModel(message);
        }
    }

    function addMessageToChat(sender, message, isHTML = false) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('chat-message', sender);
        if (isHTML) {
            messageElement.innerHTML = message;
        } else {
            messageElement.textContent = message;
        }
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Cargar preguntas desde JSON
    fetch('../../azure-qna/questions.json') // Sube dos niveles desde chatbot-website
        .then(response => response.json())
        .then(data => {
            console.log('Archivo JSON cargado correctamente', questions);
            questions = data; // Asegúrate de que el JSON tiene una clave "questions"
        })
        .catch(error => console.error('Error al cargar el archivo JSON:', error));


    // Evento para el botón "random"
    randomButton.addEventListener('click', function() {
        if (questions.length > 0) {
            const randomIndex = Math.floor(Math.random() * questions.length);
            const randomQuestionObj = questions[randomIndex]; // Obtener objeto aleatorio
            const randomQuestion = Object.keys(randomQuestionObj)[0]; // Extraer la clave (pregunta)
            chatInput.value = randomQuestion; // Insertar pregunta en el input
        } else {
            console.error("No se han cargado preguntas correctamente.");
        }
    });

    fetch('./keys.json')
        .then(response => response.json())
        .then(data => {
            subscriptionKey = data.AZURE_SUBSCRIPTION_KEY;
            endpoint = data.AZURE_ENDPOINT;
            console.log('Configuración cargada:', subscriptionKey, endpoint);
        })
        .catch(error => {
            console.error('Error al cargar el archivo de configuración:', error);
        });
    
    function formatBotResponse(botResponse) {
        // Dividir el texto en dos partes: antes y después de "::"
        const [paragraph, listItems] = botResponse.split('::');
        
        // Crear el párrafo
        let formattedResponse = `<p>${paragraph.trim()}</p>`;
        
        // Crear la lista desordenada si hay elementos de lista
        if (listItems) {
            const items = listItems.split(';;');
            formattedResponse += '<ul>';
            items.forEach(item => {
                // Extraer el texto y el enlace del item
                const match = item.match(/\[(.*?)\]\((.*?)\)/);
                if (match) {
                    const text = match[1];
                    const url = match[2];
                    formattedResponse += `<li><a href="${url}" target="_blank">${text}</a> ${item.replace(match[0], '').trim()}</li>`;
                } else {
                    formattedResponse += `<li>${item.trim()}</li>`;
                }
            });
            formattedResponse += '</ul>';
        } else {
            // Procesar enlaces en el párrafo
            const match = paragraph.match(/\[(.*?)\]\((.*?)\)/);
            if (match) {
                const text = match[1];
                const url = match[2];
                formattedResponse = `<p>${paragraph.replace(match[0], `<a href="${url}" target="_blank">${text}</a>`).trim()}</p>`;
            }
        }
        
        return formattedResponse;
    }

    async function analyzeConversation(query, participantId = "user", language = "es") {
        const endpoint = "https://languaje-service-mike-tajamar.cognitiveservices.azure.com/language/:analyze-conversations?api-version=2022-10-01-preview";
        const subscriptionKey = "AaOOJMzfudw2A0CXdT9t37SnuQ2MJlcaL8oaOiEplqLM8IDD1OrAJQQJ99BBACYeBjFXJ3w3AAAaACOGmY72";
    
        const requestBody = {
            kind: "Conversation",
            analysisInput: {
                conversationItem: {
                    id: participantId,
                    text: query,
                    modality: "text",
                    language: language,
                    participantId: participantId
                }
            },
            parameters: {
                projectName: "musical-advisor",
                verbose: true,
                deploymentName: "ask-hifi-L2",
                stringIndexType: "TextElement_V8"
            }
        };
    
        console.log("Enviando petición a Azure con:", JSON.stringify(requestBody, null, 2));
    
        try {
            const response = await fetch(endpoint, {
                method: "POST",
                headers: {
                    "Ocp-Apim-Subscription-Key": subscriptionKey,
                    "Content-Type": "application/json",
                    "Apim-Request-Id": "4ffcac1c-b2fc-48ba-bd6d-b69d9942995a"
                },
                body: JSON.stringify(requestBody)
            });
    
            const data = await response.json();
            console.log("Respuesta recibida de Azure:", data);
    
            if (response.ok) {
                const botResponse = data.result?.prediction?.topIntent || "No se pudo determinar la intención.";
                addMessageToChat('analysis', formatAnalysisResponse(botResponse), true);
            } else {
                console.error(`Error en la API de Azure: ${response.status} - ${data?.error?.message}`);
                addMessageToChat('analysis', `Error en la respuesta de Azure: ${data?.error?.message}`);
            }
        } catch (error) {
            console.error("Error al conectar con Azure:", error);
            addMessageToChat('analysis', "Error al obtener la respuesta.");
        }
    }

    function formatAnalysisResponse(botResponse) {
        botResponse = botResponse.replace(/_/g, ' ');
        let response = "intención: " + botResponse;
        return response;
    }

    async function sendMessageToModel(message) {
    
        const endpoint = "https://languaje-service-mike-tajamar.cognitiveservices.azure.com/language/:query-knowledgebases?projectName=ask-hifi&api-version=2021-10-01&deploymentName=production";
        const subscriptionKey = "AaOOJMzfudw2A0CXdT9t37SnuQ2MJlcaL8oaOiEplqLM8IDD1OrAJQQJ99BBACYeBjFXJ3w3AAAaACOGmY72";

        const requestBody = {
            "top": 3,
            "question": message,
            "includeUnstructuredSources": true,
            "confidenceScoreThreshold": 0.5,
            "answerSpanRequest": {
                "enable": true,
                "topAnswersWithSpan": 1,
                "confidenceScoreThreshold": 0.5
            },
            "filters": {
                "metadataFilter": {
                    "logicalOperation": "AND",
                    "metadata": []
                }
            }
        };

        console.log("Enviando petición a Azure con:", JSON.stringify(requestBody, null, 2));

        try {
            // Call analyzeConversation and get the output
            const analysisOutput = await analyzeConversation(message);

            const response = await fetch(endpoint, {
                method: "POST",
                headers: {
                    "Ocp-Apim-Subscription-Key": subscriptionKey,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(requestBody)
            });

            const data = await response.json();
            console.log("Respuesta recibida de Azure:", data);

            if (response.ok) {
                const botResponse = data.answers?.[0]?.answer || "No tengo una respuesta para eso.";
                //addMessageToChat('bot', botResponse);
                const formattedResponse = formatBotResponse(botResponse);
                addMessageToChat('bot', formattedResponse, true);
            } else {
                console.error(`Error en la API de Azure: ${response.status} - ${data?.error?.message}`);
                addMessageToChat('bot', `Error en la respuesta de Azure: ${data?.error?.message}`);
            }

        } catch (error) {
            console.error("Error al conectar con Azure:", error);
            addMessageToChat('bot', "Error al obtener la respuesta.");
        }
    } 
});
