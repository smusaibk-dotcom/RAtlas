import json
import time
from pathlib import Path

import stanza

from application.dto.chunk import Chunk

INPUT_FILE = Path("tests/fixtures/chunks/peta_chunks.json")
OUTPUT_FILE = Path("tests/fixtures/candidate_discovery/stanza_candidates.json")

# Load pipeline once
nlp = stanza.Pipeline(
    lang="en",
    processors="tokenize,pos,lemma,ner,depparse,constituency",
    use_gpu=False,
)


def extract_candidates(text: str):
    doc = nlp(text)

    candidates = []
    seen = set()

    # ---------- Named Entities ----------
    for ent in doc.ents:
        key = ent.text.lower().strip()

        if key in seen:
            continue

        seen.add(key)

        candidates.append(
            {
                "text": ent.text,
                "candidate_type": f"NER:{ent.type}",
                "evidence": ent.text,
            }
        )

    # ---------- Nouns / Proper Nouns ----------
    for sentence in doc.sentences:
        for word in sentence.words:

            if word.upos not in {"NOUN", "PROPN"}:
                continue

            token = word.text.strip()

            if len(token) < 3:
                continue

            key = token.lower()

            if key in seen:
                continue

            seen.add(key)

            candidates.append(
                {
                    "text": token,
                    "candidate_type": word.upos,
                    "evidence": token,
                }
            )

    return candidates


def main():

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        chunk_dicts = json.load(f)

    results = []

    total = len(chunk_dicts)

    print(f"\nProcessing {total} chunks...\n")

    for index, chunk_dict in enumerate(chunk_dicts, start=1):

        chunk = Chunk(**chunk_dict)

        text = chunk.content.get("text", "")
        heading = chunk.content.get("heading", "")

        print("=" * 80)
        print(f"Chunk {index}/{total}")
        print(f"Heading : {heading}")
        print("=" * 80)

        candidates = extract_candidates(text)

        print(f"Candidates Found : {len(candidates)}")

        for c in candidates:
            print(f"{c['candidate_type']:12} {c['text']}")

        results.append(
            {
                "chunk_id": chunk.chunk_id,
                "heading": heading,
                "candidates": candidates,
            }
        )

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(
                results,
                f,
                indent=4,
                ensure_ascii=False,
            )

        if index != total:
            print("\nSleeping 10 seconds...\n")
            time.sleep(10)

    print("\nDone.")


if __name__ == "__main__":
    main()