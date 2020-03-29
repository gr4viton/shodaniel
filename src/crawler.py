from attr import attrib, attrs
from structlog import get_logger
from src.config import config
from src.stream.source import StreamSource
import shodan


log = get_logger(__name__)


@attrs
class Crawler:

    API_KEY = config.shodan_api_key

    source_store = attrib(factory=dict)

    def __init__(self):
        if not self.API_KEY:
            log.warn("crawler.shodan_api_key.missing")

    def acq_sources(self):

        query = 'boa "Content-Length: 963" country:"US"'

        sources = None

        try:
            sources = self.get_sources_from_query(query)
        except Exception:
            log.exception("crawler.unhandled_exception")

        return sources

    def get_sources(self):
        sources = self.acq_sources()

        if sources:
            source_dict = {source.code: source for source in sources}
            self.source_store.update(source_dict)
        return self.source_store

    def get_sources_from_query(self, query):
        """

        source should have
        - ip
        - name
        - quality etc setting
        - query_time_utc - to deprecate found sources
        """
        api = shodan.Shodan(self.API_KEY)

        result = api.search(query)

        if not result:
            log.error("crawler.empty_result", hint="is shodan_api_key valid?")
            return None

        matches = result['matches']
        log.info("crawler.found_matches", count=len(matches))

        sources = []
        for service in matches:
            source = StreamSource.from_shodan_match(service)
            if not source:
                continue
            sources.append(source)

        return sources
