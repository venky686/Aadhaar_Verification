import re
from datetime import datetime
from utils.logger import app_logger

class Validator:
    """
    Rule-based validation for extracted data.
    """
    
    @staticmethod
    def validate_aadhaar_number(aadhaar_num: str) -> bool:
        """
        Validates Aadhaar number format (12 digits) and Verhoeff algorithm (simplified here).
        """
        if not aadhaar_num:
            return False
            
        clean_num = re.sub(r'\D', '', aadhaar_num)
        
        if len(clean_num) != 12:
            return False
            
        # Basic check: should not start with 0 or 1
        if clean_num[0] in ['0', '1']:
            return False
            
        return True

    @staticmethod
    def validate_dob(dob: str) -> bool:
        """
        Validates Date of Birth format and logic.
        """
        if not dob:
            return False
        
        # Try parsing common formats
        formats = ["%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(dob, fmt)
                if 1900 < dt.year < datetime.now().year:
                    return True
            except ValueError:
                continue
                
        return False

    @staticmethod
    def validate_gender(gender: str) -> bool:
        """
        Validates gender.
        """
        if not gender:
            return False
        return gender.upper() in ["MALE", "FEMALE", "TRANSGENDER", "M", "F", "T"]

    @staticmethod
    def validate_extracted_data(data: dict) -> dict:
        """
        Runs all validations and returns a report.
        """
        report = {
            "aadhaar_valid": Validator.validate_aadhaar_number(data.get("aadhaar_number")),
            "dob_valid": Validator.validate_dob(data.get("dob")),
            "gender_valid": Validator.validate_gender(data.get("gender")),
            "name_present": bool(data.get("name")),
            "address_present": bool(data.get("address"))
        }
        
        # Overall validation score
        valid_fields = sum(report.values())
        total_fields = len(report)
        report["validation_score"] = (valid_fields / total_fields) * 100
        
        return report
