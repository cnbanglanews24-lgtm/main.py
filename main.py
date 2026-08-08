import os
import requests
from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
FACEBOOK_PAGE_ACCESS_TOKEN = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_live_news():
    print("🤖 Generating real-time latest tech news post...")
    prompt = """
    Write an engaging, highly professional, and authentic Facebook news post in Bengali for a news page named "CN Bangla".
    Topic: Focus on the absolute latest trending technology news, recent gadget launches, or AI/software updates.
    Strict Guidelines:
    1. Absolute Policy Compliance: Must strictly adhere to Facebook Community Standards. Zero misinformation, zero clickbait.
    2. Output Format:
       - Direct Bengali template post only.
       - Include an eye-catching headline.
       - Provide 2-3 short, clear, informative paragraphs in clean Bengali.
       - Include 4-5 relevant hashtags (e.g., #CNBangla #TechNews #LatestUpdate).
       - Do NOT include any intro, outro, commentary, or meta-text. Return strictly the post text.
    """
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt,
    )
    return response.text

def post_to_facebook(message):
    print("📤 Publishing live post to Facebook Page...")
    url = "https://graph.facebook.com/v20.0/me/feed"
    payload = {
        'message': message,
        'access_token': FACEBOOK_PAGE_ACCESS_TOKEN
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("✅ Success! Live post published successfully.")
        print("Post ID:", response.json().get('id'))
    else:
        print("❌ Failed to publish post:", response.json())

if __name__ == "__main__":
    try:
        news_content = generate_live_news()
        print("\n--- Generated News Content ---")
        print(news_content)
        print("------------------------------\n")
        post_to_facebook(news_content)
    except Exception as e:
        print("❌ Error during execution:", e)
