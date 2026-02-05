from flask import Flask, jsonify, request, render_template_string
from auto_AI_agent import ZenBotAgent, LOG_FILE  # Importing your original code
import os
import json

app = Flask(__name__)

# Initialize your ZenBotAgent instance globally
# This ensures we control the SAME bot across different URL requests
bot = ZenBotAgent()

# --- API ENDPOINTS ---

@app.route('/status', methods=['GET'])
def get_status():
    """Check if the agent is currently running"""
    return jsonify({
        "agent_active": bot.is_running,
        "developer": "Ali Khalid",
        "system": "Moltbook Autonomous Intelligence"
    })

@app.route('/start', methods=['GET', 'POST'])
def start_bot():
    """Trigger the .start() method from your ZenBotAgent class"""
    if not bot.is_running:
        bot.start()
        return jsonify({"message": "ZenBot started! Ali Khalid's agent is now online."})
    return jsonify({"message": "Agent is already running."})

@app.route('/stop', methods=['GET', 'POST'])
def stop_bot():
    """Stop the agent loop safely"""
    bot.is_running = False
    return jsonify({"message": "Stop signal sent to ZenBot."})

@app.route('/logs', methods=['GET'])
def get_logs():
    """Read your LOG_FILE (agent_history.jsonl) and return the latest 20 actions"""
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            # Parse the last 20 lines of JSONL
            for line in lines[-20:]:
                try:
                    logs.append(json.loads(line))
                except:
                    continue
    return jsonify(logs[::-1]) # Returns newest logs first

# --- SIMPLE DASHBOARD ---

@app.route('/')
def dashboard():
    """A simple HTML view to see everything at once"""
    html = """
    <html>
        <head><title>ZenBot Control Panel</title></head>
        <body style="font-family: sans-serif; padding: 50px; background: #f4f4f9;">
            <h1>🦞 ZenBot Dashboard</h1>
            <p>Developed by: <strong>Ali Khalid</strong></p>
            <hr>
            <div>
                <button onclick="fetch('/start', {method:'POST'}).then(()=>location.reload())">▶ Start Agent</button>
                <button onclick="fetch('/stop', {method:'POST'}).then(()=>location.reload())">⏹ Stop Agent</button>
                <button onclick="location.reload()">🔄 Refresh View</button>
            </div>
            <h3>Recent Activity:</h3>
            <iframe src="/logs" width="100%" height="400px" style="background: white; border: 1px solid #ccc;"></iframe>
        </body>
    </html>
    """
    return render_template_string(html)

if __name__ == "__main__":
    # Changed from 6000 to 5050 to avoid ERR_UNSAFE_PORT
    print("🚀 ZenBot Dashboard starting on http://127.0.0.1:5050")
    app.run(host='127.0.0.1', port=5050, debug=False)