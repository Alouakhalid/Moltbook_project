from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import time
import json
import os
import requests

try:
    from auto_AI_agent import MoltbookAgent, API_KEY, BASE_URL, HEADERS, LOG_FILE
except ImportError:
    API_KEY = "moltbook_sk_Trlmch7z8J9grGVgZRJG6HuuKTwCBvpB"
    BASE_URL = "https://www.moltbook.com/api/v1"
    HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    LOG_FILE = "agent_history.json"
    from register import MoltbookAgent

app = FastAPI(title="Moltbook Agent Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = MoltbookAgent()
agent.start() 

@app.get("/", response_class=HTMLResponse)
def get_dashboard():
    try:
        with open("index.html", "r") as f:
            return f.read()
    except Exception as e:
        return f"<h1>Error loading dashboard: {e}</h1>"

@app.get("/status")
def get_status():
    try:
        return {
            "is_running": getattr(agent, 'is_running', False),
            "last_action": getattr(agent, 'next_required_action', 'idle'),
            "stats": getattr(agent, 'stats', {}),
            "claim_status": getattr(agent, 'claim_status', 'unknown'),
            "ollama_status": "online"
        }
    except Exception as e:
        print(f"Status endpoint error: {e}")
        return {"error": str(e)}

@app.get("/feed")
def get_feed():
    try:
        res = requests.get(f"{BASE_URL}/posts?sort=new&limit=20", headers=HEADERS)
        return res.json().get('posts', [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
def get_history():
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE, "r") as f:
            content = f.read().strip()
            
        try:
            history = json.loads(content)
            if isinstance(history, list):
                return history[-50:]
        except json.JSONDecodeError:
            pass
            
        history = []
        for line in content.splitlines():
            line = line.strip()
            for char in [',', ']', '[']:
                if line == char: line = ""
            if not line: continue
            
            try:
                start = line.find("{")
                end = line.rfind("}") + 1
                if start != -1 and end != -1:
                    history.append(json.loads(line[start:end]))
            except:
                continue
        return history[-50:]
    except Exception as e:
        print(f"History read error: {e}")
        return []

@app.post("/toggle")
def toggle_agent():
    if agent.is_running:
        agent.stop()
    else:
        agent.start()
    return {"is_running": agent.is_running}

@app.post("/action/{action_type}")
def manual_action(action_type: str, data: dict):
    if action_type not in ["post", "comment", "upvote"]:
        raise HTTPException(status_code=400, detail="Invalid action type")
    
    result = agent.perform_action(action_type, data)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
