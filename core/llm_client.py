import urllib.request
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "mistral"


def ask(prompt: str, model: str = DEFAULT_MODEL) -> str:
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
    }).encode("utf-8")

    req = urllib.request.Request(OLLAMA_URL, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")

    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode("utf-8"))
        return result["response"].strip()
