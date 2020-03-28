import threading
from src.stream_thread import StreamThread
from attr import attrib, attrs
from src.stream import Stream
import cv2

from structlog import get_logger

log = get_logger(__name__)


@attrs
class Streamer:

    stream_store = attrib(factory=dict)
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

    def main(self):

        formats = ["http://{}/shot.json", "https://{}/shot.json", "http://{}", "https://{}"]

        form = "rtsp://{ip}:554/live/ch00_0"

        fname = "local/ips.txt"
        with open(fname, "r") as fil:
            txt = fil.read()

        ips = txt.split("\n")

        sources = [form.format(ip=ip) for ip in ips]

        # for index, src in enumerate(sources):
        #     # self.stream_it_safe(src)
        #     self.stream_via_thread(index, src)

        src = sources[1]
        self.stream_via_thread(1, src)
        self.stream_via_thread(2, src)

        self.display_loop()

        self.suicide()
        log.info("streamer.end")

    def display_pane(self):
        """Aggregate frames from open streams."""

        names = sorted(self.stream_store.keys())
        frames = [self.stream_store[name].get("frame") for name in names]

        if not frames:
            return

        if len(frames) > 1:
            cat = [[frames[0]], frames[1:]]
            pane = self.concat_tile_resize(cat)
        else:
            pane = frames[0]

        name = "streamer"
        cv2.imshow(name, pane)

    @classmethod
    def concat_tile_resize(cls, im_list_2d, interpolation=cv2.INTER_CUBIC):
        im_list_v = [cls.hconcat_resize_min(im_list_h, interpolation=cv2.INTER_CUBIC) for im_list_h in im_list_2d]
        return cls.vconcat_resize_min(im_list_v, interpolation=cv2.INTER_CUBIC)

    @classmethod
    def vconcat_resize_min(cls, im_list, interpolation=cv2.INTER_CUBIC):
        w_min = min(im.shape[1] for im in im_list)
        im_list_resize = [
            cv2.resize(im, (w_min, int(im.shape[0] * w_min / im.shape[1])), interpolation=interpolation)
            for im in im_list
        ]
        return cv2.vconcat(im_list_resize)

    @classmethod
    def hconcat_resize_min(cls, im_list, interpolation=cv2.INTER_CUBIC):
        h_min = min(im.shape[0] for im in im_list)
        im_list_resize = [
            cv2.resize(im, (int(im.shape[1] * h_min / im.shape[0]), h_min), interpolation=interpolation)
            for im in im_list
        ]
        return cv2.hconcat(im_list_resize)

    def display_loop(self):

        # frame_max = 3
        # frame_max = 1000
        while True:
            self.display_pane()

            # enough_frames = i_frame > frame_max
            pressed_q = self.is_key("q")
            # to_end = pressed_q or enough_frames
            to_end = pressed_q
            if to_end:
                break

    def is_key(self, letter):
        key = cv2.waitKey(self.wait_time_ms) & 0xFF
        return key == ord(letter)

    def suicide(self):
        """Close output window."""
        log.info("windows.destroy_all")
        cv2.destroyAllWindows()

    def stream_via_thread(self, index, source):
        name = "stream{index}".format(index=index)
        thread = StreamThread(stream_store=self.stream_store, name=name, source=source)
        thread.start()

        count = threading.activeCount()
        log.info("thread.active", count=count)

    def stream_it_safe(self, source):
        try:
            stream = Stream(source=source)
            stream.start()
        except Exception:
            log.exception("stream.exception_raised")
            pass
