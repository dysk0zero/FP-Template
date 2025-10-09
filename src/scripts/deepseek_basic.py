from __future__ import annotations

import os
from typing import Any, Dict, List, TypedDict

import requests
from dotenv import load_dotenv

load_dotenv()


class Message(TypedDict):
    role: str
    content: str


class Choice(TypedDict):
    message: Message


class CompletionResponse(TypedDict):
    choices: List[Choice]


DEEPSEEK_API_KEY: str | None = os.getenv("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    raise RuntimeError("Set DEEPSEEK_API_KEY environment variable")

BASE_URL: str = "https://api.deepseek.com"
ENDPOINT: str = "/chat/completions"
URL: str = BASE_URL + ENDPOINT


def deepseek_chat(
    prompt: str,
    *,
    system: str = "You are a helpful assistant.",
    model: str = "deepseek-chat",
    temperature: float = 0.2,
) -> str:
    """
    Send a prompt to DeepSeek's /chat/completions endpoint and return the reply text.
    """
    headers: Dict[str, str] = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    messages: List[Message] = [
        {"role": "system", "content": system},
        {"role": "user", "content": prompt},
    ]

    payload: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "stream": False,
    }

    response = requests.post(URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()

    data: CompletionResponse = response.json()
    return data["choices"][0]["message"]["content"]


if __name__ == "__main__":
    prompt: str = input("Prompt: ").strip()
    reply: str = deepseek_chat(prompt)
    print("Reply:", reply)
