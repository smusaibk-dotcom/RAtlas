from enum import Enum


class ParseFailureType(str, Enum):
    HTTP_403 = "http_403"
    HTTP_404 = "http_404"
    TIMEOUT = "timeout"
    CLOUDFLARE = "cloudflare"
    NETWORK = "network"
    PARSER = "parser"
    UNKNOWN = "unknown"


class ParseErrorClassifier:
    @staticmethod
    def classify(exc: Exception) -> ParseFailureType:
        text = str(exc).lower()

        if "403" in text:
            return ParseFailureType.HTTP_403

        if "404" in text:
            return ParseFailureType.HTTP_404

        if "cloudflare" in text:
            return ParseFailureType.CLOUDFLARE

        if "timeout" in text:
            return ParseFailureType.TIMEOUT

        if "connection" in text:
            return ParseFailureType.NETWORK

        return ParseFailureType.UNKNOWN
