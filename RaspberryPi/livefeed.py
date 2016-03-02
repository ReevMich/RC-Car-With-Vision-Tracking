#!/usr/bin/python

import serial
import SimpleCV
from Queue import Queue
from threading import Thread, Event
from Queue import Queue

def main():
        cam = SimpleCV.Camera()
        image_queue = Queue()

        camera_thread = ImageCaptureThread(cam, image_queue)
        img_display_thread = ImageDisplayThread(image_queue)
        camera_thread.start()
        img_display_thread.start()


class ImageCaptureThread(Thread):
        def __init__(self, camera, img_queue):
                Thread.__init__(self)
                self.cam = camera
                self.img_queue = img_queue
                self.thread_kill_request = Event()

        def run(self):
                while not self.thread_kill_request.is_set():
                        try:
                                img = cam.getImage()
                                self.img_queue.put(img)
                        except self.img_queue.Empty:
                                continue

        def join(self, timeout=None):
                self.thread_kill_request.set()
                super(ImageCaptureThread, self).join(timeout)

class ImageDisplayThread(Thread):
        def __init__(self, img_queue):
                Thread.__init__(self)
                self.img_queue = img_queue
                self.thread_kill_request = Event()

        def run(self):
                while not self.thread_kill_request.is_set():
                        try:
                                img = self.img_queue.get()
                                img.show()
                        except self.img_queue.Empty:
                                continue

        def join(self, timeout=None):
                self.thread_kill_request.set()
                super(ImageDisplayThread, self).join(timeout)


if __name__ == '__main__':
        main()
