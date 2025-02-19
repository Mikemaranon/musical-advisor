function formatAnalysisResponse(botResponse) {
    botResponse = botResponse.replace(/_/g, ' ');
    return botResponse;
}

function addLow(botResponse) {
    botResponse = botResponse.replaceAll(' ', '_');
    return botResponse;
}

function normalyzeStr(text) {
    return text
        .toLowerCase()                   // Convertir a minúsculas
        .normalize('NFD')                 // Descomponer los caracteres con tildes
        .replace(/[\u0300-\u036f]/g, "")  // Eliminar los diacríticos (tildes)
        .replace(/\s+/g, '');             // Eliminar los espacios
}

fetch('../JS/keywords.json') // Sube dos niveles desde chatbot-website
        .then(response => response.json())
        .then(data => {
            console.log('Archivo JSON cargado correctamente', data);
            keywords = data; 
        })
        .catch(error => console.error('Error al cargar el archivo JSON:', error));

document.addEventListener('DOMContentLoaded', function() {
    const chatBox = document.querySelector('.chat-box');
    const chatInput = document.querySelector('.chat-input');

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
            sendMessageToModel_L3(message);
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

    async function analyzeConversation_L2(query, participantId = "user", language = "es") {
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
    
        //console.log("Enviando petición a Azure con:", JSON.stringify(requestBody, null, 2));
    
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
                addMessageToChat('analysis', "intención: " + formatAnalysisResponse(botResponse), true);
                return botResponse
            } else {
                console.error(`Error en la API de Azure: ${response.status} - ${data?.error?.message}`);
                addMessageToChat('analysis', `Error en la respuesta de Azure: ${data?.error?.message}`);
            }
        } catch (error) {
            console.error("Error al conectar con Azure:", error);
            addMessageToChat('analysis', "Error al obtener la respuesta.");
        }
    }

    async function queryCosmosDB(query) {
        const endpoint = "https://hifi-cosmosdb.documents.azure.com:443/";
        const databaseId = "ToDoList"; // Reemplaza con tu ID de base de datos
        const containerId = "Items"; // Reemplaza con tu ID de contenedor
        const subscriptionKey = "";
    
        // Crea el URL de la consulta
        const url = `${endpoint}dbs/${databaseId}/colls/${containerId}/docs`;
    
        const options = {
            method: "POST",
            headers: {
                "Authorization": subscriptionKey, // Autenticación
                "Content-Type": "application/query+json",
                "x-ms-version": "2018-12-31",
                "x-ms-documentdb-isquery": "true"
            },
            body: JSON.stringify({ query }) // Cuerpo de la consulta
        };
    
        try {
            const response = await fetch(url, options);
            const data = await response.json();
    
            if (response.ok) {
                return data.Documents; // Devuelve los documentos encontrados
            } else {
                console.error(`Error en la consulta a Cosmos DB: ${response.status} - ${data.message}`);
                throw new Error(`Error en la consulta: ${data.message}`);
            }
        } catch (error) {
            console.error("Error al conectar con Cosmos DB:", error);
            throw error; // Lanza el error para manejarlo en otro lugar si es necesario
        }
    }

    async function sendMessageToModel_L3(message) {

        const intent = analyzeConversation_L2(message);
        let query = '';
        const filteredMessage = await extractKeyWords(message);
        console.log('Componentes del mensaje filtrado', filteredMessage);
    
        let queryBody = craftQuery(filteredMessage);
    
        switch(intent) {
            case 'mostrar_lista_de_productos':
                query = `SELECT c.title FROM c ${queryBody}`;
                break;
    
            case 'saber_caracteristicas':
                query = `SELECT c.title, c.features FROM c ${queryBody}`;
                break;
    
            case 'saber_disponibilidad':
                query = `SELECT c.title, c.availability FROM c ${queryBody}`;
                break;
    
            case 'saber_redireccion':
                query = `SELECT c.title, c.url FROM c ${queryBody}`;
                break;
    
            case 'saber_precio':
                const priceIntent = analyzePriceIntent(message);
                if (priceIntent) {
                    switch(priceIntent) {
                        case 'caro':
                            query = `SELECT c.title, c.url FROM c ${queryBody} ORDER BY c.current_price DESC OFFSET 0 LIMIT 5`;
                            break;
    
                        case 'barato':
                            query = `SELECT c.title, c.url FROM c ${queryBody} ORDER BY c.current_price ASC OFFSET 0 LIMIT 5`;
                            break;
    
                        case 'medio':
                            query = `SELECT c.title, c.url FROM c ${queryBody} WHERE c.current_price BETWEEN (SELECT AVG(c.current_price) - 5 FROM c) AND (SELECT AVG(c.current_price) + 5 FROM c) OFFSET 0 LIMIT 5`;
                            break;
    
                        case 'rebajas':
                            query = `SELECT c.title, c.url FROM c ${queryBody} ORDER BY c.price_reduction DESC OFFSET 0 LIMIT 5`;
                            break;
                    }
                }
                break;
        }
    
        console.log("Query generada:", query);
    
        // Aquí iría la conexión a CosmosDB

        queryCosmosDB(query)
    }
    
    async function extractKeyWords(message) {
        try {
            const keywordsData = keywords;
            const foundKeywords = {};
    
            // Normalizamos el mensaje de entrada
            const mensajeNormalizado = normalyzeStr(message);
            console.log("Mensaje normalizado:", mensajeNormalizado);
    
            // Recorremos las claves y las listas de palabras clave
            for (const category in keywordsData) {
                if (keywordsData.hasOwnProperty(category)) {
                    const keywords = keywordsData[category];
                    const coincidencias = keywords.filter(keyword => 
                        mensajeNormalizado.includes(normalyzeStr(keyword)) // Compara el término normalizado
                    );
    
                    console.log(`Palabras clave en ${category}:`, keywords);
                    console.log(`Coincidencias encontradas:`, coincidencias);
    
                    if (coincidencias.length > 0) {
                        foundKeywords[category] = coincidencias;
                    }
                    break;
                }
            }
    
            console.log("Resultado final de coincidencias:", foundKeywords);
            return foundKeywords;
    
        } catch (error) {
            console.error('Error al cargar o procesar el archivo de palabras clave:', error);
            return {};
        }
    }    

    function craftQuery(keywords) {
        if (!keywords || Object.keys(keywords).length === 0) {
            return ""; // No hay filtros
        }
    
        let conditions = [];
    
        for (const type in keywords) {
            if (keywords.hasOwnProperty(type)) {
                const words = keywords[type].map(word => `LOWER("${word}")`).join(", ");
                conditions.push(`(ARRAY_CONTAINS(c.features, ${words}, true) AND ARRAY_CONTAINS(c.type, '${type}', true))`);
            }
        }
        
        return conditions.length > 0 ? `WHERE ${conditions.join(" OR ")}` : "";
    }       

    function analyzePriceIntent(message) {
        const normalizedMessage = normalyzeStr(message);
    
        const priceKeywords = {
            "caro": ["más caro", "lo más caro", "precio alto", "mayor precio", "más costoso", "menos barato"],
            "barato": ["más barato", "lo más barato", "precio bajo", "menor precio", "más económico", "menos caro"],
            "medio": ["precio medio", "precio promedio", "en medio", "equilibrado", "media", "normal"],
            "rebajas": ["rebaja", "descuento", "oferta", "promoción", "precio reducido"]
        };
    
        for (const category in priceKeywords) {
            if (priceKeywords[category].some(keyword => normalizedMessage.includes(normalyzeStr(keyword)))) {
                return category;
            }
        }
    
        return null; // No se detectó ninguna categoría de precio
    }    
});
