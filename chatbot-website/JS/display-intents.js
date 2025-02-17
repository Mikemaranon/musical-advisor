document.addEventListener('DOMContentLoaded', function () {
    let jsonData; // Variable para almacenar los datos cargados

    function assignIntentEvents() {
        document.querySelectorAll('.intent').forEach(intentDiv => {
            intentDiv.onclick = () => createQuestionDivs(addLow(intentDiv.textContent.trim()));
        });
    }

    function createIntentDivs(data) {
        jsonData = data; // Guardar datos en una variable global

        const intents = data.assets.intents;
        const container = document.querySelector('.intent-container');

        intents.forEach(intent => {
            const intentDiv = document.createElement('div');
            intentDiv.classList.add('intent');
            intentDiv.textContent = formatAnalysisResponse(intent.category);
            container.appendChild(intentDiv);
        });
        assignIntentEvents();
    }

    function createQuestionDivs(intentName) {
        const utterances = jsonData.assets.utterances.filter(u => u.intent === intentName);
        const sendButton = document.querySelector('#send-button');
        if (utterances.length === 0) {
            console.error(`No se encontraron frases para el intent: ${intentName}`);
            return;
        }

        const shuffledTexts = utterances.map(u => u.text).sort(() => Math.random() - 0.5);
        const selectedTexts = shuffledTexts.slice(0, 10);

        const questionContainer = document.querySelector('.question-box');
        questionContainer.innerHTML = ''; // Limpiar preguntas previas

        selectedTexts.forEach(text => {
            const div = document.createElement('div');
            div.classList.add('question');
            div.textContent = text;

            // Añadir evento onclick al div
            div.onclick = function() {
                addTextToChatInput(text); // Llamar a la función que añade el texto al input
                sendMessage(); // Enviar el mensaje automáticamente
            };

            questionContainer.appendChild(div);
        });
    }

    // Función para añadir el texto al input del chat
    function addTextToChatInput(text) {
        const chatInput = document.querySelector('#chat-input'); // Asegúrate de tener un input con el id "chat-input"
        chatInput.value = text; // Asignar el texto al campo de entrada
    }

    fetch('../../../Azure/azure-clu/clu_project.json')
        .then(response => response.json())
        .then(data => {
            jsonData = data;
            createIntentDivs(data);
        })
        .catch(error => console.error('Error al cargar el archivo JSON:', error));
});
