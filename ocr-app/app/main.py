import uvicorn
from core.config import config

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8082,
        reload=config.DEBUG,
        ssl_keyfile="./certs/key.pem",
        ssl_certfile="./certs/cert.pem",
    )
