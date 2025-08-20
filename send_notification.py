import requests
import sys

def send_slack_message(text, webhook_url):
    payload = {"content": text}
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 204:
        print("Discord 메시지 전송 성공")
    else:
        print(f"Discord 전송 오류: {response.status_code}, {response.text}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python send_notification.py 'Message to send'")
        sys.exit(1)

    message = sys.argv[1]
    webhook_url = "https://discord.com/api/webhooks/1406954745448628234/hKwYgzRHHndk6u3uqC6xybDB2F0Laauy32VxZS1ruKfe658wzRfwE8E2wqZlWtM6UuKe"
    send_slack_message(message, webhook_url)


# os.system(f"python3 send_notification.py '{message}'")