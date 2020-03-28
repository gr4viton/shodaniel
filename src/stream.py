from attr import attrib, attrs
import cv2
from structlog import get_logger
from vidgear.gears import CamGear


@attrs
class Stream:
    name = attrib()
    source = attrib()
    stream_store = attrib()

    font_setup = dict(
        fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA
    )

    frame_count_read = attrib(default=0)
    frame_count_real = attrib(default=0)

    def __attrs_post_init__(self):
        self.log = get_logger(__name__)
        self.log_kwargs = dict(source=self.source)

    def start(self):
        self.log.info("stream.creating")
        stream = CamGear(source=self.source).start()
        self.log.info("stream.created")

        while True:
            frame = stream.read()
            # read frames

            self.frame_count_read += 1

            if frame is None:
                break
            self.frame_count_real += 1

            self.display_hud(frame)
            self.frame = frame

            self.store()

        stream.stop()
        self.log.info("stream.stopped")

    def store(self):
        """Store stream data into stream_store."""
        self.stream_store[self.name] = {"frame": self.frame}

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
