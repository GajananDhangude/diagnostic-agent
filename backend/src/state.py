from typing import TypedDict, Optional
from src.schema import DDRReport

class DDRState(TypedDict):
    inspection_pdf_path: str
    thermal_pdf_path: str
    
    # Extracted Text
    inspection_text: str
    thermal_text: str

    report:Optional[DDRReport]

    markdown_content:str