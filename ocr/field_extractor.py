import re
from typing import Dict, Any
from utils.logger import app_logger

class FieldExtractor:
    """
    Extracts and normalizes Aadhaar specific fields from OCR output.
    """
    
    @staticmethod
    def extract_aadhaar_fields(ocr_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parses the Azure OCR result to find Aadhaar fields.
        """
        extracted = {
            "aadhaar_number": None,
            "name": None,
            "dob": None,
            "gender": None,
            "address": None,
            "pincode": None
        }
        
        try:
            if not ocr_result.get("documents"):
                return extracted
                
            # Assuming single document for now
            doc = ocr_result["documents"][0]
            fields = doc.get("fields", {})
            
            # Map Azure prebuilt-idDocument fields to our schema
            # Note: Azure might map these differently depending on the model version
            
            if "DocumentNumber" in fields:
                extracted["aadhaar_number"] = fields["DocumentNumber"]["value"]
            
            if "FirstName" in fields and "LastName" in fields:
                extracted["name"] = f"{fields['FirstName']['value']} {fields['LastName']['value']}"
            elif "FirstName" in fields:
                 extracted["name"] = fields["FirstName"]["value"]
            elif "LastName" in fields: # Fallback
                 extracted["name"] = fields["LastName"]["value"]
                 
            if "DateOfBirth" in fields:
                extracted["dob"] = str(fields["DateOfBirth"]["value"])
                
            if "Sex" in fields:
                extracted["gender"] = fields["Sex"]["value"]
                
            if "Address" in fields:
                extracted["address"] = fields["Address"]["value"]
                
            # Post-processing for Aadhaar Number if not found directly
            # Sometimes it might be in 'MachineReadableZone' or just raw text
            
            return extracted
            
        except Exception as e:
            app_logger.error(f"Error extracting fields: {e}")
            return extracted

    @staticmethod
    def normalize_aadhaar(aadhaar_num: str) -> str:
        """
        Removes spaces and non-digit characters from Aadhaar number.
        """
        if not aadhaar_num:
            return ""
        return re.sub(r'\D', '', str(aadhaar_num))
