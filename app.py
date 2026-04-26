import os

from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai
from dotenv import load_dotenv


# 🔐 Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# 🔑 Get API key from .env
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in .env file")

client = genai.Client(api_key=api_key)


PROFILE_CONTEXT = """
I am a BTech Information Technology student focused on building practical AI-powered products.

I work at the intersection of Artificial Intelligence and web development, creating real-world solutions rather than just academic projects.

My work includes:
- AI systems for accessibility (autism prediction, sign language to text and speech)
- Tools that improve communication and productivity

I combine technical skills with creativity through writing and content creation.

I am currently preparing for high-quality software engineering roles (10 LPA+) while also aiming to build original AI-based products.

I value learning from experienced engineers and building meaningful, impactful technology.

LinkedIn:
https://www.linkedin.com/in/akshara-addagoda/
"""


@app.route("/")
def home():
    return "Backend is running 🚀"


@app.route("/generate", methods=["POST"])
def generate_message():
    data = request.get_json(silent=True) or {}

    role = data.get("role", "").strip()
    company = data.get("company", "").strip()
    tone = data.get("tone", "Friendly").strip()
    target_type = data.get("type", "engineer").strip().lower()

    if not role or not company:
        return jsonify({"error": "Role and company are required."}), 400

    if tone not in ["Formal", "Friendly", "Confident"]:
        tone = "Friendly"

    # 🔥 Company personalization
    company_hint = f"{company} is known for innovation and building impactful products at scale."

    prompt = f"""
Write a highly personalized LinkedIn connection message.

About me:
{PROFILE_CONTEXT}

Target:
- Role: {role}
- Company: {company}
- Tone: {tone}
- Target Person Type: {target_type}

Company context:
{company_hint}

Instructions:
- Keep it under 80 words.
- Start naturally (no placeholders like [Name]).
- Sound human, not AI-generated.
- Show curiosity and intent to learn.
- Subtly highlight my work in AI + real-world projects.
- Adapt based on who I'm reaching out to:
  - recruiter → focus on role fit and enthusiasm
  - engineer → focus on learning and technical curiosity
  - founder → focus on building and impact
- Mention something relevant about the company.
- Avoid generic phrases.
- No hashtags.
- Return only the message.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        message = response.text
        return jsonify({"message": message})

    except Exception as error:
        return jsonify({"error": str(error)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)