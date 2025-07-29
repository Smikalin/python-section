from dataclasses import dataclass, field
from itertools import batched
from typing import Iterable, TypeAlias

SomeRemoteData: TypeAlias = int


@dataclass
class Query:
    per_page: int = 3
    page: int = 1


@dataclass
class Page:
    per_page: int = 3
    results: Iterable[SomeRemoteData] = field(default_factory=list)
    next: int | None = None


def request(query: Query) -> Page:
    data = [i for i in range(0, 10)]
    chunks = list(batched(data, query.per_page))
    return Page(
        per_page=query.per_page,
        results=chunks[query.page - 1],
        next=query.page + 1 if query.page < len(chunks) else None,
    )


class RetrieveRemoteData():
    def __init__(self, per_page: int = 3):
        self.per_page = per_page
        self.current_page = 1

    def __iter__(self):
        return self

    def __next__(self):
        query = Query(per_page=self.per_page, page=self.current_page)
        page = request(query)

        if not page.results:
            raise StopIteration

        self.current_page += 1
        return page.results


class Fibo():
    def __init__(self, n: int):
        self.n = n
        self.current = 0
        self.count = 0
        self.prev = 0
        self.prev_prev = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.count >= self.n:
            raise StopIteration

        if self.count == 0:
            result = 0
        elif self.count == 1:
            result = 1
        else:
            result = self.prev + self.prev_prev

        self.prev_prev = self.prev
        self.prev = result
        self.count += 1

        return result
