import json
from openai import AzureOpenAI
from utils.config import settings
from utils.logger import app_logger
from llm.prompt_templates import PromptTemplates

class OpenAIRefiner:
    """
    Uses Azure OpenAI to refine and normalize OCR extracted text.
    """
    
    def __init__(self):
        self.endpoint = settings.AZURE_OPENAI_ENDPOINT
        self.key = settings.AZURE_OPENAI_KEY
        self.deployment = settings.AZURE_OPENAI_DEPLOYMENT_NAME
        self.api_version = settings.AZURE_OPENAI_API_VERSION
        
        if not self.endpoint or not self.key:
            app_logger.warning("Azure OpenAI credentials not set.")
            self.client = None
        else:
            self.client = AzureOpenAI(
                api_key=self.key,
                api_version=self.api_version,
                azure_endpoint=self.endpoint
            )

    def refine_extracted_data(self, raw_data: dict) -> dict:
        """
        Sends raw OCR data to LLM for correction.
        """
        if not self.client:
            return raw_data

        try:
            prompt = PromptTemplates.AADHAAR_CORRECTION_USER.format(raw_data=json.dumps(raw_data))
            
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=[
                    {"role": "system", "content": PromptTemplates.AADHAAR_CORRECTION_SYSTEM},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            corrected_data = json.loads(content)
            return corrected_data
            
        except Exception as e:
            if "DeploymentNotFound" in str(e):
                app_logger.error(f"Azure OpenAI Deployment '{self.deployment}' not found. Please check AZURE_OPENAI_DEPLOYMENT_NAME in .env")
            else:
                app_logger.error(f"Error refining data with OpenAI: {e}")
            return raw_data
