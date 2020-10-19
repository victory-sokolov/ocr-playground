import os
import time

import cv2
import numpy as np
from PIL import Image
from redis import Redis
from rq import Queue
from tesserocr import OEM, PSM, PyTessBaseAPI

os.environ["load_system_dawg"] = "0"
os.environ["load_freq_dawg"] = "0"
os.environ["load_punc_dawg"] = "0"


class Recogniser:

    def recognise(self, files):
        recognised_data = []

        if type(files) is not list:
            files = [files]

        for image in files:
            img = cv2.imread(f"static/{image}")
            if img is None:
                raise FileExistsError("Image not found")

            img = cv2.resize(img, None, fx=1.2, fy=1.2,
                             interpolation=cv2.INTER_CUBIC)
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            thresh = cv2.threshold(
                img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

            # cv2.imwrite("output.jpg", thresh)
            result = Image.fromarray(thresh)

            with PyTessBaseAPI(lang="lav+eng+ocrb", oem=OEM.LSTM_ONLY) as api:
                api.SetImage(result)
                response = api.GetUTF8Text()
                recognised_data.append({
                    'image': image,
                    'ocr': response
                })

        return recognised_data

    def recognition_queue(self, images):
        q = Queue(connection=Redis())
        q.empty()
        job = q.enqueue(self.recognise, args=([images]))

        time.sleep(260)
        print(job.result)
