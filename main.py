import uvicorn
from assets.routes import app as api

if __name__ == '__main__':
    # or in terminal>
    # uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    uvicorn.run(app=api, host="0.0.0.0", port=8000)
