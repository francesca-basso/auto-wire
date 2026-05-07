You extract searchable keywords from a user intent description.

User intent: {intent}

Output strict JSON, no preamble, no code fences:
{{
  "domain_keywords": ["..."],
  "action_keywords": ["..."],
  "integration_targets": ["..."],
  "search_query": "..."
}}

Rules:
- domain_keywords: 3-5 nouns describing the domain
- action_keywords: 2-3 verbs describing actions
- integration_targets: named services explicitly mentioned

- search_query: EXACTLY ONE WORD. The MCP Registry's full-text search returns ZERO results for most multi-word queries. Single word is mandatory, no exceptions. Pick the most distinctive noun.

WRONG: "github issue"   → returns 0 results
RIGHT: "github"

WRONG: "browser automation"   → returns 0 results
RIGHT: "browser"

WRONG: "postgres database"   → returns fewer results than "postgres"
RIGHT: "postgres"

- Avoid generic verbs: "manage", "handle", "process"
- Prefer concrete nouns over abstract concepts

Examples:

Intent: "I want an agent that monitors GitHub issues and posts critical ones to Slack"
Output:
{{
  "domain_keywords": ["github", "issues", "notifications"],
  "action_keywords": ["monitor", "post"],
  "integration_targets": ["GitHub", "Slack"],
  "search_query": "github issues"
}}

Intent: "esegui query sul mio db postgres"
Output:
{{
  "domain_keywords": ["postgres", "database", "sql"],
  "action_keywords": ["query"],
  "integration_targets": ["PostgreSQL"],
  "search_query": "postgres database"
}}