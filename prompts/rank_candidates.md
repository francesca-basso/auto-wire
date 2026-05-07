Evaluate which MCP servers fit the user's intent.

User intent: {intent}

Candidates:
{candidates_json}

For each, score:
- relevance (0-10): how well it serves the stated intent.
  10 = direct match (canonical official server). 7 = good. 4 = tangential. 0 = irrelevant.
- specificity (0-10): focused single-purpose (high) vs generic kitchen-sink (low).
  Prefer focused servers when relevance is similar.

Trust signals to consider in relevance:
- Namespace prefix indicates publisher: io.github.github/* > io.github.<known-org>/* > random
- Description quality: detailed and specific > generic boilerplate
- Prefer canonical servers (e.g., io.github.github/* for GitHub) over wrappers/forks

Output strict JSON, no preamble, no code fences:
{{
  "ranked": [
    {{"name": "...", "relevance": N, "specificity": N, "reason": "1 sentence"}}
  ],
  "recommend": ["name1", "name2"],
  "skip": ["name3"],
  "missing_capability": "..."
}}

Rules:
- recommend: 1-3 names with relevance >= 7. If none reach 7, return [].
- NEVER recommend a server with relevance < 7
- Sort ranked by relevance desc
- missing_capability: if recommend is empty, what feature was needed but not found