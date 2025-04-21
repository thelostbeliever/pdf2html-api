from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
import base64
import tempfile
import subprocess
import os
import logging
import traceback
import shutil

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

def convert_pdf_to_html(input_pdf_path, output_html_path):
    result = subprocess.run(
        ["pdf2htmlEX", input_pdf_path, output_html_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"pdf2htmlEX failed:\n{result.stderr}")
    return output_html_path

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    tb = traceback.format_exc()
    logger.error(f"Unhandled exception: {exc}\n{tb}")
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "traceback": tb},
    )

@app.get("/")
def read_root():
    return {"message": "PDF to HTML API is running"}

@app.get("/debug")
def debug():
    return {
        "pdf2htmlEX_installed": shutil.which("pdf2htmlEX"),
    }

@app.post("/convert", response_class=HTMLResponse)
async def convert_pdf(file: UploadFile = File(None), base64_pdf: str = Form(None)):
    logger.info("Received request to /convert")
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input.pdf")
        output_path = os.path.join(tmpdir, "output.html")

        if file:
            logger.info(f"Received file upload: {file.filename}")
            with open(input_path, "wb") as f:
                f.write(await file.read())
        elif base64_pdf:
            logger.info("Received base64_pdf data")
            with open(input_path, "wb") as f:
                f.write(base64.b64decode(base64_pdf))
        else:
            logger.warning("No file or base64_pdf provided")
            return JSONResponse(status_code=400, content={"error": "Provide either a file or base64_pdf."})

        try:
            convert_pdf_to_html(input_path, output_path)
            with open(output_path, "r", encoding="utf-8") as f:
                html_content = f.read()
            return HTMLResponse(content=html_content)
        except Exception as e:
            logger.error(f"Conversion error: {e}")
            raise
