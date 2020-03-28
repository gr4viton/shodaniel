from glom import glom
import cv2

from structlog import get_logger


log = get_logger(__name__)


class StreamerMixinDisplay:
    """Streamer methods which display images."""

    window_name = "streamer"

    def display_pane(self):
        """Aggregate frames from open streams."""

        names = sorted(self.stream_store.keys())
        frames = []
        for name in names:
            spec = "{name}.output.frame".format(name=name)
            frame = glom(self.stream_store, spec, default=None)
            if frame is None:
                continue
            frames.append(frame)

        if not frames:
            return

        if len(frames) > 1:
            cat = [[frames[0]], frames[1:]]
            pane = self.concat_tile_resize(cat)
        else:
            pane = frames[0]

        cv2.imshow(self.window_name, pane)

    def display_loop(self):

        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)

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
