import uvicorn
from assets.routes import app as api

if __name__ == '__main__':
    uvicorn.run(app=api, host="0.0.0.0", port=8000)
