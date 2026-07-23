from __future__ import annotations

from collections import Counter
from typing import Iterable

from application.dto.search_result import SearchResult
from application.dto.resource_reference import ResourceReference


class SearchCollector:
    """
    Collects developer statistics from SearchService output.

    This class is ONLY for the Developer Console.

    It MUST NOT be used by production logic.
    """

    @staticmethod
    def collect(
        results: list[SearchResult],
    ) -> dict:
        requested_results = 0
        retrieved_results = 0

        total_response_time = 0.0

        pdf_count = 0
        html_count = 0
        youtube_count = 0
        other_count = 0

        duplicate_count = 0

        provider_counter = Counter()

        seen_urls = set()

        generated_queries = []

        all_resources: list[ResourceReference] = []

        logs = []

        # ---------------------------------------------------
        # Iterate over every SearchResult
        # ---------------------------------------------------

        for result in results:
            generated_queries.append(result.search_query.query)

            requested_results += result.requested_results

            retrieved_results += result.retrieved_results

            total_response_time += result.response_time

            logs.append(
                f"{result.search_query.query} -> "
                f"{result.retrieved_results}/{result.requested_results}"
            )

            for resource in result.resources:
                all_resources.append(resource)

                provider_counter[resource.provider] += 1

                if resource.url in seen_urls:
                    duplicate_count += 1
                else:
                    seen_urls.add(resource.url)

                resource_type = (resource.resource_type or "").strip().lower()

                if resource_type == "pdf":
                    pdf_count += 1

                elif resource_type == "html":
                    html_count += 1

                elif resource_type == "youtube":
                    youtube_count += 1

                else:
                    other_count += 1

        # ---------------------------------------------------
        # Return developer payload
        # ---------------------------------------------------

        return {
            "generated_queries": generated_queries,
            "query_count": len(generated_queries),
            "requested_results": requested_results,
            "retrieved_results": retrieved_results,
            "unique_resources": len(seen_urls),
            "duplicate_resources": duplicate_count,
            "pdf_count": pdf_count,
            "html_count": html_count,
            "youtube_count": youtube_count,
            "other_count": other_count,
            "providers": dict(provider_counter),
            "elapsed_time": round(total_response_time, 3),
            "logs": logs,
            "resources": all_resources,
            "raw_results": results,
        }
