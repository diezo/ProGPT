from requests import Session
from requests import Response, JSONDecodeError
from urllib.parse import unquote_plus, quote_plus


class Authentication:

    @staticmethod
    def login(email: str, password: str) -> str:

        session: Session = Session()

        session.headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
                                        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

        session.get(
            url="https://chat.openai.com/api/auth/session",
            headers={
                "accept": "*/*",
                "accept-language": "en-US,en;q=0.9",
                "content-type": "application/x-www-form-urlencoded",
                "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "Referer": "https://chat.openai.com/auth/login",
                "Referrer-Policy": "strict-origin-when-cross-origin"
            }
        )

        redirect_response: Response = session.post(
            url="https://chat.openai.com/api/auth/signin/auth0?prompt=login",
            headers={
                "accept": "*/*",
                "accept-language": "en-US,en;q=0.9",
                "content-type": "application/x-www-form-urlencoded",
                "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "Referer": "https://chat.openai.com/auth/login",
                "Referrer-Policy": "strict-origin-when-cross-origin"
            },
            data=f'callbackUrl=%2F&csrfToken='
                 f'{unquote_plus(session.cookies.get("__Host-next-auth.csrf-token")).split("|")[0]}'
                 f'&json=true'
        )

        try:
            redirect_response_json: dict = redirect_response.json()

            if "url" not in redirect_response_json:
                raise Exception("Key 'url' not in response JSON. Most probably it's a CSRF issue with this package.")

            # Get State
            state: str = session.get(
                redirect_response_json["url"],
                allow_redirects=False
            ).headers.get("location").split("state=")[-1]

            # Load Login Page for Cookies!
            session.get(
                url=f"https://auth0.openai.com/u/login/password?state={state}",
                headers={
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                              "image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "accept-language": "en-US,en;q=0.9",
                    "cache-control": "no-cache",
                    "pragma": "no-cache",
                    "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": "\"Windows\"",
                    "sec-fetch-dest": "document",
                    "sec-fetch-mode": "navigate",
                    "sec-fetch-site": "same-origin",
                    "sec-fetch-user": "?1",
                    "upgrade-insecure-requests": "1",
                    "Referer": f"https://auth0.openai.com/u/login/identifier?state={state}",
                    "Referrer-Policy": "same-origin"
                }
            )

            # Authenticate
            auth_response: Response = session.post(
                url=f"https://auth0.openai.com/u/login/password?state={state}",
                headers={
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,"
                              "image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "accept-language": "en-US,en;q=0.9",
                    "cache-control": "max-age=0",
                    "content-type": "application/x-www-form-urlencoded",
                    "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": "\"Windows\"",
                    "sec-fetch-dest": "document",
                    "sec-fetch-mode": "navigate",
                    "sec-fetch-site": "same-origin",
                    "sec-fetch-user": "?1",
                    "upgrade-insecure-requests": "1",
                    "Referer": f"https://auth0.openai.com/u/login/password?state={state}",
                    "Referrer-Policy": "same-origin"
                },
                data=f"state={state}&username={quote_plus(email)}&password={quote_plus(password)}",
                allow_redirects=False
                # data={
                #     "state": state,
                #     "username": email,
                #     "password": password
                # }
            )

            return auth_response.status_code

        except JSONDecodeError:
            raise Exception("HTTP response is not a valid JSON. Most probably it's a CSRF issue with this package.")
