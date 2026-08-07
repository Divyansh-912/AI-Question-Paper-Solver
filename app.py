from flask import Flask, render_template,request, redirect, url_for, send_from_directory, session, send_file

from ai.pipeline import process_document
from ai.pdf_generator import generate_pdf
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key =os.getenv("SECRET_KEY")

UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
PDF_FOLDER = os.path.join(app.root_path,"generated_pdfs")
TEMP_FOLDER = os.path.join(app.root_path,"temp")

os.makedirs(TEMP_FOLDER, exist_ok=True)

@app.route("/")
def home():
   return render_template("index.html")

# @app.route("/submit", methods=["post"])
# def submit():
#     username = request.form["username"]
#     return f"Hello {username}"


@app.route("/upload" ,methods=["post"])
def upload():
    

    # file.save("QuestionPaperSolver/uploads/" + file.filename)
    try:
        file = request.files["file"]

        image_path=os.path.join(UPLOAD_FOLDER, file.filename)    
        file.save(image_path)

        results = process_document(image_path)

        results_file = (
            file.filename.rsplit(".", 1)[0]
            + "_results.json"
        )

        results_path = os.path.join(
            TEMP_FOLDER,
            results_file
        )

        with open(results_path, "w", encoding="utf-8") as f:
            json.dump(
                results,
                f,
                ensure_ascii=False,
                indent=4
            )

        session["results_file"] = results_file
        session["filename"] = file.filename
        
        print(session)

        return render_template(
            "success.html",
            filename=file.filename,
            results = results
            )


    except Exception as e:

        return render_template(
            "error.html",
            message=str(e)
        )


@app.route("/preview")
def preview():
    sample_results = [
        {
            "number": "Q1",
            "text": "What is encapsulation?",
            "co": "CO1",
            "marks": 6,
            "answer_html": "<h3>Understanding Encapsulation</h3><p>This is a sample answer.</p>"
        }
    ]

    return render_template(
        "success.html",
        filename="sample_question_paper.jpg",
        results=sample_results
    )


@app.route("/upload/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/download-pdf")
def download_pdf():
    print(session)

    results_file =  session.get("results_file")
    results_path = os.path.join(
            TEMP_FOLDER,
            results_file
        )

    with open(results_path, "r", encoding="utf-8") as f:
        results = json.load(f)
        
    filename = session.get("filename")
    pdf_name = filename.rsplit(".", 1)[0] + "_solved.pdf"

    pdf_path = os.path.join(
        PDF_FOLDER,
        pdf_name
    )

    generate_pdf(results,pdf_path)

    return send_file(
        pdf_path,
        as_attachment =  True
    )

if __name__ == "__main__":
    app.run(debug=True)


