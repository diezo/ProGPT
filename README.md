# ProGPT - GPT-3.5 API Reverse Engineered
[![PyPI](https://img.shields.io/pypi/v/ensta)](https://pypi.org/project/ensta)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ensta)]()
[![Downloads](https://static.pepy.tech/badge/ensta)](https://pepy.tech/project/ensta)
[![Twitter Share](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Fdiezo%2Fensta)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2Fdiezo%2Fensta)

<!-- <img style="border-radius: 10px" src="https://raw.githubusercontent.com/diezo/Ensta/master/assets/logo.png"/> -->

I reverse engineered [ChatGPT 3.5](https://chat.openai.com)'s API and put it all together into this simple python package.

It supports both **Generative (Singular prompts)** & **Conversation (Chat-like)** mode.

[<img style="margin-top: 10px" src="https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-1.svg" width="160"/>](https://buymeacoffee.com/diezo)

## Installation
```shell
$ pip install progpt
```

### Get your session_token
1. Login to [chat.openai.com](https://chat.openai.com) in your computer.
2. Open DevTools by pressing **F12** or **Right Click > Inspect**
3. Click on the **Application** tab
4. Click on ```https://chat.openai.com``` under the **Cookies** tab
5. Copy the value of ```__Secure-next-auth.session-token``` cookie. This is your session_token.

## Generative
With this mode, the AI doesn't remember your prompts but rather responds to independent prompts.

```python
from ProGPT import Generative

generative = Generative(session_token)  # See above on how to get session_token

print(generative.prompt("hello"))
```

## Conversation
With this mode, the AI remembers your previous messages and responds to your prompts keeping them in mind.

```python
from ProGPT import Conversation

conversation = Conversation(session_token)  # See above on how to get session_token

print(conversation.send("hello"))
print(conversation.send("how's your day going?"))
print(conversation.send("i want to ask something..."))
```

## Donate
Wish to support this project? Please consider donating:

[<img src="https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-1.svg" width="150"/>](https://buymeacoffee.com/diezo)

## Legal
This is a third party library and not associated with OpenAI or ChatGPT. It is strictly for educational purposes only. You are liable for all the actions you take.
