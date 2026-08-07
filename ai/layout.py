import numpy as np
from ai.preprocess_image import preprocess_for_layout

def sort_blocks_by_x(blocks):
        
        # def get_x(block):
        #     return block["x"]
        
        # res = sorted(blocks, key=get_x)
        # return res
        
        blocks = sorted(blocks,key=lambda block: block["x"])

        return blocks


def sort_blocks_by_y(blocks):
    blocks= sorted(blocks, key= lambda block:block["y"])
    return blocks


def calculate_x_gaps(blocks):
        gaps= []
        for block1,block2 in zip(blocks, blocks[1:]):
            gap = block2["x"] - block1["x"]
            res ={
                "gap": gap,
                "from_x": block1["x"],
                "to_x": block2["x"],
            }
            gaps.append(res)
        return gaps


def calculate_y_gaps(blocks):
    gaps = []
    for block1,block2 in zip(blocks, blocks[1:]):
            gap = block2["y"] - block1["y"]
            res ={
                "gap": gap,
                "from_y": block1["y"],
                "to_y": block2["y"],
            }
            gaps.append(res)
    return gaps


def find_large_gaps(gaps):
    large_gaps = []
    threshold = 40

    for gap in gaps:
        if gap["gap"] > threshold:
             large_gaps.append(gap)

    return large_gaps


     
def detect_header(blocks):
    blocks = sort_blocks_by_y(blocks)
    gaps = calculate_y_gaps(blocks)
    large_gaps = find_large_gaps(gaps)

    if not large_gaps:
         return[], blocks
    
    boundary = large_gaps[0]["to_y"]

    header = [] 
    body = []

    for block in blocks:
        if block["y"] < boundary:
              header.append(block)
        else: 
            body.append(block)

    return header,body

# def detect_columns(body):
#     blocks= sort_blocks_by_x(body)
#     gaps = calculate_x_gaps(blocks)
#     large_gaps = find_large_gaps(gaps)

#     if not large_gaps:
#         return body, []
    

#     large_gap = large_gaps[0]
#     boundary = (large_gap["from_x"]+ large_gap["to_x"])/2
    
#     left_column =[]
#     right_column=[]

#     for block in body:
#         if block["x"] < boundary:
#             left_column.append(block)

#         else:
#             right_column.append(block)

#     left_column = sort_blocks_by_y(left_column)
#     right_column = sort_blocks_by_y(right_column)

    # print("LEFT COLUMN")
    # for block in left_column:
    #     print(block["text"])

    # print()

    # print("RIGHT COLUMN")
    # for block in right_column:
    #     print(block["text"])


#     return left_column,right_column




def detect_page_layout(image_path):
    binary = preprocess_for_layout(image_path)

    projection = np.sum(binary,  axis=0)
    threshold = projection.max() * 0.10

    empty_columns = projection < threshold

    start = None 
    gaps = []

    for i, is_empty in enumerate(empty_columns):

        if is_empty and start is None:
            start= i

        elif not is_empty and start is not None:
             gaps.append((start, i -1))
             start = None

    if start is not None:
         gaps.append((start, len(empty_columns)-1))

    if not gaps:
         return {"type":"single"}

    widest_gap = max(gaps, key=lambda gap: gap[1] - gap[0])

    gap_width = widest_gap[1] - widest_gap[0]

    if gap_width > binary.shape[1] *0.08:

        boundary = (widest_gap[0] + widest_gap[1])//2

        return{
             "type": "double",
             "boundary": boundary
        }
    return {"type" : "single"}