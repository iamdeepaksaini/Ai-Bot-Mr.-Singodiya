import json
import requests
from flask import Flask, request
import subprocess

app = Flask(__name__)

TELEGRAM_API_URL = "https://api.telegram.org/bot7618634435:AAGbBdvclyDRwSeYJnl-ycfOn7VZcNlQ6G8/sendMessage"

# Webhook endpoint for receiving updates from Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()  # Webhook se data prapt karen
    
    chat_id = data['message']['chat']['id']
    user_message = data['message']['text']
    
    # Pollinations API ko request bheje
    payload = {
        "messages": [
            {"role": "system", "content": "You are Mr. Singodiya. A UPSC helper only"},
            {"role": "user", "content": user_message}
        ]
    }

    # curl command ko execute karen
    curl_command = [
        "curl", "-X", "POST", "https://text.pollinations.ai/",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload)
    ]
    
    # Pollinations se reply prapt karen
    response = subprocess.check_output(curl_command)
    response_data = json.loads(response)
    
    # Pollinations se reply ko extract karen
    reply_message = response_data['choices'][0]['message']['content']

    # Telegram par reply bheje
    send_message(chat_id, reply_message)
    
    return 'OK', 200

# Telegram ko message bhejne ka function
def send_message(chat_id, text):
    params = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(TELEGRAM_API_URL, params=params)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
