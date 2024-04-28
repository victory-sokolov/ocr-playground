import os
from typing import Union
from uuid import uuid1

import cv2
import imutils
import numpy as np
from loguru import logger
from redis import Redis
from rq import Queue

from app.recognizers import Recognizer
from app.transform import four_point_transform


class Processor:
    def __init__(self, recognizer: Recognizer) -> None:
        self.recognizer = recognizer

    def pre_process(self, img) -> str:
        # img_cut = self.image_contours(img)
        img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        thresh = cv2.threshold(
            img_gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU,
        )[1]

        # Save resized image
        img_id = str(uuid1())
        img_name = f"{img_id}.jpg"
        img_path = f"app/static/processed/{img_name}"
        # TODO: Use TempFile module to store image and remove it
        cv2.imwrite(img_path, img)

        # temporary processed image to used by OCR engine
        processed_img = f"app/static/processed/temp-{img_id}.jpg"
        cv2.imwrite(processed_img, thresh)

        recognition_result = self.recognizer.recognize(processed_img)
        # remove temp image
        os.remove(processed_img)

        return recognition_result

    def _load_image(self, img_name: str):
        path = f"app/static/{img_name}"
        img = cv2.imread(path)

        if img is None:
            raise FileExistsError(f"Image {path} is not found")

        return img

    def process_list_of_images(self, files: list[str]) -> list:
        recognized_data = []

        for image in files:
            logger.info(f"Processing image {image}")

            img = self._load_image(image)
            recognition_result = self.pre_process(img)
            recognized_data.append({"text": recognition_result})

        return recognized_data

    def process_image_bytes(self, file: bytes) -> str:
        nparr = np.fromstring(file, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        data = self.pre_process(img_np)
        return data

    def process(self, files: Union[list, str, bytes]) -> str:
        if isinstance(files, list):
            self.process_list_of_images(files)
        elif isinstance(files, bytes):
            return self.process_image_bytes(files)
        elif isinstance(files, str):
            image = self._load_image(files)
            return self.pre_process(image)

        raise ValueError(f"Unknown file type: {type(files)}")

    def image_contours(self, image):
        ratio = image.shape[0] / 500.0
        orig = image.copy()
        image = imutils.resize(image, height=500)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        edged = cv2.Canny(gray, 0, 200)

        # find the contours in the edged image, keeping only the
        # largest ones, and initialize the screen contour
        cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

        for cnt in cnts:
            # approximate the contour
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

            if len(approx) == 4:
                screen_cnt = approx
                break

        # show the contour (outline) of the piece of paper
        cv2.drawContours(image, [screen_cnt], -1, (0, 255, 0), 2)
        warped = four_point_transform(orig, screen_cnt.reshape(4, 2) * ratio)
        return warped

    def recognition_queue(self, images):
        queue = Queue(connection=Redis())
        queue.empty()
        queue.enqueue(self.process, args=[images])
