import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def summarize_news(title, description):
    try:
        prompt = f"""
        Anda adalah editor berita profesional.

        Ringkas berita berikut ke Bahasa Indonesia.

        Maksimal 2-3 kalimat.
        Gunakan bahasa formal dan profesional.

        Judul:
        {title}

        Isi:
        {description}
        """

        response = model.generate_content(prompt)

        print("=== GEMINI RESPONSE ===")
        print(response.text)

        return response.text.strip()

    except Exception as e:
        print("ERROR GEMINI:", e)
        return description