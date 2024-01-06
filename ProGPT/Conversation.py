import requests
from requests import Session, Response, JSONDecodeError
import json
import random
import string
from uuid import uuid4


class Conversation:

    session: Session

    session_token: str
    conversation_id: str = None
    history_and_training_enabled: bool
    bearer_token: str

    def __init__(
            self,
            session_token: str,
            history_and_training_enabled: bool = False
    ) -> None:

        self.session_token = session_token
        self.history_and_training_enabled = history_and_training_enabled
        self.session: Session = requests.Session()

        self.session.cookies.set("__Secure-next-auth.session-token", self.session_token)
        self.session.headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
                                             "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

        self.refresh_bearer_token()

    def refresh_bearer_token(self) -> None:

        response: Response = self.session.get(
            url="https://chat.openai.com/api/auth/session",
            headers={
                "accept": "*/*",
                "accept-language": "en-US",
                "content-type": "application/json",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "Referer": "https://chat.openai.com",
                "Referrer-Policy": "strict-origin-when-cross-origin"
            }
        )

        try:
            response_json: dict = response.json()

            if "accessToken" not in response_json:
                raise Exception(
                    "Key 'accessToken' not in response JSON. Most probably you're not "
                    "logged in. Please check your credentials and try deleting the session file."
                )

            self.bearer_token = response_json["accessToken"]

        except JSONDecodeError:
            raise Exception(
                "HTTP Response is not a valid JSON. "
                "Please check your network connection or switch to another network."
            )

    def send(self, text: str) -> str:

        body: dict = {
            "action": "next",
            "arkose_token": "null",
            "conversation_mode": {
                "kind": "primary_assistant"
            },
            "force_paragen": False,
            "force_rate_limit": False,
            "history_and_training_disabled": not self.history_and_training_enabled,
            "messages": [{
                "metadata": {},
                "author": {
                    "role": "user"
                },
                "content": {
                    "content_type": "text",
                    "parts": [text]
                }
            }],
            "model": "text-davinci-002-render-sha",
            "parent_message_id": str(uuid4()),
            "timezone_offset_min": -330
        }

        if self.conversation_id is not None:
            body["conversation_id"] = self.conversation_id

        response: Response = self.session.post(
            url="https://chat.openai.com/backend-api/conversation",
            headers={
                "accept": "text/event-stream",
                "accept-language": "en-US",
                "authorization": f"Bearer {self.bearer_token}",
                "content-type": "application/json",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "Referer": "https://chat.openai.com",
                "Referrer-Policy": "strict-origin-when-cross-origin"
            },
            data=json.dumps(body)
        )

        data: dict = {}

        with open("test.txt", "w") as file:
            file.write(response.text)

        for chunk in response.text.split("\n"):

            if chunk[8:9] == "c" and "conversation_id" in json.loads(chunk[6:]):
                self.conversation_id = json.loads(chunk[6:])["conversation_id"]

            if chunk != "" and chunk != "data: [DONE]" and chunk[8:9] != "c":

                try: data: dict = json.loads(chunk[6:])
                except JSONDecodeError:
                    raise Exception("Couldn't parse assistant's answer into a valid JSON. Please try another prompt.")

        if data["message"]["status"] != "finished_successfully":

            raise Exception(
                "Assistant's message was not finished successfully. Most probably there's an issue with this package."
            )

        if data["message"]["content"]["content_type"] != "text":

            raise Exception(
                "Didn't receive 'text' data type as assistant's response."
            )

        message_parts: list = data["message"]["content"]["parts"]

        return "".join(message_parts)
