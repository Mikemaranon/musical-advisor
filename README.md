# Chatbot de preguntas y respuestas
Este proyecto consiste en un chatbot que responde preguntas usando los servicios de Azure Cognitive Language Services. Ha sido entrenado scrappeando el contenido de Madrid Hifi, una tienda de instrumentos musicales.  
## 1: Web Scrapping
Ejecutando `Madrid-HiFi.py` puedes extraer los datos introduciendo el fabricante del que te gustaría recolectar.  
## 2: Preparación de datos
Ejecutando `qna_generate_questions.py` analizarás el JSON creado en el paso 1 para generar el fichero TSV y JSON que necesitaremos para alimentar al bot
## 3: QnA en Azure
Creando un proyecto de preguntas y respuestas en Azure Cognitive Language Services, importamos el TSV como datos de entrenamiento para que genere los pares automáticamente.  
Posteriormente lanzamos el proyecto para que sea accesible a través de la red
## 4: Chatbot en la web
Accediendo a `chatbot-website/chatbot.html` tendremos ya listo todo lo necesario para poder empezar a usar el bot. Introduce en `keys.json` la clave API y el endpoint de tu proyecto.  
En el caso de que no los reconozca bien, puedes introducirlos manualmente dentro del código JS en la función `sendMessageToModel` en las variables `endpoint` y `subscriptionKey`
