from attr import attrib, attrs
from src.stream import Stream
import cv2

from structlog import get_logger

log = get_logger(__name__)


@attrs
class Streamer:

    concurent_stream_count = attrib(default=3)
    streams = None

    font_setup = dict(fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)

    def __init__(self):
        self.streams = []


    def main(self):

        formats = ["http://{}/shot.json", "https://{}/shot.json", "http://{}", "https://{}"]

        form = "rtsp://{ip}:554/live/ch00_0"

        fname = "local/ips.txt"
        with open(fname, "r") as fil:
            txt = fil.read()

        ips = txt.split("\n")

        sources = [form.format(ip=ip) for ip in ips]

        for src in sources:
            self.stream_it_safe(src)

        self.suicide()

    def suicide(self):
        """Close output window."""
        self.log.info("windows.destroy_all")
        cv2.destroyAllWindows()

    def stream_it_safe(self, source):
        try:
            stream = Stream(source=source)
            stream.start()
        except Exception:
            log.exception("stream.exception_raised")
            pass

