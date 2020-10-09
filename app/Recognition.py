import cv2
import numpy as np
import pytesseract

# from redis import Redis
# from rq import Queue


class Recogniser(object):

    def __init__(self, lang: str, image):
        self._lang = lang
        self.image = image

    def recognise(self) -> str:
        img_cv = cv2.imread(f'static/{self.image}')
        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        blur = cv2.GaussianBlur(img_rgb, (5, 5), 0)
        thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)[1]

        cv2.imwrite("output.jpg", thresh)
        config = (f"-l {self._lang} --oem 1 --psm 7")
        result = pytesseract.image_to_string(thresh, config=config)
        print(result)
        return result

    # def recognision_queue(self, image):
    #     image_process = ImageProcessing(image)

    #     q = Queue(connection=Redis())

    #     pipeline_job = q.enqueue(image_process.run_pipeline)
    #     q.enqueue(self.recognise, args=(
    #         image), depends_on=pipeline_job)

    #     print(
    #         f"Task {pipeline_job.id} added to queue at {pipeline_job.enqueued_at}. {len(q)} tasks in the queue"
    #     )
