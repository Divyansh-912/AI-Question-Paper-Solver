from paddleocr import PaddleOCR

from ai.preprocess_image import preprocess_for_ocr


print("Loading OCR model....")

ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    enable_mkldnn=False,
    lang="en"
)

print(" OCR model loaded.")


def extract_text_blocks(image_path):


    processed = preprocess_for_ocr(image_path)
    result = ocr.predict(processed)

    blocks = convert_to_blocks(result)
    # blocks = detect_layout(blocks)
    
    return blocks


def convert_to_blocks(result):
    page = result[0]
   
    texts = page["rec_texts"]
    boxes = page["rec_boxes"]
    scores = page["rec_scores"]

    
   
    blocks = [] 
    # print(type(texts))
    # print(type(boxes))
    # print(type(scores))

    # print(texts[0])
    # print(type(boxes))
    # print(boxes.shape)
    # print(type(boxes[0]))
    # print(boxes[0])
    # print(boxes[0].tolist())
    # print(scores[0])
    for text,box,score in zip(texts, boxes, scores):
        
        block = {
        "text": text,
        "box": box.tolist(),
        "x" : box[0],
        "y" : box[1],
        "confidence" : score
        }

        blocks.append(block)
    
    return blocks


# def detect_columns(blocks):
        
#     blocks = sort_blocks_by_x(blocks)
#     gaps = calculate_x_gaps(blocks)
#     large_gaps = find_large_gaps(gaps)

#     return split_into_columns(blocks, large_gaps)







# def detect_layout(blocks):
   

#     header, body = detect_header(blocks)

#     columns  =  detect_columns(body)

#     columns = sort_columns(columns)

#     columns = merge_lines(columns)

#     ordered_blocks = reconstruct_reading_order(header,columns)

#     return ordered_blocks

