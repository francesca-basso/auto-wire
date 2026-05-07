import os, json, re
from pathlib import Path
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

MODEL = os.environ.get("LLM_MODEL", "anthropic/claude-sonnet-4-6")


def call_json(prompt_file: str, **vars) -> dict:
    template = Path(f"prompts/{prompt_file}").read_text()
    prompt = template.format(**vars)

    response = completion(
        model=MODEL,
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.choices[0].message.content.strip()
    text = re.sub(r"^```(?:json)?\n?|\n?```$", "", text, flags=re.M).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        print(f"⚠ Invalid JSON from LLM (model={MODEL}):\n{text}")
        raise