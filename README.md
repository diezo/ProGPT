# ProGPT - Free GPT-3.5 API

[![PyPI](https://img.shields.io/pypi/v/progpt)](https://pypi.org/project/progpt)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/progpt)]()
[![Downloads](https://static.pepy.tech/badge/progpt/month)](https://pepy.tech/project/progpt)

![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)

I reverse engineered [ChatGPT 3.5](https://chat.openai.com)'s Free Web API and put it all together into this simple python package.

Both **Generative** & **Conversation** modes are supported.

[<img style="margin-top: 10px" src="https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-1.svg" width="160"/>](https://buymeacoffee.com/diezo)

## Installation
```python
$ pip install progpt
```

### Get Session Token
1. Log in to [chat.openai.com](https://chat.openai.com) on desktop.
2. Open DevTools by pressing **F12** or **Right Click > Inspect**.
3. Click on the **Application** tab.
4. Under the **Cookies** section, tap ```https://chat.openai.com```.
5. Copy the value of ```__Secure-next-auth.session-token``` from the list. This is your *session_token*.

## Basic Usage

<details>

<summary><b>Generative</b> (Independent)</summary>

It'll answer individual prompts, not based on previous messages.

```python
from ProGPT import Generative

bot = Generative(session_token)

print(generative.prompt("who invented electricity?"))
```

</details>

<details>

<summary><b>Conversation</b> (Remembers History)</summary>

It'll create a new conversation thread so ChatGPT remembers your message history.

```python
from ProGPT import Conversation

bot = Conversation(session_token)

print(bot.send("hello"))
print(bot.send("how are you?"))
```

</details>

## Rate Limit
To overcome the free rate limits:
1. Add time gap between prompts
2. Use multiple accounts

## Support Me
To support this project, please consider visiting this link:

**PayPal:** [**@gitdiezo**](https://www.paypal.com/paypalme/gitdiezo)

[<img src="https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-1.svg" width="150"/>](https://buymeacoffee.com/diezo)

## Legal
This is a third party library and not associated with OpenAI or ChatGPT. It's strictly for educational purposes. You are liable for all the actions you take.
