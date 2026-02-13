# 🏗️ Building Diagnostic Agent (DDR)

An intelligent multi-agent system built with **LangGraph** to automate the generation of Building Diagnostic Reports (DDR). The agent extracts data from inspection and thermal imaging PDFs, performs root cause analysis, and generates professional Markdown reports.

## 🚀 Features

*   **Parallel PDF Extraction**: Concurrent processing of inspection and thermal scan documents to reduce runtime.
*   **Structured Data Analysis**: Uses Pydantic schemas to ensure 100% consistent data extraction.
*   **Automated Reporting**: Converts raw technical data into a high-quality Markdown narrative.
*   **Defensive File IO**: Robust writer node that handles directory creation and prevents common string/list type errors.