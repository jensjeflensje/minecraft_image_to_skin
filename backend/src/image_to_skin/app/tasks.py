import base64
import io
from typing import Any, Dict, Optional

import requests
from django.conf import settings

from image_to_skin.app.models import GenerationTask
from image_to_skin.app.generation import generate_skin


def call_openai_responses(base64_image: str, prompt: str) -> Dict[str, Any]:
    if not settings.OPENAI_API_KEY:
        raise ValueError('OPENAI_API_KEY is not configured.')

    payload = {
        'model': settings.OPENAI_MODEL,
        'input': [
            {
                'role': 'user',
                'content': [
                    {'type': 'input_text', 'text': prompt},
                    {'type': 'input_image', 'image_url': "data:image/png;base64," + base64_image},
                ],
            }
        ],
    }
    headers = {
        'Authorization': f'Bearer {settings.OPENAI_API_KEY}',
        'Content-Type': 'application/json',
    }

    response = requests.post(
        'https://api.openai.com/v1/responses',
        headers=headers,
        json=payload,
        timeout=60,
    )
    print(response.text)
    response.raise_for_status()
    return response.json()


def _extract_output_image_base64(response_data: Dict[str, Any]) -> Optional[str]:
    for output_item in response_data.get('output', []):
        for content_item in output_item.get('content', []):
            if content_item.get('type') == 'output_image' and content_item.get('image_base64'):
                return content_item['image_base64']
    return None


def _extract_output_text(response_data: Dict[str, Any]) -> Optional[str]:
    for output_item in response_data.get('output', []):
        for content_item in output_item.get('content', []):
            if content_item.get('type') == 'output_text' and content_item.get('text'):
                return content_item['text']
    return None


def process_generation_task(task_id: str) -> None:
    task = GenerationTask.objects.get(pk=task_id)
    base64_input = base64.b64encode(task.input_image).decode('ascii')

    response_data = call_openai_responses(
        base64_image=base64_input,
        prompt=settings.OPENAI_PROMPT,
    )

    output_prompt = _extract_output_text(response_data)
    if not output_prompt:
        return

    print(output_prompt)

    generated_skin = generate_skin(output_prompt)
    buffer = io.BytesIO()
    generated_skin.save(buffer, format='PNG')
    task.output_image = buffer.getvalue()
    task.save(update_fields=['output_image'])
