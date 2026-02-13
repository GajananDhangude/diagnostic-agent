from src.state import DDRState
from src.utils.pdf_tools import process_doc


def pdf_extraction_agent(state:DDRState) -> DDRState:
    """Extract text from both PDFs"""


    inspection_text = process_doc(state['inspection_pdf_path'])

    thermal_text = process_doc(state['thermal_pdf_path'])
        
    return {
        "inspection_text": inspection_text,
        "thermal_text": thermal_text
    }