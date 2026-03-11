# backend/app/ai/ollama_client.py
"""
Ollama API Client.
Handles all communication with the locally running Ollama server.
"""

import httpx
from typing import Optional
from app.config import settings


class OllamaClient:
    """
    Client for interacting with Ollama API.
    """

    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
        self.timeout = 300.0  # 5 minutes timeout

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate a response from the AI model.
        """
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_predict": 200,  # Shorter response = faster
                    "num_ctx": 1024,     # Smaller context = less RAM
                }
            }

            if system_prompt:
                payload["system"] = system_prompt

            print(f"[OLLAMA] Sending request to {self.model}...")

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json=payload
                )

                if response.status_code == 200:
                    result = response.json()
                    text = result.get("response", "No response generated.")
                    print(f"[OLLAMA] Response received ({len(text)} chars)")
                    return text
                else:
                    print(f"[OLLAMA] Error: Status {response.status_code}")
                    return f"AI model returned error (status {response.status_code})."

        except httpx.ConnectError:
            print("[OLLAMA] Cannot connect to Ollama")
            return "Cannot connect to Ollama. Please start Ollama by running 'ollama serve' in a terminal."
        except httpx.TimeoutException:
            print("[OLLAMA] Timeout - falling back to rule-based")
            return "TIMEOUT"
        except Exception as e:
            print(f"[OLLAMA] Unexpected error: {e}")
            return f"AI error: {str(e)}"

    async def chat(self, messages: list, system_prompt: Optional[str] = None) -> str:
        """
        Have a multi-turn conversation with the AI model.
        """
        try:
            ollama_messages = []

            if system_prompt:
                ollama_messages.append({
                    "role": "system",
                    "content": system_prompt[:500]  # Limit system prompt size
                })

            # Only send last 4 messages for context (saves memory)
            recent = messages[-4:] if len(messages) > 4 else messages
            for msg in recent:
                ollama_messages.append({
                    "role": msg["role"],
                    "content": msg["content"][:500]  # Limit each message
                })

            payload = {
                "model": self.model,
                "messages": ollama_messages,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_predict": 250,  # Shorter = faster
                    "num_ctx": 1024,
                }
            }

            print(f"[OLLAMA] Chat request with {len(ollama_messages)} messages...")

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json=payload
                )

                if response.status_code == 200:
                    result = response.json()
                    text = result.get("message", {}).get("content", "No response generated.")
                    print(f"[OLLAMA] Chat response received ({len(text)} chars)")
                    return text
                else:
                    return f"AI model returned error (status {response.status_code})."

        except httpx.ConnectError:
            return "Cannot connect to Ollama. Please start Ollama by running 'ollama serve' in a terminal."
        except httpx.TimeoutException:
            return "TIMEOUT"
        except Exception as e:
            return f"AI error: {str(e)}"

    async def is_available(self) -> bool:
        """Check if Ollama is running and the model is available."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                if response.status_code == 200:
                    models = response.json().get("models", [])
                    model_names = [m["name"] for m in models]
                    is_found = any(self.model in name for name in model_names)
                    print(f"[OLLAMA] Available models: {model_names}, looking for: {self.model}, found: {is_found}")
                    return is_found
                return False
        except Exception:
            return False


# Singleton instance
ollama_client = OllamaClient()