from src.state import DDRState
from langgraph.graph import StateGraph , START , END
from src.agents.pdf_extractor import pdf_extraction_agent
from src.agents.data_extractor import data_extraction_agent
from src.agents.report_geneerator import report_generation_agent
from src.agents.file_writer import markdown_writer



builder = StateGraph(DDRState)

builder.add_node("pdf_extractor" , pdf_extraction_agent)
builder.add_node("data_extractor" , data_extraction_agent)
builder.add_node("report_generator" , report_generation_agent)
builder.add_node("file_writer" , markdown_writer)

builder.add_edge(START , "pdf_extractor")
builder.add_edge("pdf_extractor" , "data_extractor")
builder.add_edge("data_extractor", "report_generator")
builder.add_edge("report_generator", "file_writer")
builder.add_edge("file_writer" , END)



graph = builder.compile()