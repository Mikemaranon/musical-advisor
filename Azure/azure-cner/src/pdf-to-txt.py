import os
from dotenv import load_dotenv
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener las variables de entorno
endpoint = os.getenv("AZURE_ENDPOINT")
api_key = os.getenv("AZURE_API_KEY")

# Cliente de Form Recognizer
client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))

# Directorios
pdfs_dir = 'pdfs'  # Ruta a la carpeta de PDFs
output_dir = 'txt_outputs'  # Carpeta para los archivos de texto

# Asegurarse de que la carpeta de salida exista
os.makedirs(output_dir, exist_ok=True)

# Función para analizar y guardar el texto
def analyze_pdf(pdf_path):
    with open(pdf_path, "rb") as f:
        poller = client.begin_analyze_document("prebuilt-document", f)
        result = poller.result()
        
        # Guardar el texto extraído
        output_path = os.path.join(output_dir, os.path.basename(pdf_path).replace(".pdf", ".txt"))
        with open(output_path, "w", encoding="utf-8") as txt_file:
            for page in result.pages:
                for line in page.lines:
                    txt_file.write(line.content + "\n")
            print(f"Texto extraído y guardado en {output_path}")
        
# Analizar cada PDF
for pdf_file in os.listdir(pdfs_dir):
    if pdf_file.endswith(".pdf"):
        pdf_path = os.path.join(pdfs_dir, pdf_file)
        analyze_pdf(pdf_path)
