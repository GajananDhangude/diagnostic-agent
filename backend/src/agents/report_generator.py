from src.state import DDRState
from src.utils.llm import llm


def report_generation_agent(state:DDRState) -> DDRState:
    """Generate professional markdown report"""

    extracted_text = state['report']


    markdown= f"""You are a professional building diagnostic expert. Convert the following 
    JSON data into a formal, highly detailed Markdown Diagnostic Report (DDR).

    JSON DATA:
    {extracted_text}

    OUTPUT REQUIREMENTS (DDR Structure):
    1. Property Issue Summary
    2. Area‑wise Observations
    3. Probable Root Cause
    4. Severity Assessment (with reasoning)
    5. Recommended Actions
    6. Additional Notes
    7. Missing or Unclear Information (explicitly mention “Not Available” if needed)
    
    Format using professional headings and bullet points.
    
    """

    response = llm.invoke(markdown)

    return {
        "markdown_content":response.content
    }

