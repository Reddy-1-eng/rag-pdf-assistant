# Production main.py for Render deployment
import os
import sys

# Add backend directory to Python path
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

# Change to backend directory for relative imports
os.chdir(backend_dir)

# Import and run the FastAPI app
from main import app

if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment (Render sets this)
    port = int(os.environ.get("PORT", 8000))
    
    print(f"Starting RAG application on port {port}")
    
    # Run the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0", 
        port=port,
        reload=False
    )