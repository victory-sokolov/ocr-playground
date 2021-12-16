import cv2
import imutils
import os
from uuid import uuid1
from redis import Redis
from rq import Queue

from config import config
from transform import four_point_transform
from recognizers import Recognizer

config_name = config['development']

class Processor:

    def __init__(self, recognizer: Recognizer) -> None:
        self.recognizer = recognizer

    def process(self, files):
        recognised_data = []

        if type(files) is not list:
            files = [files]

        for image in files:
            img = cv2.imread(f"static/{image}")

            if img is None:
                raise FileExistsError("Image not found")

            # img_cut = self.image_contours(img)

            img = cv2.resize(img, None, fx=1.2, fy=1.2,
                             interpolation=cv2.INTER_CUBIC)
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            thresh = cv2.threshold(
                img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )[1]

            # Save resized image
            img_name = f"{str(uuid1())}.jpg"
            img_path = f"static/processed/{img_name}"
            cv2.imwrite(img_path, img)

            # temporary processed image to used by OCR engine
            processed_img = f"static/temp-{str(uuid1)}.jpg"
            cv2.imwrite(processed_img, thresh)

            recognition_result = self.recognizer.recognize(processed_img)
            recognised_data.append({
                'image': img_name,
                'text': recognition_result
            })

            # remove temp image
            # ToDo: Refactor use Context manager
            os.remove(processed_img)

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
        job = q.enqueue(self.process, args=([images]))

        print(job.result)
