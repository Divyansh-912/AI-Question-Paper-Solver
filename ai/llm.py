from google import genai
import os
from dotenv import load_dotenv
import markdown

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key = api_key)


def generate_answer(question):
    prompt = f"""
    You are an expert teacher.

    Answer the following question clearly and accurately.
    Use simple language.
    Include examples where appropriate.
    Keep the answer concise.
    Answer in 150-200 words.
    Use headings and bullet points.
    Avoid unnecessary repetition.

    - Leave one blank line before every bullet list.
    - Leave one blank line before every numbered list.
    
    Question:
    {question["text"]}
    """
    try:
        response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
        )
        answer = response.text

        import re

        answer = re.sub(
            r":\s*([*-])\s",
            r":\n\n\1 ",
            answer
        )

        answer_html = markdown.markdown(
            answer, 
            extensions=["extra"]
        )

    except Exception as e:
        answer = f"Unable to generate answer: {e}"

    return{
        "number": question["number"],
        "text": question["text"],
        "marks": question["marks"],
        "co": question["co"],
        "answer_html": answer_html
    }
