from fastapi import HTTPException
from google import genai
from google.genai import errors, types

from app.core.config import settings

client = genai.Client(api_key=settings.AI_API_KEY)


def generate_text(
    prompt: str,
    system_instruction: str | None = None,
    temperature: float = 0.7,
    max_output_tokens: int = 1000,
) -> str:
    try:
        response = client.models.generate_content(
            model=settings.AI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=temperature,
                max_output_tokens=max_output_tokens,
            ),
        )
    except errors.APIError as e:
        code = getattr(e, "code", None)
        if code == 429:
            raise HTTPException(status_code=429, detail="AI rate limit reached, try again later")
        if code in (401, 403):
            raise HTTPException(status_code=502, detail="AI service authentication failed")
        raise HTTPException(status_code=502, detail="AI service error")
    except Exception:
        raise HTTPException(status_code=502, detail="Could not reach AI service")

    usage = response.usage_metadata
    if usage:
        print("AI tokens ->", usage.prompt_token_count, usage.candidates_token_count, usage.total_token_count)

    text = (response.text or "").strip()
    if not text:
        raise HTTPException(status_code=502, detail="AI returned an empty response")
    return text