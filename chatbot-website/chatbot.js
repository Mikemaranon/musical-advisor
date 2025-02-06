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
