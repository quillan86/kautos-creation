from anthropic import Anthropic
from src.backend.constants import ANTHROPIC_API_KEY, MODEL_NAME


class LLM:
    def __init__(self):
        self.model_name = MODEL_NAME
        self.client = Anthropic(api_key=ANTHROPIC_API_KEY)

    def generate(self, system_prompt: str, user_prompt: str, tools: list[dict] = None, tool_choice: str | None = None, temperature: float = 0.0) -> str:

        message = self.client.messages.create(
            max_tokens=4096,
            model=self.model_name,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
            temperature=temperature,
            tools=tools,
            tool_choice={"type": "tool", "name": tool_choice} if tool_choice else None
        )
        return message.content[0].input
