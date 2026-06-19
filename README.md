# ProGPT - Python SDK for ChatGPT Conversations

[![PyPI](https://img.shields.io/pypi/v/progpt)](https://pypi.org/project/progpt)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/progpt)]()
[![Downloads](https://static.pepy.tech/badge/progpt)](https://pepy.tech/project/progpt)

![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge\&logo=openai\&logoColor=white)

ProGPT is an open-source Python client for ChatGPT conversations, providing a simple interface for generative and conversational workflows.

Both **Generative** & **Conversation** modes are supported.

[<img style="margin-top: 10px" src="https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-1.svg" width="160"/>](https://buymeacoffee.com/sonii)

## 📦 Installation

```python
$ pip install progpt
```

## 🔑 Authentication

In your browser:

1. Login to https://chat.openai.com
2. Open https://chat.openai.com/api/auth/session
3. Copy the value of `accessToken`

### 🚀 Generative Mode

Answers individual prompts without maintaining conversation history.

```python
from ProGPT import Generative

bot = Generative(access_token)

print(bot.prompt("who invented electricity?"))
```

### 💬 Conversation Mode

Creates a conversation thread and maintains chat history across prompts.

```python
from ProGPT import Conversation

bot = Conversation(access_token)

print(bot.prompt("hello"))
print(bot.prompt("how are you?"))
```

## ⚡ Usage Considerations

ChatGPT web services may enforce request limits depending on account status and usage patterns. Applications should implement appropriate retry logic and rate limiting when necessary.

## ❤️ Support Me

If you're benefitting from my work and wish to support me, please consider visiting this link:

[<img src="https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-1.svg" width="150"/>](https://buymeacoffee.com/sonii)

## 👮 Legal Notice

This project is an independent third-party library and is not affiliated with or endorsed by OpenAI.

Users are responsible for ensuring their usage complies with applicable terms of service, policies, and local regulations.
