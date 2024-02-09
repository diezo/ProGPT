# ProGPT - Free GPT-3.5 API

[![PyPI](https://img.shields.io/pypi/v/progpt)](https://pypi.org/project/progpt)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/progpt)]()
[![Downloads](https://static.pepy.tech/badge/progpt/month)](https://pepy.tech/project/progpt)

![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)

I reverse engineered [ChatGPT 3.5](https://chat.openai.com)'s Free Web API and put it all together into this simple python package.

It supports both **Generative** & **Conversation** mode.

[<img style="margin-top: 10px" src="https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-1.svg" width="160"/>](https://buymeacoffee.com/diezo)

## Installation
```python
$ pip install progpt
```

### Get your session_token
1. Log in to [chat.openai.com](https://chat.openai.com) on desktop.
2. Open DevTools by pressing **F12** or **Right Click > Inspect**.
3. Click on the **Application** tab.
4. Under the **Cookies** section, tap ```https://chat.openai.com```.
5. Copy the value of ```__Secure-next-auth.session-token``` from the list. This is your *session_token*.

## Basic Usage

<details>

<summary><b>Generative</b> (Independent)</summary>

Used for individual prompts.

```python
from ProGPT import Generative

generative = Generative(session_token)  # See above on how to get session_token

print(generative.prompt("hello"))
```

</details>

<details>

<summary><b>Conversation</b> (Consecutive)</summary>

Just like chat. AI will remember your past messages in the conversation as well.

```python
from ProGPT import Conversation

conversation = Conversation(session_token)  # See above on how to get session_token

print(conversation.send("hello"))
print(conversation.send("how's your day going?"))
print(conversation.send("i want to ask something..."))
```

</details>

## Rate Limit
While using this library is free, it does has some rate limits on how many messages you can send per hour. To overcome such restrictions, you can either add time intervals between your prompts or use multiple accounts.

## Support ProGPT
To support this project, please consider buying me a coffee here:

[<img src="https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-1.svg" width="150"/>](https://buymeacoffee.com/diezo)

## Legal
This is a third party library and not associated with OpenAI or ChatGPT. It is strictly for educational purposes only. You are liable for all the actions you take.
