# Fast API OCR Playground

Comparing few OCR libraries

1. [Tesseract](https://github.com/sirfz/tesserocr)
2. [EasyOCR](https://github.com/JaidedAI/EasyOCR)
3. [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)

Image preprocessing is being done using OpenCV

## Start dev

```shell
make dev
```

## Generate SSL certificate to run server over https
```bash
brew install mkcert

mkdir certs && cd certs
mkcert localhost 127.0.0.1 ::1
```

## Run inside Docker

Build Dockerfile `docker build -t ocr-app .`

Run app inside Docker

```bash
docker run -p 8000:8000 -it --rm ocr-app
```

Run with Kubernetes

1. Build Docker image: `docker build -t ocr-app .`
2. Tag the image: `docker tag ocr-app localhost:5000/ocr-app`
3. Start local Docker registry: `docker run -d -p 5000:5000 --restart=always --name registry registry:2`
4. Push image to local registry: `docker push localhost:5000/ocr-app`
5. Apply the Kubernetes deployment config: `kubectl apply -f deployment.yaml`
