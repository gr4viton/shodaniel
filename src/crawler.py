from shodaniel.src.shodaniel.config import shodan_api_key
import shodan

class Crawler:

    API_KEY = shodan_api_key

    def __init__(self):
        pass

    def acq_webcam(self, count):

        query = 'boa "Content-Length: 963" country:"US"'

        try:
            # Setup the api
            api = shodan.Shodan(self.API_KEY)

            # Perform the search
            result = api.search(query)

            # Loop through the matches and print each IP
            for service in result['matches']:
                print(service['ip_str'])

        except Exception as e:
            print(e)

    def main(self):
        self.acq_webcam(1)
