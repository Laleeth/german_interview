import requests
import json

def call_openrouter_api(prompt: str, category: str, api_key: str, model: str) -> str:
    system_prompt = f""" You are a professional German interview coach. Generate a detailed, natural answer (150-200 words) in German at B1/B2 level for {category} interview questions.

IMPORTANT:
1. Write the answer primarily in German.
2. Provide **inline English translations only for hard or uncommon vocabulary words**, immediately after the German word in parentheses.
3. Use HTML color tags for grammatical cases:
   - <span style="color: red;">text</span> = Nominativ (subject)
   - <span style="color: blue;">text</span> = Dativ (indirect object)
   - <span style="color: green;">text</span> = Akkusativ (direct object)
4. Include practical examples and specific details.
5. Structure your answer with an introduction, main points, and a conclusion.
6. Make the tone conversational and professional.

Example: Ich habe <span style="color: green;">ein komplexes (complex)</span> Projekt erfolgreich abgeschlossen.
"""


    user_prompt = f"""Question: {prompt}

# Provide a detailed, professional German answer with color-coded grammatical cases."""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://german-interview-generator.streamlit.app",
        "X-Title": "German Interview Generator"
    }

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 800
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(data), timeout=30)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ Error: {response.status_code} - {response.text}"
