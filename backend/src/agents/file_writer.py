from src.state import DDRState
from pathlib import Path


def markdown_writer(state: DDRState):
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    

    user_input = input("Enter the desired filename (e.g., MyReport): ").strip()

    if not user_input:
        user_input = "DDR_Report"

    file_name = output_dir / f"{user_input}.md"

    raw_content = state.get('markdown_content', "")

    if isinstance(raw_content, list):
        first_item = raw_content[0] if len(raw_content) > 0 else ""
        if isinstance(first_item, dict):
            content = first_item.get('text', str(first_item))
        else:
            content = str(first_item)
    
    elif isinstance(raw_content, str):
        content = raw_content

    else:
        content = str(raw_content)
        
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"--- Report successfully saved to {file_name} ---")
    except Exception as e:
        print(f"Failed to write file: {e}")
        return {"file_path": "ERROR"}

    return {"file_path": str(file_name)}