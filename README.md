# auto-wire

CLI that auto-discovers and installs MCP servers from natural-language intent.

## Install

\`\`\`bash
git clone
cd auto-wire
python -m venv venv && source venv/bin/activate
pip install httpx litellm click python-dotenv
echo "LLM_MODEL=groq/llama-3.3-70b-versatile" > .env
echo "GROQ_API_KEY=..." >> .env
\`\`\`

## Use

\`\`\`bash
python auto_wire.py "voglio leggere file dal mio filesystem"
\`\`\`

## Status

search + rank + trust + install. Skill discovery: WIP.
