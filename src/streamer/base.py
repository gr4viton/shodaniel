from attr import attrib, attrs
from src.stream import Stream
from src.streamer.threads import StreamerMixinThreads
from src.streamer.display import StreamerMixinDisplay
import cv2

from structlog import get_logger

log = get_logger(__name__)


@attrs
class Streamer(StreamerMixinThreads, StreamerMixinDisplay):

    stream_store = attrib(factory=dict)
    threads = attrib(factory=list)
    concurent_stream_count = attrib(default=3)

    streams = None
    wait_time_ms = 30

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

    def load_sources(self):

        formats = ["http://{}/shot.json", "https://{}/shot.json", "http://{}", "https://{}"]

        form = "rtsp://{ip}:554/live/ch00_0"

        fname = "local/ips.txt"
        with open(fname, "r") as fil:
            txt = fil.read()

        ips = [line for line in txt.split("\n") if line]

        sources = [form.format(ip=ip) for ip in ips]
        return sources

    def main(self):

        sources = self.load_sources()

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
