# src/ai/ai_deepseek.py
import os
from typing import Dict, Any, Iterable, List, Literal, TypedDict, Optional
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

Role = Literal["system", "user", "assistant"]


class Msg(TypedDict):
    role: Role
    content: str


DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    raise RuntimeError("Missing DEEPSEEK_API_KEY")

BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
TIMEOUT_MS = int(os.getenv("DEEPSEEK_TIMEOUT_MS", "60000"))

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=BASE_URL, timeout=TIMEOUT_MS / 1000)


def chat(
    messages: List[Msg],
    model: Optional[str] = None,
    temperature: float = 0.2,
    max_tokens: int = 1024,
) -> Dict[str, Any]:
    """Simple one-shot chat completion call."""
    res = client.chat.completions.create(
        model=model or MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    ch = res.choices[0]
    return {
        "id": res.id,
        "model": res.model,
        "content": ch.message.content or "",
        "finish_reason": getattr(ch, "finish_reason", "stop"),
        "usage": res.usage,
    }


def chat_stream(
    messages: List[Msg],
    model: Optional[str] = None,
    temperature: float = 0.2,
    max_tokens: int = 1024,
) -> Iterable[str]:
    """Streaming version."""
    stream = client.chat.completions.create(
        model=model or MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
    )
    for part in stream:
        yield part.choices[0].delta.content or ""
