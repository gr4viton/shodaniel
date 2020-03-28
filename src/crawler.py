from attr import attrib, attrs
from structlog import get_logger
from src.config import config
import shodan


log = get_logger(__name__)


@attrs
class Crawler:

    API_KEY = config.shodan_api_key

    sources = attrib(factory=set)

    def __init__(self):
        if not self.API_KEY:
            log.warn("crawler.shodan_api_key.missing")

    def acq_webcams(self):

        query = 'boa "Content-Length: 963" country:"US"'

        ips = None

        try:
            ips = self.get_ips_from_query(query)
        except Exception:
            log.exception("crawler.unhandled_exception")

        return ips

    def get_sources(self):
        ips = self.acq_webcams()

        if ips:
            self.sources.update(ips)
        return self.sources

    def get_ips_from_query(self, query):
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
        ips = []
        for service in matches:
            ip = service['ip_str']
            ips.append(ip)

        return ips
