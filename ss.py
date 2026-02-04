import requests

API_KEY = "moltbook_sk_Trlmch7z8J9grGVgZRJG6HuuKTwCBvpB"
POST_ID = "cf0f5407-90dd-4dda-a8ea-8ed6ed19b1ae"
url = f"https://www.moltbook.com/api/v1/posts/{POST_ID}"
headers = {"Authorization": f"Bearer {API_KEY}"}

response = requests.get(url, headers=headers)
print(response.json())