# Chatbot interactivo para recomendar productos en [Madrid HiFi](https://www.madridhifi.com)
Este proyecto consiste en un chatbot que responde preguntas usando los servicios de Azure Cognitive Language Services. Ha sido entrenado scrappeando el contenido de Madrid Hifi, una tienda de instrumentos musicales.  
## 1: Web Scrapping
Ejecutando `Madrid-HiFi.py` puedes extraer los datos introduciendo el fabricante del que te gustaría recolectar.  
## 2: Preparación de datos
Ejecutando `qna_generate_questions.py` analizarás el JSON creado en el paso 1 para generar el fichero TSV y JSON que necesitaremos para alimentar al bot
## 3: QnA en Azure
Creando un proyecto de preguntas y respuestas en Azure Cognitive Language Services, importamos el TSV como datos de entrenamiento para que genere los pares automáticamente.  
Posteriormente lanzamos el proyecto para que sea accesible a través de la red
## 4: CLU en azure
Ejecutamos el script `clu_project_maker.py` para generar nuestro archivo json de proyecto con toda la información ya clasificada.  
Creamos un proyecto conversacional en Azure Cognitive Language Service subiendo el archivo generado en `azure-clu/clu_proyect.json`, acto seguido entrenamos el modelo en modo avanzado (ya que la información está en español y el modo gratuito solo soporta inglés), tras 15 minutos estará listo (depende de la cantidad de datos que hayamos metido en el modelo).  
Cuando tengamos el entrenamiento listo, desplegamos el modelo.
## 5: Chatbot en la web
Accediendo a `chatbot-website/chatbot.html` tendremos ya listo todo lo necesario para poder empezar a usar el bot. Introduce en `keys.json` la clave API y el endpoint de tu proyecto.  
En el caso de que no los reconozca bien, puedes introducirlos manualmente dentro del código JS en la función `sendMessageToModel` en las variables `endpoint` y `subscriptionKey`. Realizar el mismo proceso con las claves de conversational model en la función `analyzeConversation`

# Ask-HiFi: Como usar el Bot
Este bot esta conectado a servicios de azure que emplean herramientas de Inteligencia Artificial Tradicional. Su funcionamiento no es comparable a cualquier otro chatbot de IA generativa (como Copilot, DeepSeek o ChatGPT). Esto es un proyecto realizado en poco tiempo y no ha podido ser entrenado con los suficientes datos para poder abarcar un caso realista, por lo que es muy posible que muchas preguntas no puedan ser identificadas correctamente en la base de datos generada mediante los scripts.  
Para poder solventar este problema he añadido las secciones de los laterales las cuales generan preguntas directamente desde la base de datos con la que se ha alimentado al bot, de esta forma se puede ver su rendimiento en el caso óptimo. Se pueden generar preguntas manualmente las cuales si tienen las palabras clave adecuadas también serán respondidas aunque no siempre con éxito.  

> ⚠️ **Advertencia:**
La intención de este proyecto es poder observar como se tratan las interacciones con el bot para que este identifique las intenciones del usuario junto con una respuesta apropiada a la pregunta tras su respectivo entrenamiento.  
Porfavor, cualquier propuesta y critica constructiva para ayudar a mejorar este proyecto es bienvenida puesto que su unica finalidad es ayudar a mi proceso formativo en el uso de sercicios de Azure e IA.   


![image](https://github.com/user-attachments/assets/9440eff6-d445-4e25-974d-aa747f55057b)


