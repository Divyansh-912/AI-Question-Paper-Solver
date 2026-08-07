from google import genai
from dotenv import load_dotenv
import os 
import json

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def extract_questions(blocks):

    text = "\n".join(block["text"] for block in blocks)

    prompt =prompt = f"""
        You are an expert at reading university examination papers from OCR text.

        The OCR text may contain:
        - OCR mistakes
        - Broken line breaks
        - Headers and footers
        - College name
        - Subject name
        - Instructions
        - Page numbers
        - CO codes
        - Marks
        - Optional questions (OR)

        Your task is to extract ONLY the exam questions.

        Instructions:

        1. Ignore:
        - college/university names
        - department names
        - subject titles
        - instructions
        - page numbers
        - decorative text

        2. Preserve every question in the same order as the paper.

        3. If a question has marks, extract them.

        4. If a question has a CO code, extract it.

        5. If questions belong to an OR section, preserve both questions.

        6. Merge broken OCR lines into one complete question.

        7. Do NOT answer the questions.

        Return ONLY valid JSON.

        The JSON format must be:

        [
            {{
                "number": "Q1",
                "text": "Question text...",
                "marks": 6,
                "co": "CO1"
            }}
        ]

        If a field is missing, use null.

        OCR Text:

        {text}
    """

    response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=prompt
    )

    response_text = response.text.strip()

    if response_text.startswith("```"):
        response_text = response_text.replace("```json", "").replace("```", "").strip()

    questions = json.loads(response_text)
    return questions