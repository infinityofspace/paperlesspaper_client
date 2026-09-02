import json

from paperlesspaper_client import cli


class _FakeUsers:
    def __init__(self):
        self.last_delete_user_id = None

    def delete_user(self, user_id):
        self.last_delete_user_id = user_id
        return {"deleted": user_id}


class _FakeClient:
    last_api_key = None

    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url
        self.users = _FakeUsers()
        _FakeClient.last_api_key = api_key


def test_cli_users_delete_uses_option_token_over_env(monkeypatch, capsys):
    monkeypatch.setenv("PAPERLESSPAPER_API_KEY", "env-token")
    monkeypatch.setattr(cli, "Client", _FakeClient)

    exit_code = cli.main(["--api-key", "option-token", "users", "delete", "u1"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert _FakeClient.last_api_key == "option-token"
    assert json.loads(captured.out) == {"deleted": "u1"}


def test_cli_users_delete_uses_env_token_if_option_missing(monkeypatch, capsys):
    monkeypatch.setenv("PAPERLESSPAPER_API_KEY", "env-token")
    monkeypatch.setattr(cli, "Client", _FakeClient)

    exit_code = cli.main(["users", "delete", "u2"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert _FakeClient.last_api_key == "env-token"
    assert json.loads(captured.out) == {"deleted": "u2"}
