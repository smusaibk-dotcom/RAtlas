# ==========================================================
# GITHUB TOOL
# ==========================================================

import shutil
import tempfile
from pathlib import Path
from git import Repo


class GitHubTool:
    """
    Tool for interacting with GitHub repositories.

    Performs deterministic operations only.
    All reasoning, planning and fallback decisions
    are handled by the KEE.
    """

    def __init__(self) -> None:
        self._workspace = Path(
            tempfile.mkdtemp(
                prefix="ratlas_github_",
            )
        )

    def extract(
        self,
        repository_url: str,
    ):
        """
        Clone and return the local repository path.
        """

        repository = Repo.clone_from(
            repository_url,
            self._workspace,
        )

        return self._workspace

    def clone_repository(
        self,
        repository_url: str,
    ) -> dict:
        try:
            repository = Repo.clone_from(
                repository_url,
                self._workspace,
            )

            return {
                "success": True,
                "content": self._workspace,
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

    def fetch_file(
        self,
        repository: Path,
        path: str,
    ) -> dict:
        try:
            file = repository / path

            if not file.exists():
                return {
                    "success": True,
                    "content": None,
                    "status_code": None,
                    "error": None,
                }

            return {
                "success": True,
                "content": file.read_text(
                    encoding="utf-8",
                    errors="ignore",
                ),
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

    def fetch_directory(
        self,
        repository: Path,
        path: str,
    ) -> dict:
        try:
            directory = repository / path

            if not directory.exists():
                return {
                    "success": True,
                    "content": [],
                    "status_code": None,
                    "error": None,
                }

            files = []

            for file in directory.rglob("*"):
                if not file.is_file():
                    continue

                try:
                    files.append(
                        {
                            "path": str(
                                file.relative_to(
                                    repository,
                                )
                            ),
                            "extension": file.suffix,
                            "size": file.stat().st_size,
                            "content": file.read_text(
                                encoding="utf-8",
                                errors="ignore",
                            ),
                        }
                    )

                except Exception:
                    files.append(
                        {
                            "path": str(
                                file.relative_to(
                                    repository,
                                )
                            ),
                            "extension": file.suffix,
                            "size": file.stat().st_size,
                            "content": None,
                        }
                    )

            return {
                "success": True,
                "content": files,
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

    def extract_readme(
        self,
        repository: Path,
    ) -> dict:
        try:
            candidates = [
                "README.md",
                "README.rst",
                "README.txt",
                "README",
            ]

            for candidate in candidates:
                readme = repository / candidate

                if readme.exists():
                    return {
                        "success": True,
                        "content": readme.read_text(
                            encoding="utf-8",
                            errors="ignore",
                        ),
                        "status_code": None,
                        "error": None,
                    }

            return {
                "success": True,
                "content": "",
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

    def extract_repository_structure(
        self,
        repository: Path,
    ) -> dict:
        try:
            structure = []

            for path in repository.rglob("*"):
                structure.append(
                    {
                        "path": str(
                            path.relative_to(
                                repository,
                            )
                        ),
                        "type": ("directory" if path.is_dir() else "file"),
                    }
                )

            return {
                "success": True,
                "content": structure,
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

    def extract_code_blocks(
        self,
        repository: Path,
    ) -> dict:
        try:
            files = self.fetch_directory(
                repository,
                "",
            )

            if not files["success"]:
                return files

            code_extensions = {
                ".py",
                ".js",
                ".ts",
                ".tsx",
                ".java",
                ".cpp",
                ".c",
                ".cc",
                ".hpp",
                ".h",
                ".cs",
                ".go",
                ".rs",
                ".rb",
                ".php",
                ".swift",
                ".kt",
                ".scala",
                ".r",
                ".m",
                ".sql",
                ".sh",
                ".yaml",
                ".yml",
                ".toml",
                ".json",
                ".xml",
                ".html",
                ".css",
                ".md",
            }

            code_blocks = []

            for file in files["content"]:
                if file["extension"] in code_extensions and file["content"] is not None:
                    code_blocks.append(
                        {
                            "id": file["path"],
                            "path": file["path"],
                            "language": (file["extension"].lstrip(".")),
                            "content": file["content"],
                            "start_offset": None,
                            "end_offset": None,
                        }
                    )

            return {
                "success": True,
                "content": code_blocks,
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
        shutil.rmtree(
            self._workspace,
            ignore_errors=True,
        )
