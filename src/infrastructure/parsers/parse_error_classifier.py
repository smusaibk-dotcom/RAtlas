from infrastructure.parsers.page_validator import InvalidPageException
from infrastructure.parsers.parse_failures import ParseFailureType


class ParseErrorClassifier:
    @staticmethod
    def classify(exc: Exception) -> ParseFailureType:
        if isinstance(exc, InvalidPageException):
            return exc.reason

        text = str(exc).lower()

        if "403" in text:
            return ParseFailureType.HTTP_403

        if "404" in text:
            return ParseFailureType.HTTP_404

        if "timeout" in text:
            return ParseFailureType.TIMEOUT

        if "connection" in text:
            return ParseFailureType.NETWORK

        return ParseFailureType.UNKNOWN
