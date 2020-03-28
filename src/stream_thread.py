from attr import attrib, attrs
import threading
from src.stream import Stream
from structlog import get_logger

log = get_logger(__name__)


# @attrs
class StreamThread(threading.Thread):
    # source = attrib()

    def __init__(self, name, **init_kwargs):
        threading.Thread.__init__(self)
        self.name = name
        self.init_kwargs = init_kwargs

    def run(self):
        stream = Stream(name=self.name, **self.init_kwargs)
        stream.start()
