import random
from structlog import get_logger
from src.crawler import Crawler

log = get_logger(__name__)


class StreamerMixinSource:
    """Streamer methods for stream source acquirance."""
    craw = None

    def load_sources(self):
        # sources = self.sources_from_file()
        self.crawl_sources()

    def select_random_sources(self):
        count = 4
        population = list(self.craw.source_store.values())
        selected_sources = random.sample(population, count)

        return selected_sources

    def crawl_sources(self):
        log.info("streamer.crawling")
        self.craw = Crawler()
        sources = self.craw.get_sources()
        return sources

    def sources_from_file(self):

        formats = ["http://{}/shot.json", "https://{}/shot.json", "http://{}", "https://{}"]
        log.debug("ip_formats", formats=formats)

        form = "rtsp://{ip}:554/live/ch00_0"

        fname = "local/ips.txt"
        with open(fname, "r") as fil:
            txt = fil.read()

        ips = [line for line in txt.split("\n") if line]

        sources = [form.format(ip=ip) for ip in ips]
        return sources


