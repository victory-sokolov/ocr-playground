import uvicorn

from app.core.config import config

if __name__ == "__main__":
    uvicorn.run(
        "app.app:app",
        host="127.0.0.1",
        port=8082,
        reload=config.DEBUG,
        ssl_keyfile="./certs/key.pem",
        ssl_certfile="./certs/cert.pem",
    )
