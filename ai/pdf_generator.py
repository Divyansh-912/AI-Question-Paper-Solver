from reportlab.platypus import(
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem
)

from bs4 import BeautifulSoup

from html.parser import HTMLParser

import xml.etree.ElementTree as ET

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.enums import TA_CENTER

import re


def generate_pdf(results, pdf_path):
    doc = SimpleDocTemplate(
        pdf_path
    )
    styles = getSampleStyleSheet()

    title_style =  styles["Heading1"]

    heading_style = styles["Heading2"]

    body_style = styles["BodyText"]

    title_style.alignment = TA_CENTER

    story = []

    story.append(
        Paragraph(
            "<b>Question Paper Solver</b>",
            title_style
        )
    )

    story.append(
        Paragraph(
            "AI Generated Solutions Report",
            body_style
        )
    )

    story.append(
        Spacer(1, 20)
    )

    for index, question in enumerate(results, start=1):

        story.append(
            Paragraph(
                f"<b>Question {index}</b>",
                heading_style
            )
        )

        story.append(
            Paragraph(
                f"<b>CO:</b> {question['co']} &nbsp;&nbsp;&nbsp;&nbsp; <b>Marks:</b> {question['marks']}",
                body_style
            )
        )

        story.append(
            Spacer(1,8)
        )

        story.append(
            Paragraph(
                "<b>Question</b>",
                body_style
            )
        )

        story.append(
            Paragraph(
                question["text"],
                body_style
            )
        )

        story.append(
            Spacer(1, 10)
        )

        story.append(
            Paragraph(
                "<b>Answer</b>",
                body_style
            )
        )


        render_answer_html(
            story,
            question["answer_html"],
            heading_style,
            body_style
        )
    
        story.append(
            Paragraph(
                "<font color='grey'>________________________________________________________________________________________</font>",
                body_style
            )
        )

        story.append(
            Spacer(1,20)
        )

    doc.build(story)

    return pdf_path


def render_answer_html(story, html, heading_style,body_style):

    root = ET.fromstring(f"<root>{html}</root>")

    for element in root:

        if element.tag == "h3":

            story.append(
                Paragraph(
                    f"<b>{element.text}</b>",
                    heading_style
                )
            )

            story.append(
                Spacer(1, 8)
            )

        elif element.tag == "p":

            text = "".join(element.itertext()).strip()
            text = latex_to_unicode(text)

            if text:

                story.append(
                    Paragraph(
                        text,
                        body_style
                    )
                )

                story.append(
                    Spacer(1, 6)
                )


def latex_to_unicode(text):

    if not text:
        return ""

    replacements = {
        r"\equiv": "≡",
        r"\neq": "≠",
        r"\leq": "≤",
        r"\geq": "≥",
        r"\times": "×",
        r"\cdot": "·",
        r"\phi": "φ",
        r"\theta": "θ",
        r"\alpha": "α",
        r"\beta": "β",
        r"\gamma": "γ",
        r"\lambda": "λ",
        r"\pi": "π",
    }

    text = re.sub(
        r"\^\{([^}]*)\}",
        r"^(\1)",
        text
    )

    text = re.sub(
        r"\\pmod\{([^}]*)\}",
        r"(mod \1)",
        text
    )

    text = text.replace("$", "")

    for latex, symbol in replacements.items():
        text = text.replace(latex, symbol)

    return text 