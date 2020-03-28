import os


class Config:
    structlog_prettify_xml = bool(os.getenv("STRUCTLOG_PRETTIFY_XML", None))
    structlog_prettify_json = bool(os.getenv("STRUCTLOG_PRETTIFY_JSON", None))

    app_name = os.getenv('APP_NAME', 'shodaniel')
    debug = True
    shodan_api_key = os.getenv("SHODAN_API_KEY", None)


config = Config()
