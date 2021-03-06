from time import sleep
from attr import attrib, attrs
import cv2
from structlog import get_logger
from vidgear.gears import CamGear


@attrs
class Stream:
    """


    stream_srore is a shared dict
    each key is accessed by one thread and the main thread
    ```
    stream_store = {
        first_stream_name: {
            "control": {
                "killed": False
            },
            "output": {
                "frame": ...,
                ...
            }
        },
        second_stream_name: {...}
    ```
    """
    name = attrib()
    source = attrib()
    stream_store = attrib()
    interface = attrib(init=False)

    font_setup = dict(
        fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA
    )

    sleep_frame_sec = attrib(default=0.5)
    sleep_idle_sec = attrib(default=1)

    frame_count_read = attrib(default=0)
    frame_count_real = attrib(default=0)

    def __attrs_post_init__(self):
        log_kwargs = dict(url=self.source.url, name=self.name)
        self.log = get_logger(__name__, **log_kwargs)
        self.stream_store[self.name] = {
            "control": {
                "stream": self.source.start_streaming,
                "killed": False,
            },
            "output": {}
        }

    def output_dict(self):
        return {}

    @property
    def output(self):
        stream_dict = self.stream_store.get(self.name)
        if not stream_dict:
            return None
        return stream_dict.get("output")

    @output.setter
    def output(self, value):
        self.stream_store[self.name]["output"] = value

    @property
    def control(self):
        default = {}
        stream_dict = self.stream_store.get(self.name)
        if not stream_dict:
            return default
        return stream_dict.get("control", default)

    @property
    def streaming(self):
        """Streamer sets control.stream to True when the stream should stream."""
        return self.control.get("stream", self.source.start_streaming)

    @property
    def stopped(self):
        """Streamer sets control.stop to True when the stream should end."""
        return self.control.get("stop", False)

    def start(self):
        try:
            self.stream_loop()
        except Exception:
            self.log.exception("stream.unhandled_exception")
        self.kill()

    def kill(self):
        self.control["killed"] = True
        self.log.info("stream.killed")
        # raise SystemExit

    def stream_loop(self):
        self.log.info("stream.creating")
        stream = CamGear(source=self.source.url).start()
        self.log.info("stream.created")

        while not self.stopped:
            if not self.streaming:
                sleep(self.sleep_idle_sec)
                self.log.info("straming_off")
                continue

            frame = stream.read()
            # read frames

            self.frame_count_read += 1

            if frame is None:
                break
            self.frame_count_real += 1

            self.display_hud(frame)
            self.frame = frame

            self.interface.store_output()
            sleep(self.sleep_frame_sec)

        stream.stop()
        self.log.info("stream.stopped")

    def store_output(self):
        """Store stream output into stream_store."""
        self.output = {
            "frame": self.frame
        }

    def display_hud(self, frame):
        fps = "?"
        txt = "name: {name}, fps: {fps}, frame_count={count}".format(
            name=self.name, fps=fps, count=self.frame_count_real
        )
        origin = (42, 42)
        cv2.putText(img=frame, text=txt, org=origin, **self.font_setup)


#     @staticmethod
#     def cam_preview(previewName, camID):

#         cv2.namedWindow(previewName)
#         cam = cv2.VideoCapture(camID)
#         if cam.isOpened():
#             rval, frame = cam.read()
#         else:
#             rval = False

#         while rval:
#             cv2.imshow(previewName, frame)
#             rval, frame = cam.read()
#             key = cv2.waitKey(20)
#             if key == 27:  # exit on ESC
#                 break
#         cv2.destroyWindow(previewName)
