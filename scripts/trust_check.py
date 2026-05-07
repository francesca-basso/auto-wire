import json
from pathlib import Path

TRUSTED = json.loads(Path("data/trusted_namespaces.json").read_text())


def trust_score(server: dict) -> tuple[int, str]:
    name = server["server"]["name"]
    parts = name.split("/")
    namespace = "/".join(parts[:-1]) if len(parts) > 1 else name

    if namespace in TRUSTED:
        return TRUSTED[namespace], f"verified: {namespace}"
    return 3, f"unknown publisher: {namespace} — REVIEW MANUALLY"