import sys, json as _json
import click
from scripts.search_registry import search_mcp
from scripts.llm import call_json
from scripts.trust_check import trust_score
from scripts.install_mcp import install_mcp, safe_local_name


@click.command()
@click.argument("intent")
@click.option("--dry-run", is_flag=True)
def main(intent, dry_run):
    print(f"→ Parsing intent: {intent}")
    try:
        kw = call_json("intent_to_keywords.md", intent=intent)
    except Exception as e:
        print(f"✗ Parse failed: {e}")
        return

    print(f"\n→ Searching registry... (q='{kw['search_query']}')")
    try:
        candidates = search_mcp(kw["search_query"], limit=10)
    except Exception as e:
        print(f"✗ Registry error: {e}")
        return

    if not candidates:
        print("✗ No matches.")
        return
    print(f"  {len(candidates)} candidates found")

    candidates_simple = [
        {"name": r["server"]["name"],
         "description": r["server"].get("description", "")}
        for r in candidates
    ]
    ranked = call_json(
        "rank_candidates.md",
        intent=intent,
        candidates_json=_json.dumps(candidates_simple, indent=2),
    )

    if not ranked["recommend"]:
        print(f"✗ No good match. Missing: {ranked.get('missing_capability', '?')}")
        return

    print(f"\n→ To install:")
    to_install = []
    for name in ranked["recommend"]:
        server = next(r for r in candidates if r["server"]["name"] == name)
        score, reason = trust_score(server)
        marker = "✓" if score >= 7 else "⚠"
        print(f"  {marker} {name} [trust={score}/10] {reason}")
        to_install.append(server)

    if dry_run:
        print("\n(dry-run, stopping)")
        return

    if input("\nInstall? [y/N] ").strip().lower() != "y":
        print("Aborted.")
        sys.exit(0)

    print()
    for server in to_install:
        name = server["server"]["name"]
        local = safe_local_name(name)
        print(f"→ Installing {name} as '{local}'...")
        ok, msg = install_mcp(server)
        print(f"  {'✓ Installed' if ok else '✗ Failed: ' + msg}")

    print(f"\nDone. Run `claude mcp list` to verify.")


if __name__ == "__main__":
    main()