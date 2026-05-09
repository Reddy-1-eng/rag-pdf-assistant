# Backend main application file - FastAPI Web Server
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from rag import process_pdf, ask_question

# Get absolute paths for production
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")
UPLOADED_FILES_DIR = os.path.join(SCRIPT_DIR, "uploaded_files")

app = FastAPI(title="RAG PDF Assistant", description="AI-powered PDF question answering system")

# Serve static files (frontend)
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

class QuestionRequest(BaseModel):
    question: str

@app.get("/")
async def read_root():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.post("/ask")
async def ask_question_endpoint(request: QuestionRequest):
    try:
        response = ask_question(request.question)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/process-pdfs")
async def process_pdfs():
    try:
        results = []
        
        if os.path.exists(UPLOADED_FILES_DIR):
            for filename in os.listdir(UPLOADED_FILES_DIR):
                if filename.endswith(".pdf"):
                    pdf_path = os.path.join(UPLOADED_FILES_DIR, filename)
                    result = process_pdf(pdf_path)
                    results.append(f"{filename}: {result}")
        
        return {"message": "PDFs processed successfully", "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "RAG PDF Assistant is running"}

# Process PDFs on startup
@app.on_event("startup")
async def startup_event():
    print("Processing PDFs on startup...")
    try:
        if os.path.exists(UPLOADED_FILES_DIR):
            for filename in os.listdir(UPLOADED_FILES_DIR):
                if filename.endswith(".pdf"):
                    pdf_path = os.path.join(UPLOADED_FILES_DIR, filename)
                    result = process_pdf(pdf_path)
                    print(f"Processed {filename}: {result}")
    except Exception as e:
        print(f"Error processing PDFs: {e}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting RAG Web Application on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
