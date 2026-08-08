import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
FACEBOOK_PAGE_ACCESS_TOKEN = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")

PAGE_ID = "957930724066023"

# API Key লোড হচ্ছে কিনা চেক
if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY is missing in GitHub Secrets!")

# কি-এর প্রথম ও শেষ অংশ প্রিন্ট করে রিভিল করা (সুরক্ষিতভাবে)
cleaned_key = GROQ_API_KEY.strip()
print(f"🔑 Key detected! Starts with: {cleaned_key[:5]}... Ends with: {cleaned_key[-4:]}")

def generate_live_news():
    print("🤖 Generating real-time latest tech news post using Groq...")
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
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {cleaned_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    
    response = requests.post(url, headers=headers, json=payload)
    res_data = response.json()
    
    if response.status_code == 200:
        return res_data['choices'][0]['message']['content']
    else:
        print("❌ Groq API Error Details:", res_data)
        raise RuntimeError(f"Groq API Error: {res_data}")

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
