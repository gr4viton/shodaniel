from attr import attrib, attrs
import cv2
from structlog import get_logger
from vidgear.gears import CamGear


@attrs
class Stream:
    source = attrib()

    font_setup = dict(fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)

    def __attrs_post_init__(self):
        self.log = get_logger(__name__)
        self.log_kwargs = dict(source=self.source)

    def start(self):
        self.log.info("stream.creating")
        stream = CamGear(source=self.source).start()
        self.log.info("stream.created")

        frame_max = 1000
        i_frame = 0
        while True:
            frame = stream.read()
            # read frames

            i_frame += 1

            if frame is None:
                break

            self.show_hud(frame)
            cv2.imshow("frame", frame)

            enough_frames = i_frame > frame_max
            pressed_q = self.is_key("q")
            to_end = pressed_q or enough_frames
            if to_end:
                break

        stream.stop()
        self.log.info("stream.stopped")

    def is_key(self, letter):
        key = cv2.waitKey(1) & 0xFF
        return key == ord(letter)

    def show_hud(self, frame):
        txt = "ip: ?"
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


