from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# MongoDB connection
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client.githubEvents
collection = db.events

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    event = request.headers.get("X-GitHub-Event")
    author = data.get("sender", {}).get("login", "unknown")

    entry = {
        "event": event,
        "author": author,
        "data": data,
        "timestamp": datetime.utcnow()
    }

    collection.insert_one(entry)
    return jsonify({"status": "received"}), 200

@app.route("/api/events", methods=["GET"])
def get_events():
    events = collection.find().sort("timestamp", -1).limit(10)
    output = []

    for e in events:
        ts = e["timestamp"].strftime("%d %B %Y - %I:%M %p UTC")
        if e["event"] == "push":
            ref = e["data"].get("ref", "")
            branch = ref.split("/")[-1]
            msg = f'{e["author"]} pushed to {branch} on {ts}'
        elif e["event"] == "pull_request":
            pr = e["data"].get("pull_request", {})
            from_branch = pr.get("head", {}).get("ref", "")
            to_branch = pr.get("base", {}).get("ref", "")
            action = e["data"].get("action", "")
            if action == "closed" and pr.get("merged", False):
                msg = f'{e["author"]} merged branch {from_branch} to {to_branch} on {ts}'
            else:
                msg = f'{e["author"]} submitted a pull request from {from_branch} to {to_branch} on {ts}'
        else:
            msg = f'{e["author"]} triggered {e["event"]} on {ts}'

        output.append(msg)

    return jsonify(output)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
