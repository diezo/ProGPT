import requests
from requests import Session, Response, JSONDecodeError
import json
from uuid import uuid4
import websockets
import base64
from time import time, sleep
import asyncio
import threading


class Generative:

    session: Session

    access_token: str
    history_and_training_enabled: bool
    logging: bool

    websocket_url: str
    last_message: tuple[str, str] | None = None

    response_wait_time_limit: float = 10.0  # Seconds

    def __init__(
            self,
            access_token: str,
            history_and_training_enabled: bool = False,
            logging: bool = False
    ) -> None:
        """
        Single prompting. Doesn't preserve message history. Answers are not based on the previous context.
        :param access_token: Value of access_token from https://chat.openai.com/api/auth/session
        :param history_and_training_enabled: Should this chat session be saved in your account?
        :param logging: Should logging be enabled?
        """

        self.logging = logging
        self.access_token = access_token
        self.history_and_training_enabled = history_and_training_enabled
        self.session: Session = requests.Session()

        self.session.headers["user-agent"] = "node"

        self.register_websocket()

        self.connect_websocket()
        # asyncio.get_event_loop().run_until_complete(self.connect_websocket())
        # asyncio.run(self.connect_websocket())
        threading.Thread(target=asyncio.new_event_loop().run_until_complete, args=(self.connect_websocket(),)).start()

        # Wait for websocket connection to be established
        sleep(2)  # TODO: Maybe uncomment

    async def connect_websocket(self) -> None:
        """
        Uses websockets library to connect to the chat websocket server. This
        websocket connection is only used to retrieve messages and not send them.
        :return: None
        """

        async with websockets.connect(self.websocket_url) as websocket:

            while True:
                # noinspection PyBroadException
                try:
                    response: dict = json.loads(str(await websocket.recv()))

                    body: str = response.get("body", "")
                    body: str = base64.b64decode(body).decode("utf-8") if body != "" else ""

                    response_id: str = response.get("response_id", "")

                    if body != "" and response_id != "":
                        if body.startswith("data: {\"message"):
                            if json.loads(body[6:]).get("message").get("status") == "finished_successfully":
                                self.last_message = (body, response_id)

                    if self.logging:
                        with open("chatgpt-response.txt", "w") as file: file.write(json.dumps(response))

                except Exception as exception:
                    if self.logging: print(exception)

    def register_websocket(self) -> None:
        response: Response = self.session.post(
            url="https://chat.openai.com/backend-api/register-websocket",
            headers={
                "authorization": f"Bearer {self.access_token}",
                "sec-fetch-dest": "empty",
            }
        )

        try:
            self.websocket_url = response.json().get("wss_url", "")

        except JSONDecodeError:
            raise JSONDecodeError(
                "Couldn't retrieve websocket url. Is the access_token correct? "
                "Are you sure your account isn't restricted?"
            )

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
                "Referer": "https://chat.openai.com/",
                "Referrer-Policy": "strict-origin-when-cross-origin"
            },
            data=json.dumps(body)
        )

        try:
            response_id: str = response.json().get("response_id")
            time_snapshot: float = time()

            while True:
                if time() - time_snapshot >= self.response_wait_time_limit:
                    raise Exception(
                        f"Response time out. Didn't got the prompt response within "
                        f"{self.response_wait_time_limit} seconds."
                    )

                if self.last_message is not None and self.last_message[1] == response_id:
                    return self.last_message[0]

        except JSONDecodeError:
            raise JSONDecodeError(
                "Couldn't get response_id from this prompt."
            )

        # for chunk in response.text.split("\n"):
        #
        #     if chunk.startswith("data: {\"message\":"):
        #
        #         try: data: dict = json.loads(chunk[6:])
        #         except JSONDecodeError:
        #             raise Exception("Couldn't parse assistant's answer into a valid JSON. Please try another prompt.")
        #
        # if data["message"]["status"] != "finished_successfully":
        #
        #     raise Exception(
        #         "Assistant's message was not finished successfully. Most probably there's an issue with this package."
        #     )
        #
        # if data["message"]["content"]["content_type"] != "text":
        #
        #     raise Exception(
        #         "Didn't receive 'text' data type as assistant's response."
        #     )
        #
        # message_parts: list = data["message"]["content"]["parts"]
        #
        # return "".join(message_parts)
