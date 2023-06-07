import requests


class ContractWatcherException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


def auth_required(function):
    def wrapper(self, *args, **kwargs):
        result = function(self, *args, **kwargs)

        if result is not None:
            return result

        authenticated = self.auth()

        if not authenticated:
            raise ContractWatcherException('Invalid user or password.')

        return function(self, *args, **kwargs)

    return wrapper


class ContractWatcher:
    username: str
    password: str

    _access: str | None = None

    def __init__(self, username: str, password: str, host: str = 'http://127.0.0.1:8000'):
        self.username = username
        self.password = password
        self.host = host

        if not self.auth():
            raise ContractWatcherException("Invalid username or password")

    def _build_url(self, path: str) -> str:
        return f'{self.host}{path}'

    def _build_auth_header(self) -> dict:
        return {'Authorization': f'Bearer {self._access}'}

    def post(self, path: str, headers: dict = None, json: bool = False, **kwargs):
        if json:
            return requests.post(self._build_url(path), json=kwargs, headers=headers)
        else:
            return requests.post(self._build_url(path), data=kwargs, headers=headers)

    def get(self, path: str, headers: dict = None):
        return requests.get(self._build_url(path), headers=headers)

    def delete(self, path: str, headers: dict = None):
        return requests.delete(self._build_url(path), headers=headers)

    def auth(self) -> bool:
        response = self.post('/api/auth/token', username=self.username, password=self.password)
        approved = response.status_code == 200

        if approved:
            self._access = response.json()['access_token']

        return approved

    @auth_required
    def history(self) -> dict | None:
        response = self.get('/api/history', self._build_auth_header())
        approved = response.status_code == 200

        if not approved:
            return None

        return response.json()

    @auth_required
    def webhooks(self) -> dict | None:
        response = self.get('/api/webhooks', self._build_auth_header())
        approved = response.status_code == 200

        if not approved:
            return None

        return response.json()

    @auth_required
    def create_webhook(self, address: str, event: str, url: str, label: str, abi: list[dict]) -> dict | None:
        response = self.post(
            '/api/webhooks',
            self._build_auth_header(),
            json=True,
            address=address,
            event=event,
            url=url,
            label=label,
            abi=abi
        )

        approved = response.status_code == 200

        if response.status_code == 422:
            print(response.text)
            return {}

        if not approved:
            return None

        return response.json()

    @auth_required
    def delete_webhook(self, wid: int) -> dict | None:
        response = self.delete(f'/api/webhooks/{wid}', self._build_auth_header())
        approved = response.status_code == 200

        if response.status_code == 404:
            return {}

        if not approved:
            return None

        return response.json()
