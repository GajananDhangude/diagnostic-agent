from src.state import DDRState
from src.schema import DDRReport
from src.utils.llm import llm


def data_extraction_agent(state:DDRState) -> DDRState:
    """Extract structured data using Instructor + Pydantic"""

    inspection_text = state['inspection_text']
    thermal_text = state['thermal_text']

    prompt = f"""You are an expert building inspector analyzing property damage reports.

Extract a COMPLETE Detailed Diagnostic Report (DDR) from these documents.

INSPECTION REPORT:
{inspection_text[:8000]}

THERMAL IMAGING REPORT:
{thermal_text[:8000]}

CRITICAL RULES:
1. Extract ONLY facts present in the documents
2. Do NOT invent or assume information
3. If data is missing, include it in missing_information field
4. Match thermal readings to the correct areas
5. Ensure all temperature calculations are accurate
6. Link observations to evidence in root cause analysis
7. Be specific in recommendations (not generic advice)

Populate ALL fields in the DDRReport schema based on the provided text."""

    structured_llm = llm.with_structured_output(DDRReport)

    response = structured_llm.invoke(prompt)

    return {
        "report":response
    }