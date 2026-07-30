import json
import time
from pathlib import Path

from application.agents.candidate_discovery_agent import CandidateDiscoveryAgent
from application.dto.chunk import Chunk


INPUT_FILE = Path("tests/fixtures/chunks/peta_chunks.json")
OUTPUT_FILE = Path("tests/fixtures/candidate_discovery/candidates.json")


def main():

    agent = CandidateDiscoveryAgent()

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        chunk_dicts = json.load(f)

    results = []

    total = len(chunk_dicts)

    print(f"\nFound {total} chunks.\n")

    for index, chunk_dict in enumerate(chunk_dicts, start=1):

        chunk = Chunk(**chunk_dict)

        print("=" * 100)
        print(f"Chunk {index}/{total}")
        print(f"Chunk ID      : {chunk.chunk_id}")
        print(f"Heading       : {chunk.content['heading']}")
        print(f"Characters    : {len(chunk.content['text'])}")
        print("=" * 100)

        try:

            response = agent.run(chunk)

            print(f"\nCandidates Found : {len(response.candidates)}\n")

            for candidate in response.candidates:
                print(f"- {candidate.text} ({candidate.candidate_type})")

            results.append(
                {
                    "chunk_id": chunk.chunk_id,
                    "heading": chunk.content["heading"],
                    "candidates": [
                        candidate.model_dump()
                        for candidate in response.candidates
                    ],
                }
            )

            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(
                    results,
                    f,
                    indent=4,
                    ensure_ascii=False,
                )

        except Exception as e:
            print(f"\nERROR:\n{e}")

        if index != total:
            print("\nSleeping for 10 seconds...\n")
            time.sleep(10)

    print("\nDone.")
    print(f"Processed {total} chunks.")
    print(f"Saved results to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()