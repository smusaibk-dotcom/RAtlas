import re


class TextCleaner:
    _citation_pattern = re.compile(r"\[\s*\d+\s*\]")

    NOISE_HEADINGS = {
        "Header Follow Links",
        "Footer menu",
        "Share This",
        "Stay Connected",
        "Global Voice",
        "Media",
        "Sign Up to Stay Informed",
    }

    _noise_lines = {
        "Skip to main content",
        "Instagram",
        "Facebook",
        "Twitter",
        "TikTok",
        "YouTube",
        "LinkedIn",
    }

    _cta_patterns = (
        re.compile(r"^Find Everything", re.I),
        re.compile(r"^Read More", re.I),
        re.compile(r"^Learn More", re.I),
        re.compile(r"^Click Here", re.I),
        re.compile(r"^Subscribe", re.I),
        re.compile(r"^Share This", re.I),
    )

    def clean(
        self,
        text: str,
    ) -> str:
        text = self._remove_citations(
            text,
        )

        text = self._remove_noise(
            text,
        )

        text = self._normalize_spacing(
            text,
        )

        return text

    def _remove_citations(
        self,
        text: str,
    ) -> str:
        return self._citation_pattern.sub(
            "",
            text,
        )

    def _remove_noise(
        self,
        text: str,
    ) -> str:
        cleaned_lines = []

        for line in text.splitlines():
            line = line.strip()

            if not line:
                continue

            if line in self._noise_lines:
                continue

            if any(pattern.match(line) for pattern in self._cta_patterns):
                continue

            cleaned_lines.append(
                line,
            )

        return "\n".join(
            cleaned_lines,
        )

    def _normalize_spacing(
        self,
        text: str,
    ) -> str:
        text = (
            text.replace(" .", ".")
            .replace(" ,", ",")
            .replace(" :", ":")
            .replace(" ;", ";")
            .replace("( ", "(")
            .replace(" )", ")")
            .replace("[ ", "[")
            .replace(" ]", "]")
        )

        text = " ".join(
            text.split(),
        )

        return text.strip()
