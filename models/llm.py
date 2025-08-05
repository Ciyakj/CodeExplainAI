
import openai
from config.config import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY

def query_openai(prompt, mode="detailed"):
    try:
        system_message = "You are a helpful code explanation assistant."
        if mode == "concise":
            prompt = f"Explain briefly: {prompt}"
        else:
            prompt = f"Explain in detail: {prompt}"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error querying OpenAI: {e}]"
