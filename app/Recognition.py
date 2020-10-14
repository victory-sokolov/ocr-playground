import cv2
import numpy as np
import pytesseract
from PIL import Image
from tesserocr import OEM, PSM, PyTessBaseAPI

# from redis import Redis
# from rq import Queue


class Recogniser(object):

    def __init__(self, lang: str, image):
        self._lang = lang
        self.image = image

    def recognise(self) -> str:
        kernel = np.ones((2, 2), dtype=np.uint8)

        img = cv2.imread(f'static/{self.image}')
        img = cv2.resize(img, None, fx=1.2, fy=1.2,
                         interpolation=cv2.INTER_CUBIC)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # median = cv2.medianBlur(img_gray, 3)
        thresh = cv2.threshold(
            img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        cv2.imwrite("output.jpg", thresh)
        pl_img = Image.fromarray(thresh)

        with PyTessBaseAPI(lang="lav+eng+ocrb", oem=OEM.LSTM_ONLY) as api:
            api.SetImage(pl_img)
            response = api.GetUTF8Text()

        return response

    # def recognision_queue(self, image):
    #     image_process = ImageProcessing(image)

    #     q = Queue(connection=Redis())

    #     pipeline_job = q.enqueue(image_process.run_pipeline)
    #     q.enqueue(self.recognise, args=(
    #         image), depends_on=pipeline_job)

    #     print(
    #         f"Task {pipeline_job.id} added to queue at {pipeline_job.enqueued_at}. {len(q)} tasks in the queue"
    #     )
