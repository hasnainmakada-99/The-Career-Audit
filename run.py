# in run.py
import uvicorn
import os

if __name__ == "__main__":
    # Render will set the PORT environment variable.
    # We'll use it if it's available, otherwise default to 8000.
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=True)