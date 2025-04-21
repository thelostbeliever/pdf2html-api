from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
import base64
import tempfile
import subprocess
import os
import uuid

app = FastAPI()

def convert_pdf_to_html(input_pdf_path, output_html_path):
    subprocess.run(["pdf2htmlEX", input_pdf_path, output_html_path], check=True)

@app.post("/convert", response_class=HTMLResponse)
async def convert_pdf(file: UploadFile = File(None), base64_pdf: str = Form(None)):
    # Save uploaded or decoded PDF to temp file
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input.pdf")
        output_path = os.path.join(tmpdir, "output.html")

        if file:
            with open(input_path, "wb") as f:
                f.write(await file.read())
        elif base64_pdf:
            with open(input_path, "wb") as f:
                f.write(base64.b64decode(base64_pdf))
        else:
            return {"error": "Provide either a file or base64_pdf."}

        try:
            convert_pdf_to_html(input_path, output_path)
            with open(output_path, "r", encoding="utf-8") as f:
                html_content = f.read()
            return HTMLResponse(content=html_content)
        except subprocess.CalledProcessError as e:
            return {"error": "Conversion failed", "details": str(e)}

@app.get("/")
def read_root():
    return {"message": "PDF to HTML API is running"}
