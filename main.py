import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
RAW_TOKEN = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
PAGE_ID = "957930724066023"

def get_page_access_token(user_token):
    """
    ইনপুট টোকেন থেকে স্বয়ংক্রিয়ভাবে আসল পেজ টোকেনটি এক্সট্র্যাক্ট করে।
    """
    url = f"https://graph.facebook.com/v20.0/me/accounts?access_token={user_token.strip()}"
    res = requests.get(url).json()
    
    if "data" in res:
        for page in res["data"]:
            if page.get("id") == PAGE_ID:
                print("🔑 Successfully retrieved Page Token for CN Bangla!")
                return page.get("access_token")
    return user_token.strip()

def generate_live_news():
    print("🤖 Generating tech news using Groq...")
    prompt = """
    Write an engaging Facebook news post in Bengali for "CN Bangla".
    Topic: Latest tech news or AI updates.
    Must adhere to Facebook standards. Clean output with headline, 2-3 paragraphs, and hashtags.
    """
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY.strip()}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()['choices'][0]['message']['content']

def post_to_facebook(message):
    # টোকেন এক্সট্র্যাক্ট
    valid_page_token = get_page_access_token(RAW_TOKEN)
    
    print(f"📤 Publishing to Page ID: {PAGE_ID}...")
    url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/feed"
    payload = {
        'message': message,
        'access_token': valid_page_token
    }
    response = requests.post(url, data=payload)
    res_data = response.json()
    
    if response.status_code == 200:
        print("✅ Success! Live post published to CN Bangla.")
        print("Post ID:", res_data.get('id'))
    else:
        print("❌ Facebook API Error Details:")
        print(res_data)
        raise RuntimeError(f"Facebook Post Failed: {res_data}")

if __name__ == "__main__":
    content = generate_live_news()
    post_to_facebook(content)
