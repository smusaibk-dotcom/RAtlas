# ==========================================================
# YOUTUBE TOOL
# ==========================================================


import re

import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
import tempfile
from pathlib import Path
from faster_whisper import WhisperModel


class YouTubeTool:
    """
    Tool for interacting with YouTube videos.

    Performs deterministic operations only.
    All reasoning, planning and fallback decisions
    are handled by the KEE.
    """

    def extract(
        self,
        url: str,
    ):
        """
        Extract complete YouTube content.
        """

        info = yt_dlp.YoutubeDL(
            {
                "quiet": True,
                "skip_download": True,
            }
        ).extract_info(
            url,
            download=False,
        )

        return info

    def fetch_video(
        self,
        url: str,
    ) -> dict:
        try:
            options = {
                "quiet": True,
                "skip_download": True,
            }

            with yt_dlp.YoutubeDL(
                options,
            ) as ydl:
                info = ydl.extract_info(
                    url,
                    download=False,
                )

            return {
                "success": True,
                "content": {
                    "id": info.get("id"),
                    "title": info.get("title"),
                    "description": info.get("description"),
                    "channel": info.get("channel"),
                    "uploader": info.get("uploader"),
                    "upload_date": info.get("upload_date"),
                    "duration": info.get("duration"),
                    "view_count": info.get("view_count"),
                    "like_count": info.get("like_count"),
                    "thumbnail": info.get("thumbnail"),
                    "webpage_url": info.get("webpage_url"),
                    "chapters": info.get("chapters"),
                    "tags": info.get("tags"),
                    "categories": info.get("categories"),
                },
                "status_code": None,
                "error": None,
            }

        except Exception as e:
            return {
                "success": False,
                "content": None,
                "status_code": None,
                "error": str(e),
            }

    def extract_transcript(
        self,
        video,
    ) -> dict:
        try:
            video_id = video["id"]

            transcript = YouTubeTranscriptApi().fetch(
                video_id,
            )

            text = "\n".join(segment.text for segment in transcript)

            return {
                "success": True,
                "content": [
                    {
                        "id": f"segment_{i}",
                        "start": segment.start,
                        "duration": segment.duration,
                        "text": segment.text,
                        "start_offset": None,
                        "end_offset": None,
                    }
                    for i, segment in enumerate(
                        transcript,
                        start=1,
                    )
                ],
                "status_code": None,
                "error": None,
            }

        except Exception as e:
            return {
                "success": False,
                "content": "",
                "status_code": None,
                "error": str(e),
            }

    def extract_audio(
        self,
        url: str,
    ) -> dict:
        try:
            with tempfile.TemporaryDirectory() as directory:
                output = str(Path(directory) / "%(id)s.%(ext)s")

                options = {
                    "format": "bestaudio",
                    "outtmpl": output,
                    "quiet": True,
                }

                with yt_dlp.YoutubeDL(
                    options,
                ) as ydl:
                    info = ydl.extract_info(
                        url,
                        download=True,
                    )

                    audio = Path(ydl.prepare_filename(info))

                return {
                    "success": True,
                    "content": audio,
                    "status_code": None,
                    "error": None,
                }

        except Exception as e:
            return {
                "success": False,
                "content": None,
                "status_code": None,
                "error": str(e),
            }

    def transcribe_audio(
        self,
        audio: Path,
    ) -> dict:
        try:
            model = WhisperModel(
                "base",
                device="cpu",
                compute_type="int8",
            )

            segments, _ = model.transcribe(
                str(audio),
            )

            text = "\n".join(segment.text for segment in segments)

            return {
                "success": True,
                "content": text,
                "status_code": None,
                "error": None,
            }

        except Exception as e:
            return {
                "success": False,
                "content": "",
                "status_code": None,
                "error": str(e),
            }

    def extract_metadata(
        self,
        video,
    ) -> dict:
        try:
            metadata = {
                "id": video.get("id"),
                "title": video.get("title"),
                "description": video.get("description"),
                "uploader": video.get("uploader"),
                "channel": video.get("channel"),
                "upload_date": video.get("upload_date"),
                "duration": video.get("duration"),
                "view_count": video.get("view_count"),
                "like_count": video.get("like_count"),
                "tags": video.get("tags"),
                "categories": video.get("categories"),
                "thumbnail": video.get("thumbnail"),
                "webpage_url": video.get("webpage_url"),
            }

            return {
                "success": True,
                "content": metadata,
                "status_code": None,
                "error": None,
            }

        except Exception as e:
            return {
                "success": False,
                "content": {},
                "status_code": None,
                "error": str(e),
            }

    def extract_chapters(
        self,
        video,
    ) -> dict:
        try:
            chapters = video.get(
                "chapters",
            )

            if chapters is None:
                description = video.get("description") or ""

                pattern = r"(\d{1,2}:\d{2}(?::\d{2})?)\s+(.+)"

                chapters = []

                for match in re.finditer(
                    pattern,
                    description,
                ):
                    chapters.append(
                        {
                            "timestamp": match.group(1),
                            "title": match.group(2),
                        }
                    )

            return {
                "success": True,
                "content": chapters or [],
                "status_code": None,
                "error": None,
            }

        except Exception as e:
            return {
                "success": False,
                "content": [],
                "status_code": None,
                "error": str(e),
            }

    def cleanup(
        self,
    ) -> None:
        return
