import easyocr

class Recognition:

    def easyocr_recognition(self, filename: str):
        reader = easyocr.Reader(['lv'], gpu=False)
        result = reader.readtext(filename, detail=0)

        return list(
            filter(None, result.split("\n"))
        )




image = "IMG_20200123_175929.jpg"

recognition = Recognition()

result = recognition.easyocr_recognition(image)

print(result)
