# ProGPT - Free GPT-3.5 API
I reverse engineered [ChatGPT 3.5](https://chat.openai.com)'s Free Web API and put it all together into this simple python package.

It supports both **Generative** & **Conversation** mode.

[<img style="margin-top: 10px" src="https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-1.svg" width="160"/>](https://buymeacoffee.com/diezo)

## 🌟 Just a minute!
ProGPT is still in it's early stages and requires your support. Don't forget to give a star. Thank you!

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

## 🤖 Generative
Used for independent prompts.

```python
from ProGPT import Generative

generative = Generative(session_token)  # See above on how to get session_token

print(generative.prompt("hello"))
```

## 💬 Conversation
Just like chat. AI will remember your past messages as well in the conversation.

```python
from ProGPT import Conversation

conversation = Conversation(session_token)  # See above on how to get session_token

print(conversation.send("hello"))
print(conversation.send("how's your day going?"))
print(conversation.send("i want to ask something..."))
```

## ⚡ Rate Limit
Nothing comes free of charge. While using this library is free, OpenAI does put some rate limits per hour when you ask questions too fast. You can use multiple accounts if that's a problem.

## Support
Want to support this project?

[<img src="https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-1.svg" width="150"/>](https://buymeacoffee.com/diezo)

## Legal
This is a third party library and not associated with OpenAI or ChatGPT. It is strictly for educational purposes only. You are liable for all the actions you take.
