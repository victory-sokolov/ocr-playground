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

## Run inside Docker

```bash
docker run -p 8000:8000 -it --rm ocr-playground
```
