import responses


@responses.activate
def test_get_current_account(client, base_url):
    responses.add(
        responses.GET, f"{base_url}accounts/current", json={"id": "acc-1"}, status=200
    )
    assert client.accounts.get_current_account() == {"id": "acc-1"}


@responses.activate
def test_update_account(client, base_url):
    responses.add(
        responses.PUT,
        f"{base_url}accounts/acc-1",
        json={"id": "acc-1", "email": "a@b.com"},
        status=200,
    )
    assert client.accounts.update_account("acc-1", email="a@b.com") == {
        "id": "acc-1",
        "email": "a@b.com",
    }


@responses.activate
def test_delete_current_account(client, base_url):
    responses.add(
        responses.DELETE,
        f"{base_url}accounts/current",
        json={"deleted": True},
        status=200,
    )
    assert client.accounts.delete_current_account() == {"deleted": True}
