from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from utils.config import settings
from utils.logger import app_logger

class AzureOCR:
    """
    Wrapper for Azure AI Document Intelligence (Form Recognizer).
    """
    
    def __init__(self):
        self.endpoint = settings.AZURE_FORM_RECOGNIZER_ENDPOINT
        self.key = settings.AZURE_FORM_RECOGNIZER_KEY
        
        if not self.endpoint or not self.key:
            app_logger.warning("Azure Form Recognizer credentials not set.")
            self.client = None
        else:
            self.client = DocumentAnalysisClient(
                endpoint=self.endpoint, 
                credential=AzureKeyCredential(self.key)
            )

    def analyze_document(self, document_content: bytes) -> dict:
        """
        Analyze document using the prebuilt-idDocument model.
        """
        if not self.client:
            raise ValueError("Azure OCR client is not initialized.")

        try:
            poller = self.client.begin_analyze_document(
                "prebuilt-idDocument", document=document_content
            )
            result = poller.result()
            
            extracted_data = []
            
            for idx, document in enumerate(result.documents):
                doc_data = {
                    "doc_type": document.doc_type,
                    "confidence": document.confidence,
                    "fields": {}
                }
                
                for name, field in document.fields.items():
                    field_value = field.value if field.value else field.content
                    doc_data["fields"][name] = {
                        "value": field_value,
                        "confidence": field.confidence
                    }
                
                extracted_data.append(doc_data)
                
            return {"documents": extracted_data, "raw_result": result}
            
        except Exception as e:
            app_logger.error(f"Error analyzing document with Azure OCR: {e}")
            raise
