import json

import requests
from fastapi import status
from requests import Response, request

from app.pydantic_models import Env


class TelegramApi:
    METHOD_SET_WEBHOOK = 'setWebhook'
    METHOD_SEND_MESSAGE = 'sendMessage'

    def __init__(self, env: Env) -> None:
        self.route = f'https://api.telegram.org/bot{env.tg_bot_token}/'
        self.listener_url = f'{env.ngrok_url}/message/'

    def _request(
            self,
            method: str,
            url: str,
            data: dict | None = None,
        ) -> Response:
        try:
            response = request(method=method, url=url, data=data, timeout=30)
        except requests.exceptions.Timeout as timeout_err:
            # Log request error timeout TODO
            raise requests.exceptions.Timeout from timeout_err
        except requests.exceptions.RequestException as request_err:
            # Log request error TODO
            raise requests.exceptions.RequestException from request_err
        if response.status_code != status.HTTP_200_OK:
            # Log request error wrong status code TODO
            raise Exception
        return response

    async def set_webhook(self) -> dict:
        data = {
            'url': self.listener_url,
            'drop_pending_updates': True,
        }
        telegram_url = self.route + self.METHOD_SET_WEBHOOK
        response = self._request(method='post', url=telegram_url, data=data)
        return response.json()

    async def send_message(
            self,
            chat_id: int,
            text: str,
            reply: bool = False,
            reply_markup: dict | None = None,
        ) -> dict:
        data = {
            'chat_id': chat_id,
            'text': text,
            'reply': reply
        }
        if reply and reply_markup:
            data['reply_markup'] = json.dumps(reply_markup)
        telegram_url = self.route + self.METHOD_SEND_MESSAGE
        response = self._request(method='post', url=telegram_url, data=data)
        return response.json()
