from __future__ import annotations

import os

from groq import Groq


DEFAULT_MODEL = "llama-3.1-8b-instant"


def run_groq_completion(prompt: str, model: str | None = None) -> str:
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set.")

    selected_model = model or os.getenv("GROQ_MODEL", "").strip() or DEFAULT_MODEL
    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model=selected_model,
        temperature=0.1,
        messages=[
            {
                "role": "system",
                "content": "Return only JSON that matches the required schema.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    text = completion.choices[0].message.content
    if not text:
        raise RuntimeError("Groq returned an empty response.")
    return text

