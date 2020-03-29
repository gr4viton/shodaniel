import random
from structlog import get_logger
from src.crawler import Crawler
from src.stream.source import StreamSource

log = get_logger(__name__)


class StreamerMixinSource:
    """Streamer methods for stream source acquirance."""
    _craw = None

    @property
    def craw(self):
        """Crawler instance."""
        if not self._craw:
            self._craw = Crawler()
        return self._craw

    def load_sources(self):
        # self.craw.queries_search("rtsp")

        self.sources_from_file = self.get_sources_from_file()

        # self.crawl_sources()

    def select_random_sources(self):

        # population = list(self.craw.source_store.values())
        population = self.sources_from_file
        if not population:
            raise RuntimeError("No sources available.")

        count = self.thread_count
        print(type(count))
        if count > len(population):
            count = len(population)

        selected_sources = random.sample(population, count)

        for i in range(self.stream_count):
            selected_sources[i].start_streaming = True

        return selected_sources

    def crawl_sources(self):
        log.info("streamer.crawling")
        sources = self.craw.get_sources()
        return sources

    def get_sources_from_file(self):
        fname = "local/ips.txt"
        with open(fname, "r") as fil:
            txt = fil.read()

        ips = txt.split("\n")

        sources = [StreamSource.from_ip(ip) for ip in ips if ip]
        return sources

    def options(self):
        """

        # options
        stream
            count
            type
                camera
                    rtsp
                    http
                    ...
                display
                    desktop
                    terminal
            origin
                location
                    near
                    city
                    state
        video
            features - has / has not filtering
                color
                    grayscale
                    dark
                    grayish
                    bright_light
                dynamic
                    movement
                weather
                    blue_sky
                    foggy
                contains
                    letters
                    object = detect object in scene (futureeee)
                        car
                        people
                        3d printer
                        room
                        house
                        ...
            convert
                rotate
                    left
                    right
                    upside_down
                flip
                    left_right
                    up_down
                transform
                    fisheye
                color
                    to_grayscale - make colored images grayscale

        """
        pass
