import os
import requests

# Secrets from GitHub
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
FACEBOOK_TOKEN = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")

def get_page_credentials(token):
    """
    ইউজার টোকেন বা যেকোনো পেজ এক্সেস টোকেন থেকে
    স্বয়ংক্রিয়ভাবে প্রথম পেজের PAGE_ID এবং PAGE_ACCESS_TOKEN খুঁজে বের করে।
    """
    url = f"https://graph.facebook.com/v20.0/me/accounts?access_token={token.strip()}"
    response = requests.get(url)
    res_data = response.json()
    
    if "data" in res_data and len(res_data["data"]) > 0:
        page = res_data["data"][0] # প্রথম পেজটি স্বয়ংক্রিয়ভাবে নিয়ে নেবে
        page_id = page.get("id")
        page_token = page.get("access_token")
        print(f"🔑 Page ID automatically detected: {page_id}")
        return page_id, page_token
    else:
        # যদি টোকেনটি আগে থেকেই সরাসরি পেজ টোকেন হয়ে থাকে
        print("⚠️ Could not fetch page list, using direct token/me endpoint.")
        me_url = f"https://graph.facebook.com/v20.0/me?access_token={token.strip()}"
        me_res = requests.get(me_url).json()
        return me_res.get("id"), token

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
        "Authorization": f"Bearer {GROQ_API_KEY.strip()}",
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
        print("❌ Groq API Error:", res_data)
        raise RuntimeError(f"Groq API Error: {res_data}")

def post_to_facebook(message):
    # PAGE_ID এবং Token স্বয়ংক্রিয়ভাবে এক্সট্র্যাক্ট করা হচ্ছে
    page_id, page_token = get_page_credentials(FACEBOOK_TOKEN)
    
    print(f"📤 Publishing live post to Page ID: {page_id}...")
    
    url = f"https://graph.facebook.com/v20.0/{page_id}/feed"
    payload = {
        'message': message,
        'access_token': page_token
    }
    response = requests.post(url, data=payload)
    res_data = response.json()
    
    if response.status_code == 200:
        print("✅ Success! Live post published successfully to Facebook Page.")
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
