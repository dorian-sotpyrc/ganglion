from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SearchResult:
    path: str
    score: int
    snippet: str


class ArchiveSearch:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)

    def search(self, query: str, limit: int = 5) -> list[SearchResult]:
        words = [w.lower() for w in query.split() if w.strip()]
        results: list[SearchResult] = []

        if not self.root.exists():
            return results

        for path in self.root.rglob("*"):
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except Exception:
                continue

            lower = text.lower()
            score = sum(lower.count(w) for w in words)
            if score > 0:
                snippet = text[:180].replace("\n", " ").strip()
                results.append(
                    SearchResult(
                        path=str(path),
                        score=score,
                        snippet=snippet,
                    )
                )

        results.sort(key=lambda r: (-r.score, r.path))
        return results[:limit]
