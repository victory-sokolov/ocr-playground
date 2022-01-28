# OCR Playground

[![GitHub Super-Linter](https://github.com/victory-sokolov/ocr-playground/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/marketplace/actions/super-linter)

Comparing few OCR libraries
1. [Tesseract](https://github.com/sirfz/tesserocr)
2. [EasyOCR](https://github.com/JaidedAI/EasyOCR)
3. [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)

Image preprocessing is being done using OpenCV
## Start project

```shell
cd app && ./start.sh
```

## Run inside Docker

```bash
docker run -p 8000:8000 -it --rm ocr-playground
```
