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
