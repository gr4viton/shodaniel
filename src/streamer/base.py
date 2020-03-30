from attr import attrib, attrs
from src.stream import Stream
from src.streamer.threads import StreamerMixinThreads
from src.streamer.display import StreamerMixinDisplay
from src.streamer.source import StreamerMixinSource
import cv2

from structlog import get_logger

log = get_logger(__name__)


@attrs
class Streamer(StreamerMixinThreads, StreamerMixinSource, StreamerMixinDisplay):

    stream_store = attrib(factory=OrderedDict)
    threads = attrib(factory=list)

    streams = None

    _stream_count = 1

    thread_count_offset = attrib(default=1)

    @property
    def stream_count(self):
        return self._stream_count

    @stream_count.setter
    def stream_count(self, value):
        self._stream_count = value
        # start / stop threads
        # let the threads display

    def move_right(self):
        self.stream_store
        for i in range(self.stream_count):
            selected_sources[i].start_streaming = True

    @property
    def thread_count(self):
        return self._stream_count + self.thread_count_offset

    def __init__(self):
        """

        each StreamThread writes to stream_frames
        key = stream.name
        value = dict(
            frame=opencv_image
            ...
        )
        """

        self.streams = []

    def main(self):

        self.load_sources()

        sources = self.select_random_sources()

        self.threads_append(sources)
        self.threads_start_all()
        self.threads_wait_for_started_thread()

        self.display_loop()

        self.suicide()
        log.info("streamer.end")

    def suicide(self):
        """Close output window."""
        log.info("streamer.suiciding")
        self.threads_kill_all()
        log.info("streamer.windows.destroy_all")
        cv2.destroyAllWindows()

    def stream_simple(self, source):
        try:
            stream = Stream(source=source)
            stream.start()
        except Exception:
            log.exception("stream.exception_raised")
            pass
