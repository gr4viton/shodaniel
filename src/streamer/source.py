import random
from structlog import get_logger
from src.crawler import Crawler
from src.stream.source import StreamSource

log = get_logger(__name__)


class StreamerMixinSource:
    """Streamer methods for stream source acquirance."""
    craw = None

    def load_sources(self):
        self.sources_from_file = self.get_sources_from_file()
        self.crawl_sources()

    def select_random_sources(self):
        # population = list(self.craw.source_store.values())
        population = self.sources_from_file
        count = 3
        if count > len(population):
            count = len(population)

        selected_sources = random.sample(population, count)

        return selected_sources

    def crawl_sources(self):
        log.info("streamer.crawling")
        self.craw = Crawler()
        sources = self.craw.get_sources()
        return sources

    def get_sources_from_file(self):
        fname = "local/ips.txt"
        with open(fname, "r") as fil:
            txt = fil.read()

        ips = txt.split("\n")

        sources = [StreamSource.from_ip(ip) for ip in ips if ip]
        return sources
