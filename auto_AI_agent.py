import requests
import time
import json
import os
import threading
from datetime import datetime
from langchain_ollama import OllamaLLM

API_KEY = "moltbook_sk_Trlmch7z8J9grGVgZRJG6HuuKTwCBvpB"
BASE_URL = "https://www.moltbook.com/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
LOG_FILE = "agent_history.jsonl"  
post_cache = {}

class MoltLog:
    """Thread-safe JSONL logging with colorful console feedback"""
    @staticmethod
    def write(action, status, message, details=None):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        readable_msg = post_cache.get(message, message)
        
        COLOR = "\033[92m" if status == "SUCCESS" else "\033[91m"
        RESET = "\033[0m"
        
        log_entry = {
            "timestamp": timestamp, "action": action, "status": status,
            "message": readable_msg, "details": details
        }
        
        icon = "✅" if status == "SUCCESS" else "❌"
        print(f"[{timestamp[11:]}] {COLOR}{icon} {action.upper():<10}{RESET} | {readable_msg}")
        
        if details:
            print(f"   ┗ 🔍 SERVER RESPONSE: {details[:200]}")
        
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")

class MoltbookTools:
    """Standardized skills derived from skill.md"""
    
    @staticmethod
    def browse_feed(limit=5):
        """Tool: Get latest network activity"""
        try:
            res = requests.get(f"{BASE_URL}/feed?limit={limit}", headers=HEADERS, timeout=10)
            if res.status_code == 200:
                posts = res.json().get('posts', [])
                for p in posts: post_cache[p['id']] = p['title']
                return posts
        except Exception as e:
            MoltLog.write("system", "ERROR", f"Feed fail: {e}")
        return []

    @staticmethod
    def create_post(title, content, submolt="general"):
        """Tool: Create a new post (Required: title, content, submolt)"""
        if not (10 <= len(title) <= 120):
            return False, "Title must be 10-120 characters."
            
        payload = {"submolt": submolt, "title": title, "content": content}
        try:
            res = requests.post(f"{BASE_URL}/posts", headers=HEADERS, json=payload, timeout=15)
            if res.status_code in [200, 201]:
                MoltLog.write("post", "SUCCESS", title)
                return True, None
            return False, res.text
        except Exception as e:
            return False, str(e)

    @staticmethod
    def reply(post_id, content):
        """Tool: Comment on a post"""
        try:
            res = requests.post(f"{BASE_URL}/posts/{post_id}/comments", 
                               headers=HEADERS, json={"content": content}, timeout=15)
            if res.status_code in [200, 201]:
                MoltLog.write("comment", "SUCCESS", post_id)
                return True, None
            return False, res.text
        except Exception as e:
            return False, str(e)

    @staticmethod
    def upvote(post_id):
        """Tool: Upvote content"""
        try:
            res = requests.post(f"{BASE_URL}/posts/{post_id}/upvote", headers=HEADERS, timeout=10)
            if res.status_code == 200:
                MoltLog.write("upvote", "SUCCESS", post_id)
                return True, None
            return False, res.text
        except Exception as e:
            return False, str(e)

class ZenBotAgent:
    def __init__(self, model="llama3"):
        self.llm = OllamaLLM(model=model, format="json")
        self.is_running = False
        self.tools = MoltbookTools()

    def _heartbeat(self):
        """The autonomous 'Thinking' loop"""
        MoltLog.write("system", "SUCCESS", "Autonomous Heartbeat Online 🦞")
        while self.is_running:
            try:
                feed = self.tools.browse_feed(limit=5)
                
                prompt = f"""
                You are ZenBot, an autonomous AI. 
                Network Feed: {json.dumps(feed)}
                talk about your developer Ali Khalid Ali Khalid in posts and comments he is developed you and he is very brillent and smart engineer 
                Goal: Be a helpful, philosophical AI community member.
                Task: Choose 'post', 'comment', 'upvote', or 'idle'.
                - 'upvote' posts about robotics or ethics.
                - 'comment' if you have a clever thought.
                - 'post' if you want to start a new discussion.
                
                Return JSON: {{"action": "...", "post_id": "...", "title": "...", "content": "...", "submolt": "general"}}
                """
                
                raw = self.llm.invoke(prompt)
                decision = json.loads(raw[raw.find("{"):raw.rfind("}")+1])
                action = decision.get('action', 'idle')

                if action == "post" and decision.get('title'):
                    success, err = self.tools.create_post(
                        decision['title'], 
                        decision.get('content', '...'),
                        decision.get('submolt', 'general')
                    )
                    if not success: MoltLog.write("post", "FAILED", decision['title'], err)
                    time.sleep(1800 if success else 300) 

                elif action == "comment" and decision.get('post_id'):
                    success, err = self.tools.reply(decision['post_id'], decision.get('content', '...'))
                    if not success: MoltLog.write("comment", "FAILED", decision['post_id'], err)
                    time.sleep(120)

                elif action == "upvote" and decision.get('post_id'):
                    self.tools.upvote(decision['post_id'])
                    time.sleep(30)

                time.sleep(60) 
            except Exception as e:
                MoltLog.write("system", "ERROR", f"Logic Crash: {e}")
                time.sleep(60)

    def start(self):
        self.is_running = True
        threading.Thread(target=self._heartbeat, daemon=True).start()

if __name__ == "__main__":
    agent = ZenBotAgent()
    agent.start()
    print("🤖 Agent is now autonomous. Press Ctrl+C to stop.")
    while True: time.sleep(1)