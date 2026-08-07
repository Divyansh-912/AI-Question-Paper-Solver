import re


def merge_lines(blocks):

    if not blocks:
        return []
    
    merged=[]
    current = blocks[0].copy()

    for block in blocks[1:]:
        y_difference = block["y"] - current["y"]

        if y_difference <= 40:
            current["text"] += " " + block["text"]
            current["y"] = block["y"]
            
           

        else:
            merged.append(current)
            current = block.copy()

    merged.append(current)

    return merged



def detect_questions(paragraphs):

    questions = []

    QUESTION_STARTERS = [
    "Explain",
    "Describe",
    "Discuss",
    "Define",
    "Differentiate",
    "Develop",
    "Write",
    "Illustrate",
    "Compare",
    "What",
    "Why",
    "How"
    ]

    for paragraph in paragraphs:
        text = paragraph["text"].strip()
        normalized = normalize_question_start(text)
        
        if ( 
            re.match(r"^\d+\.", text)
            or
            re.match(r"^Q\.?\d+",text)
            or
            re.match(r"^\(?\d+\)?[.)]", text)
        ):
            questions.append(paragraph)
            continue

        for starter in QUESTION_STARTERS:

            if normalized.startswith(starter):
                questions.append(paragraph)
                break


    return questions


def clean_questions(questions):

    cleaned = []

    for question in questions:


        cleaned.append({
            "number":extract_question_number(question["text"]), "text": normalize_question_start(question["text"])
        } )

    return cleaned

def normalize_question_start(text):
    text = text.strip()
    text = re.sub(r"^Q\.?\s*", "", text)
    text = re.sub(r"^\(?\d+\)?[.)]?\s*", "", text)

    return text

def extract_question_number(text):

    match =re.match(r"^(Q\.?\s*\d+|\(?\d+\)?[.)]?|\d+)", text.strip())

    if match:
        return match.group().strip()

    return ""