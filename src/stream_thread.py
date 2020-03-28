from attr import attrib, attrs
import threading
from src.stream import Stream
from structlog import get_logger

log = get_logger(__name__)


# @attrs
class StreamThread(threading.Thread):
    # source = attrib()

    def __init__(self, **init_kwargs):
        threading.Thread.__init__(self)
        self.init_kwargs = init_kwargs

    def run(self):
        log.info("stream_thread.starting")
        stream = Stream(**self.init_kwargs)
        stream.start()
