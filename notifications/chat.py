import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Chat:

    chat_uri: str = None

    def send(self, contex: str) -> None:
        payload = {
            "channels":["chat"],
            "chatOptions": {
                "groupRecipients":["ניטור תקלות CLOUD POINT"]
            },
            "message":contex
        }
        try:
            response = requests.post(self.chat_uri, json=payload, verify=False)
            if response.status_code == 200:
                print("Message send successfully!!!")
            else:
                print(f"Failed to send message. Status code: {response.status_code}")
                print(f"Response: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"An error: {e}")