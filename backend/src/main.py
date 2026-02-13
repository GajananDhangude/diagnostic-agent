from src.graph import graph


if __name__ == "__main__":
    inputs = {"inspection_pdf_path": "data/Sample_Report.pdf", "thermal_pdf_path": "data/Thermal_Images.pdf"}
    
    
    for output in graph.stream(inputs):
        for key, value in output.items():
            print(f" Node '{key}' has finished execution.")