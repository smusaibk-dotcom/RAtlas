from infrastructure.parsers.parse_failures import ParseFailureType

class InvalidPageException(Exception):
    def __init__(self, reason: ParseFailureType):
        self.reason = reason
        super().__init__(reason.value)


class PageValidator:
    @staticmethod
    def validate(html: str) -> None:
        html = html.lower()

        if not html.strip():
            raise InvalidPageException(ParseFailureType.EMPTY_PAGE)

        if (
            "cloudflare" in html
            or "just a moment" in html
            or "checking your browser" in html
            or "verify you are human" in html
            or "security check" in html
            or "cf-browser-verification" in html
            or "cf-challenge" in html
        ):
            raise InvalidPageException(ParseFailureType.BOT_CHALLENGE)