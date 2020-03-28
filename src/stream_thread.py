from attr import attrib, attrs
import threading
from src.stream import Stream
from structlog import get_logger

log = get_logger(__name__)


# @attrs
class StreamThread(threading.Thread):
    # source = attrib()

    def __init__(self, source):
        threading.Thread.__init__(self)
        self.source = source

    def run(self):
        print("Starting " + self.previewName)
        stream = Stream(source=self.source)
        stream.stream_it()

# Create threads as follows
thread1 = CamThread("Camera 1", 0)
thread2 = CamThread("Camera 2", 1)
thread3 = CamThread("Camera 3", 2)

thread1.start()
thread2.start()
thread3.start()
print()
print("Active threads", threading.activeCount())
