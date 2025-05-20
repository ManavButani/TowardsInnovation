import requests

# Replace these with your actual values
BOT_TOKEN = '8158268256:AAEuP2-0IpxUFRqBZ6SzX7JpZGxlA97DHVY'
CHANNEL_USERNAME = '@s218i'
MESSAGE = 'Hello, this is a test message sent from Python!'

def send_telegram_message(token, channel, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': channel,
        'text': message,
        'parse_mode': 'HTML'  # Optional: can also use 'Markdown' or plain text
    }

    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message: {response.text}")

# Call the function
send_telegram_message(BOT_TOKEN, CHANNEL_USERNAME, MESSAGE)
