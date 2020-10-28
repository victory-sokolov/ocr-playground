import os
import time
import uuid

import cv2
import imutils
import numpy as np
from PIL import Image
from redis import Redis
from rq import Queue
from tesserocr import OEM, PSM, PyTessBaseAPI

from transform import four_point_transform

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

            img_cut = self.image_contours(img)

            img = cv2.resize(img, None, fx=1.2, fy=1.2,
                             interpolation=cv2.INTER_CUBIC)
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            thresh = cv2.threshold(
                img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


            img_name = f"{uuid.uuid1()}.jpg"
            cv2.imwrite(f"static/{img_name}", img_cut)

            result = Image.fromarray(thresh)

            with PyTessBaseAPI(lang="lav+eng+ocrb", oem=OEM.LSTM_ONLY) as api:
                api.SetImage(result)
                response = api.GetUTF8Text()
                recognised_data.append({
                    'image': img_name,
                    'ocr': response
                })

        return recognised_data

    def image_contours(self, image):
        ratio = image.shape[0] / 500.0
        orig = image.copy()
        image = imutils.resize(image, height=500)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        edged = cv2.Canny(gray, 0, 200)

        # find the contours in the edged image, keeping only the
        # largest ones, and initialize the screen contour
        cnts = cv2.findContours(
            edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            if len(approx) == 4:
                screenCnt = approx
                break

        # show the contour (outline) of the piece of paper
        cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
        warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
        return warped

    def recognition_queue(self, images):
        q = Queue(connection=Redis())
        q.empty()
        job = q.enqueue(self.recognise, args=([images]))

        time.sleep(260)
        print(job.result)
