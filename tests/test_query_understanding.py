from infrastructure.adapters.llm_adapter import LLMAdapter
from infrastructure.adapters.query_understanding_adapter import (
    QueryUnderstandingAdapter,
)


def main():
    llm = LLMAdapter()

    adapter = QueryUnderstandingAdapter(llm)

    result = adapter.analyze("How did Transformers evolve?")

    print(result.model_dump_json(indent=4))


if __name__ == "__main__":
    main()
