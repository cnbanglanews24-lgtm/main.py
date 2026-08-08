import os
import requests
from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
FACEBOOK_PAGE_ACCESS_TOKEN = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")

# আপনার CN Bangla পেজের নির্দিষ্ট ID
PAGE_ID = "957930724066023"

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
    print(f"📤 Publishing live post directly to Page ID: {PAGE_ID}...")
    
    url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/feed"
    payload = {
        'message': message,
        'access_token': FACEBOOK_PAGE_ACCESS_TOKEN
    }
    response = requests.post(url, data=payload)
    res_data = response.json()
    
    if response.status_code == 200:
        print("✅ Success! Live post published successfully to CN Bangla.")
        print("Post ID:", res_data.get('id'))
    else:
        print("❌ Facebook API Error Details:")
        print(res_data)
        raise RuntimeError(f"Facebook Post Failed: {res_data}")

if __name__ == "__main__":
    news_content = generate_live_news()
    print("\n--- Generated News Content ---")
    print(news_content)
    print("------------------------------\n")
    post_to_facebook(news_content)
