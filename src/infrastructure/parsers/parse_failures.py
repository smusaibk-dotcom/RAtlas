from enum import Enum

class ParseFailureType(str, Enum):
    HTTP_403 = "http_403"
    HTTP_404 = "http_404"
    TIMEOUT = "timeout"
    BOT_CHALLENGE = "bot_challenge"
    ACCESS_DENIED = "access_denied"
    LOGIN_REQUIRED = "login_required"
    EMPTY_PAGE = "empty_page"
    NETWORK = "network"
    PARSER = "parser"
    UNKNOWN = "unknown"