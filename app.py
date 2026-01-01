from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from google import genai  # ✅ new official Gemini SDK

# 🔐 Replace this with your Google Gemini API key
client = genai.Client(api_key="AIzaSyDxxxxxxx")

app = Flask(__name__)
CORS(app)  # Enable CORS so frontend can call backend

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.json
        url = data.get("url")
        question = data.get("question")

        if not url or not question:
            return jsonify({"answer": "⚠️ URL or question missing."})

        # Fetch website HTML
        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator=" ", strip=True)

        # Limit text size (Gemini works best with <=12000 chars)
        text = text[:12000]

        # Prepare prompt for AI
        prompt = f"""
Website Content:
{text}

Question:
{question}

Answer based ONLY on the website content.
"""

        # Call Google Gemini API
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        return jsonify({"answer": response.text})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"answer": "⚠️ Error analyzing website. Check backend logs."})

if __name__ == "__main__":
    app.run(debug=True)
