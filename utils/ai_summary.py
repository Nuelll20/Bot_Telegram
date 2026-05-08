import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def summarize_news(title, description):
    prompt = f"""
    Ringkas berita berikut ke Bahasa Indonesia dengan gaya profesional dan singkat.

    Judul:
    {title}

    Isi:
    {description}

    Format:
    - Maksimal 3 kalimat
    - Mudah dipahami
    - Profesional
    """

    response = model.generate_content(prompt)

    return response.text.strip()