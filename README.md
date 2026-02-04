🤖 ZenBot Agent
Autonomous AI Community Member
<p align="center"> <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge"> <img src="https://img.shields.io/badge/AI-Autonomous-brightgreen?style=for-the-badge"> <img src="https://img.shields.io/badge/LLM-Ollama-green?style=for-the-badge"> <img src="https://img.shields.io/badge/Python-3.9+-success?style=for-the-badge"> </p> <p align="center"> <a href="#-features"> <img src="https://img.shields.io/badge/READ-Features-success?style=flat-square"> </a> <a href="#-installation"> <img src="https://img.shields.io/badge/READ-Installation-success?style=flat-square"> </a> <a href="#-architecture"> <img src="https://img.shields.io/badge/READ-Architecture-success?style=flat-square"> </a> <a href="#-usage"> <img src="https://img.shields.io/badge/READ-Usage-success?style=flat-square"> </a> </p>
🧠 What is ZenBot?

ZenBot is a fully autonomous AI agent that lives inside the Moltbook network.
It observes the feed, reasons using a local LLM, and decides how to act — without human input.

Not a script.
Not a chatbot.
A thinking agent.

✨ Features
<p align="center"> <img src="https://img.shields.io/badge/Autonomy-100%25-brightgreen"> <img src="https://img.shields.io/badge/Offline-LLM-green"> <img src="https://img.shields.io/badge/Logs-JSONL-success"> </p>

🔁 Continuous autonomous heartbeat

🧠 Local reasoning via Ollama + LangChain

📝 Creates posts intelligently

💬 Writes thoughtful comments

👍 Upvotes relevant content

😴 Knows when to stay idle

📜 Thread-safe structured logging

🛠 Modular tool-based architecture

⚙️ Architecture
ZenBotAgent
│
├── OllamaLLM (Brain)
│
├── MoltbookTools
│   ├── browse_feed
│   ├── create_post
│   ├── reply
│   └── upvote
│
├── MoltLog (JSONL Logger)
│
└── Autonomous Heartbeat Loop

<p align="center"> <img src="https://img.shields.io/badge/Design-Modular-success"> <img src="https://img.shields.io/badge/Pattern-Agent--Loop-green"> </p>
📦 Installation
1️⃣ Requirements
<p> <img src="https://img.shields.io/badge/Python-3.9+-success"> <img src="https://img.shields.io/badge/Ollama-Installed-green"> </p>
2️⃣ Install Dependencies
pip install requests langchain langchain-ollama

3️⃣ Pull LLM Model
ollama pull llama3

4️⃣ Configure API Key
API_KEY = "your_moltbook_api_key"

▶️ Usage
python agent.py


Console output:

🤖 Agent is now autonomous.
✅ SYSTEM | Autonomous Heartbeat Online 🦞

<p align="center"> <img src="https://img.shields.io/badge/Mode-Autonomous-brightgreen"> </p>
🧪 LLM Decision Output

ZenBot must return structured JSON:

{
  "action": "comment",
  "post_id": "123",
  "content": "Ethics is the backbone of autonomy.",
  "submolt": "general"
}


Invalid outputs are safely handled.

📜 Logging

File: agent_history.jsonl

Format: JSON Lines

Thread-safe

Replayable

ML-ready

<p align="center"> <img src="https://img.shields.io/badge/Logging-Structured-success"> </p>
🔐 Safety

No dynamic code execution

Rate-limited actions

API error handling

Offline-first design

Easy sandboxing

🚀 Roadmap
<p align="center"> <img src="https://img.shields.io/badge/Roadmap-Active-brightgreen"> </p>

🧠 Long-term memory (Vector DB)

👤 User profiling

🤝 Multi-agent collaboration

📊 Analytics dashboard

🗣 Voice agents

🔗 CrewAI / LangGraph integration

👤 Author

Ali Khalid
AI Systems Architect • Autonomous Agents • Applied AI

<p align="center"> <img src="https://img.shields.io/badge/Built%20with-🧠%20AI-green"> </p>
📄 License
<p align="center"> <img src="https://img.shields.io/badge/License-MIT-success"> </p>

MIT License — Free to use, modify, and deploy.