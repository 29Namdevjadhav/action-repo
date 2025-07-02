# Webhook Receiver App

This Flask app receives GitHub webhook events and stores them in MongoDB.
It also provides a minimal UI to view recent events.

## Features

- Receives webhooks for Push, Pull Request, and Merge
- Stores events in MongoDB
- UI polls every 15 seconds and shows activity in clean format

## Setup Instructions

### 1. Clone Repo

```bash
git clone https://github.com/29Namdevjadhav/webhook-repo.git
cd webhook-repo
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start MongoDB

Use either local MongoDB or [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)

### 4. Run Flask App

```bash
export MONGO_URI="your-mongodb-uri"
python app.py
```

### 5. Expose to Internet

Use [ngrok](https://ngrok.com/):

```bash
ngrok http 5000
```

Use the HTTPS URL given by ngrok as your GitHub webhook URL.

### 6. Set Webhook on GitHub

In your `action-repo`, go to:
- Settings → Webhooks → Add Webhook
- Payload URL: `https://your-ngrok-url/webhook`
- Content type: `application/json`
- Events: Push, Pull Request

Done! Trigger events to see them show up live in the browser.
