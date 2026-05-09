# RAG PDF Assistant

AI-powered PDF question answering system using Google Gemini and LangChain.

## Features

- Upload and process PDF documents
- Ask questions about your documents
- Get AI-powered answers with source citations
- Web-based chat interface

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
# Create .env file with:
GOOGLE_API_KEY=your_google_api_key_here
```

3. Run the application:
```bash
python main.py
```

4. Open http://localhost:8000

## Deployment

This application is configured for deployment on Render.com with the included `render.yaml` configuration.

## Environment Variables

- `GOOGLE_API_KEY`: Your Google Gemini API key (required)
- `PORT`: Server port (automatically set by Render)

## API Endpoints

- `GET /`: Web interface
- `POST /ask`: Submit questions
- `GET /process-pdfs`: Process uploaded PDFs
- `GET /health`: Health check