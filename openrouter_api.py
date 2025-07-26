import requests
import json

def call_openrouter_api(prompt: str, category: str, api_key: str, model: str) -> str:
    system_prompt = f"""You are a professional German interview coach. Generate a comprehensive answer (150-200 words) in German at B1/B2 level for {category} interview questions.

CRITICAL FORMATTING REQUIREMENTS:
1. Write ONLY in German with English translations in parentheses
2. Use HTML color tags for grammatical cases:
   - <span style="color: red;">text</span> = Nominativ (subject)
   - <span style="color: blue;">text</span> = Dativ (indirect object)
   - <span style="color: green;">text</span> = Akkusativ (direct object)
3. Include practical examples and specific details
4. Structure: Introduction + Main points + Conclusion
5. Make it conversational and professional
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
