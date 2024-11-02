from unstructured.partition.pdf import partition_pdf

def parse_pdf(file_path: str):
    elements = partition_pdf(filename=file_path)
    content = " ".join([element.text for element in elements if element.text])
    return content
