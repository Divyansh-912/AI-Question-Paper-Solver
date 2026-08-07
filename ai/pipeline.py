from ai.layout import detect_page_layout
from ai.image_utils import split_image
from ai.ocr import extract_text_blocks
from ai.parser import merge_lines
from ai.llm import generate_answer
from ai.extractor import extract_questions

def process_document(image_path):
    layout = detect_page_layout(image_path)

    if layout["type"] == "single":
        blocks = extract_text_blocks(image_path)
        blocks = merge_lines(blocks)

    else:
        left_path, right_path = split_image(
            image_path,
            layout["boundary"]
        )

        left_blocks = extract_text_blocks(left_path)
        right_blocks = extract_text_blocks(right_path)

        blocks = left_blocks + right_blocks
        blocks = merge_lines(blocks)

    questions = extract_questions(blocks)    
    results = []

    for question in questions:
        result = generate_answer(question)
        results.append(result)

    return results