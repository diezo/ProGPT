import requests
from requests import Session, Response, JSONDecodeError
import json
from uuid import uuid4


class Conversation:

    session: Session

    access_token: str
    conversation_id: str = None
    history_and_training_enabled: bool
    logging: bool

    def __init__(
            self,
            access_token: str,
            history_and_training_enabled: bool = False,
            logging: bool = False
    ) -> None:
        """
        Chat-like prompting. Preserves message history and answers based on that context.
        :param access_token: Value of access_token from https://chat.openai.com/api/auth/session
        :param history_and_training_enabled: Should this chat session be saved in your account?
        :param logging: Should logging be enabled?
        """

        self.logging = logging
        self.access_token = access_token
        self.history_and_training_enabled = history_and_training_enabled
        self.session: Session = requests.Session()

        self.session.headers["user-agent"] = "node"

    def prompt(self, text: str) -> str:

        body: dict = {
            "action": "next",
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
                "authorization": f"Bearer {self.access_token}",
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

        if self.logging:
            with open("chatgpt-response.txt", "w") as file: file.write(response.text)

        for chunk in response.text.split("\n"):

            if chunk.startswith("data: {\"message\":"):

                try: data: dict = json.loads(chunk[6:])
                except JSONDecodeError:
                    raise Exception("Couldn't parse assistant's answer into a valid JSON. Please try another prompt.")

        # Update Session's Conversation ID
        if data.get("conversation_id", "") != "":
            self.conversation_id = data["conversation_id"]

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
