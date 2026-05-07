import httpx
from urllib.parse import quote

REGISTRY = "https://registry.modelcontextprotocol.io"


def search_mcp(query: str, limit: int = 10, _retry: bool = False) -> list[dict]:
    r = httpx.get(
        f"{REGISTRY}/v0/servers",
        params={"search": query, "limit": limit * 3},
        timeout=10,
    )
    r.raise_for_status()
    servers = r.json().get("servers", [])

    latest = [
        s for s in servers
        if s.get("_meta", {})
            .get("io.modelcontextprotocol.registry/official", {})
            .get("isLatest") is True
    ]

    seen, unique = set(), []
    for s in latest:
        name = s["server"]["name"]
        if name not in seen:
            seen.add(name)
            unique.append(s)

    # Fallback: se vuoto e la query ha più parole, riprova con la prima parola
    if not unique and " " in query and not _retry:
        first_word = query.split()[0]
        print(f"  (no results for '{query}', retrying with '{first_word}')")
        return search_mcp(first_word, limit, _retry=True)

    return unique[:limit]