"""Configuration of structlog and code for ad-hoc processors."""

from time import time

import structlog
import structlog_pretty

from src.config import config


def configure_structlog():
    """Set up structlog with one of two predefined config schemes.

    The config scheme is selected based on ``.config.debug``.
    """
    if not config.debug:
        processors = [
            drop_debug_logs,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            unix_timestamper,
            structlog_pretty.NumericRounder(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(),
        ]

    else:
        # add keys from structlog kwargs to these if they should be syntax highlighted / formatted as JSON / XML
        keys_json = ["request_json", "response_json"]
        keys_xml = ["request_xml", "response_xml"]

        syn_xml = {key: "xml" for key in keys_xml}
        syn_json = {key: "json" for key in keys_json}
        syntax_highlighter_dict = {**syn_xml, **syn_json}

        processors = [
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog_pretty.NumericRounder(),
        ]

        if config.structlog_prettify_xml:
            processors.append(structlog_pretty.XMLPrettifier(keys_xml))

        if config.structlog_prettify_json:
            processors.append(structlog_pretty.JSONPrettifier(keys_json))

        processors += [
            structlog_pretty.SyntaxHighlighter(syntax_highlighter_dict),  # has to be after all formaters!
            structlog.processors.TimeStamper('iso'),
            structlog.processors.ExceptionPrettyPrinter(),
            structlog.processors.UnicodeDecoder(),
            structlog.dev.ConsoleRenderer(pad_event=25),
        ]

    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=structlog.threadlocal.wrap_dict(dict),
    )


def unix_timestamper(_, __, event_dict):
    """Add a ``timestamp`` key to the event dict with the current Unix time."""
    event_dict['timestamp'] = time()
    return event_dict


def drop_debug_logs(_, level, event_dict):
    """Drop the event if its level is ``debug``."""
    if level == 'debug':
        raise structlog.DropEvent
    return event_dict
